"""Note migrator orchestrator."""

from pathlib import Path


from dx_vault_atlas.shared.config import get_settings
from dx_vault_atlas.services.note_migrator.core.errors import (
    EditorCancelledError,
    FileReadError,
    FrontmatterParseError,
    MissingFieldsError,
)
from dx_vault_atlas.services.note_migrator.core.heuristics import TypeHeuristics
from dx_vault_atlas.services.note_migrator.models.frontmatter import FrontmatterSchema
from dx_vault_atlas.services.note_migrator.models.migration import (
    MigrationResult,
    MigrationStatus,
)
from dx_vault_atlas.services.note_migrator.services.editor_buffer import (
    EditorAbortedError,
    EditorBufferService,
)
from dx_vault_atlas.services.note_migrator.services.yaml_parser import (
    YamlParseError,
    YamlParserService,
)


from dx_vault_atlas.services.note_migrator.core.schema_upgrader import SchemaUpgrader
from dx_vault_atlas.services.note_migrator.core.transformation_service import (
    TransformationService,
)


class NoteMigrator:
    """Orchestrates the migration of a single note.

    Handles parsing, type detection, user prompts for missing fields,
    validation, and writing the migrated note.
    """

    # Empty fields, schema enforced dynamically.

    def __init__(
        self,
        editor: str = "vim",
        yaml_parser: YamlParserService | None = None,
        editor_service: EditorBufferService | None = None,
        heuristics: TypeHeuristics | None = None,
        schema_upgrader: SchemaUpgrader | None = None,
        transformation_service: TransformationService | None = None,
    ) -> None:
        """Initialize migrator with services.

        Args:
            editor: System editor command for manual input.
            yaml_parser: Optional injected service.
            editor_service: Optional injected service.
            heuristics: Optional injected service.
            schema_upgrader: Optional injected service.
            transformation_service: Optional injected service.
        """
        self.yaml_parser = yaml_parser or YamlParserService()
        self.editor_service = editor_service or EditorBufferService(editor=editor)
        self.heuristics = heuristics or TypeHeuristics()
        self.schema_upgrader = schema_upgrader or SchemaUpgrader()
        self.transformation_service = transformation_service or TransformationService(
            settings=get_settings()
        )

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
            content = note_path.read_text(encoding="utf-8")
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
        missing = self._get_missing_fields(frontmatter.model_dump(), detected_type)

        # If missing fields or no type, prompt user
        if missing or not (frontmatter.type or detected_type):
            try:
                updated_dict = self.editor_service.prompt_user(
                    original_content=content,
                    frontmatter=frontmatter.model_dump(),
                    missing_fields=missing,
                )
                frontmatter = FrontmatterSchema.model_validate(updated_dict)
                # Re-detect type after user input
                detected_type = frontmatter.type or detected_type
            except EditorAbortedError as e:
                raise EditorCancelledError(note_path, str(e)) from e

        # Final validation
        final_missing = self._get_missing_fields(
            frontmatter.model_dump(), detected_type
        )
        if final_missing:
            raise MissingFieldsError(note_path, final_missing)

        # Write migrated note (schema_upgrader handles field cleanup)
        self._write_migrated_note(note_path, frontmatter.model_dump(), parsed.body)

        return MigrationResult(
            file_path=note_path,
            status=MigrationStatus.SUCCESS,
            detected_type=detected_type,
        )

    def _get_missing_fields(
        self,
        frontmatter: dict[str, str | int | list[str] | None],
        note_type: str | None,
    ) -> list[str]:
        """Determine which required fields are missing."""
        # If no type, we need it first
        if not note_type:
            return ["type"] if "type" not in frontmatter else []

        from dx_vault_atlas.services.note_migrator.validator import MODEL_MAP

        required = ["title", "type"]
        if model_cls := MODEL_MAP.get(note_type):
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
    ) -> None:
        """Write the migrated note back to disk."""
        # Delegate schema upgrade and cleaning
        upgraded_frontmatter = self.schema_upgrader.upgrade(dict(frontmatter))

        yaml_content = self.yaml_parser.serialize_frontmatter(upgraded_frontmatter)
        note_path.write_text(yaml_content + body, encoding="utf-8")
