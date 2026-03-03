"""Note migrator orchestrator."""

from pathlib import Path

from dx_vault_atlas.services.note_migrator.core.errors import (
    EditorCancelledError,
    FileReadError,
    FrontmatterParseError,
    MissingFieldsError,
)
from dx_vault_atlas.services.note_migrator.core.interfaces import (
    IEditorService,
    ISchemaUpgrader,
    ITransformer,
    ITypeHeuristics,
    IYamlParser,
)
from dx_vault_atlas.services.note_migrator.models.frontmatter import FrontmatterSchema
from dx_vault_atlas.services.note_migrator.models.migration import (
    MigrationResult,
    MigrationStatus,
)
from dx_vault_atlas.services.note_migrator.services.editor_buffer import (
    EditorAbortedError,
)
from dx_vault_atlas.services.note_migrator.services.file_repository import (
    FileRepository,
)
from dx_vault_atlas.services.note_migrator.services.yaml_parser import YamlParseError


class NoteMigrator:
    """Orchestrates the migration of a single note.

    Handles parsing, type detection, user prompts for missing fields,
    validation, and writing the migrated note.
    """

    # Empty fields, schema enforced dynamically.

    def __init__(
        self,
        yaml_parser: IYamlParser,
        editor_service: IEditorService,
        heuristics: ITypeHeuristics,
        schema_upgrader: ISchemaUpgrader,
        transformation_service: ITransformer,
        file_repository: FileRepository,
    ) -> None:
        """Initialize migrator with services.

        Args:
            yaml_parser: Yaml parser service.
            editor_service: Editor buffer service.
            heuristics: Type heuristics service.
            schema_upgrader: Schema upgrader service.
            transformation_service: Transformation service.
            file_repository: File repository service for I/O operations.
        """
        self.yaml_parser = yaml_parser
        self.editor_service = editor_service
        self.heuristics = heuristics
        self.schema_upgrader = schema_upgrader
        self.transformation_service = transformation_service
        self.file_repository = file_repository

    def migrate(self, note_path: Path) -> MigrationResult:
        """Migrate a single note file.

        Args:
            note_path: Path to the markdown file.

        Returns:
            MigrationResult on success.

        Raises:
            FileReadError: If the file cannot be read.
            FrontmatterParseError: If YAML parsing fails.
            MissingFieldsError: If required fields are missing after user input.
            EditorCancelledError: If user cancels editor input.
        """
        try:
            content = self.file_repository.read_text(note_path)
        except (OSError, UnicodeDecodeError) as e:
            raise FileReadError(note_path, f"Cannot read file: {e}") from e

        # Parse YAML
        try:
            parsed = self.yaml_parser.parse(content)
        except YamlParseError as e:
            raise FrontmatterParseError(note_path, str(e)) from e

        # 2. Transform (rename fields, check version, etc.)
        frontmatter_dict, transformed = self.transformation_service.transform(
            parsed.frontmatter, note_path
        )
        frontmatter = FrontmatterSchema.model_validate(frontmatter_dict)

        # Detect type via heuristics
        detected_type = self.heuristics.detect_type(frontmatter.model_dump())
        if not frontmatter.type and detected_type:
            frontmatter.type = detected_type

        # Determine missing fields
        dump_kwargs = {"exclude_unset": False, "exclude_none": False}
        missing = self._get_missing_fields(
            frontmatter.model_dump(**dump_kwargs), detected_type, note_path
        )

        merged_frontmatter = None

        # If missing fields or no type, prompt user
        if missing or not (frontmatter.type or detected_type):
            try:
                updated_dict = self.editor_service.prompt_user(
                    original_content=content,
                    frontmatter=frontmatter.model_dump(**dump_kwargs),
                    missing_fields=missing,
                )
                # the updated_dict has all the fields, including those from 'model_config={"extra": "allow"}'
                frontmatter = FrontmatterSchema.model_validate(updated_dict)
                # Keep merged dict directly to preserve any dynamically passed fields
                # that were missing on the model validation
                merged_frontmatter = {
                    **updated_dict,
                    **frontmatter.model_dump(exclude_unset=False),
                }
                # Re-detect type after user input
                detected_type = frontmatter.type or detected_type
            except EditorAbortedError as e:
                raise EditorCancelledError(note_path, str(e)) from e

        # Final validation
        final_valid_frontmatter = (
            merged_frontmatter
            if merged_frontmatter is not None
            else frontmatter.model_dump(**dump_kwargs)
        )

        final_missing = self._get_missing_fields(
            final_valid_frontmatter,
            detected_type,
            note_path,
        )
        if final_missing:
            raise MissingFieldsError(note_path, final_missing)

        # Write migrated note (schema_upgrader handles field cleanup)
        # Returns False if skipped due to collision
        write_success = self._write_migrated_note(
            note_path, final_valid_frontmatter, parsed.body
        )

        return MigrationResult(
            file_path=note_path,
            status=MigrationStatus.SUCCESS
            if write_success
            else MigrationStatus.SKIPPED,
            detected_type=detected_type,
        )

    def _get_missing_fields(
        self,
        frontmatter: dict[str, str | int | list[str] | None],
        note_type: str | None,
        note_path: Path,  # Added note_path argument
    ) -> list[str]:
        """Determine which required fields are missing."""
        # If no type, we need it first
        if not note_type:
            return ["type"] if "type" not in frontmatter else []

        from dx_vault_atlas.core.registry import NoteModelRegistry

        # The original `note_type` argument is used here, not re-detected.
        # The `_detect_type` method and `return False` are not part of this change.
        # The `required = ["title", "type"]` line is removed as per the snippet.
        required = []  # Initialize required to an empty list
        if model_cls := NoteModelRegistry.get_model(note_type):
            required = [
                field.alias or name
                for name, field in model_cls.model_fields.items()
                if field.is_required()
            ]
        missing = []

        for field in required:
            value = frontmatter.get(field)
            # Check if field is empty/None
            # Allow empty list (e.g. aliases: []) and 0 (priority)
            if value is None or value == "":
                missing.append(field)

        # Ensure title comes first if missing (user preference for empty files)
        if "title" in missing:
            missing.remove("title")
            missing.insert(0, "title")

        return missing

    def _write_migrated_note(
        self,
        note_path: Path,
        frontmatter: dict[str, str | int | list[str] | None],
        body: str,
    ) -> bool:
        """Write the migrated note back to disk.

        Returns:
            True if written successfully, False if skipped due to collision.
        """
        # NoteMigrator.migrate performs in-place updates.
        # If the architecture changes to support moving files (source -> target),
        # an explicit `self.file_repository.target_exists(target_path)` check
        # should be added here to warn and return False.

        # Delegate schema upgrade and cleaning
        upgraded_frontmatter = self.schema_upgrader.upgrade(dict(frontmatter))

        yaml_content = self.yaml_parser.serialize_frontmatter(upgraded_frontmatter)
        self.file_repository.write_text(note_path, yaml_content + body)
        return True
