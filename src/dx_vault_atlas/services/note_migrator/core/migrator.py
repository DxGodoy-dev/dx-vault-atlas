"""Note migrator orchestrator."""

from pathlib import Path


from dx_vault_atlas.services.note_creator.models.enums import (
    NoteArea,
    NoteSource,
    NoteStatus,
    Priority,
)
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

    # Required fields per note type (matching note_creator behavior)
    REQUIRED_FIELDS: dict[str, list[str]] = {
        "moc": ["title", "aliases", "type"],
        "info": ["title", "aliases", "type", "source", "priority"],
        "task": ["title", "aliases", "type", "source", "priority", "area"],
        "project": ["title", "aliases", "type", "source", "priority", "area"],
    }

    # Default values for fields that note_creator provides defaults for
    DEFAULT_VALUES: dict[str, str | int | list[str]] = {
        "source": NoteSource.OTHER.value,
        "priority": Priority.LOW.value,
        "area": NoteArea.PERSONAL.value,
        "status": NoteStatus.TO_DO.value,
        "tags": [],
    }

    def __init__(self, editor: str = "vim") -> None:
        """Initialize migrator with services.

        Args:
            editor: System editor command for manual input.
        """
        self.yaml_parser = YamlParserService()
        self.editor_service = EditorBufferService(editor=editor)
        self.heuristics = TypeHeuristics()
        self.schema_upgrader = SchemaUpgrader()
        self.transformation_service = TransformationService(settings=get_settings())

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
        except OSError as e:
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

        # Apply defaults and write
        final_dict = self._apply_defaults(frontmatter.model_dump())
        self._write_migrated_note(note_path, final_dict, parsed.body)

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

        required = self.REQUIRED_FIELDS.get(note_type, ["title", "aliases", "type"])
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

    def _apply_defaults(
        self, frontmatter: dict[str, str | int | list[str] | None]
    ) -> dict[str, str | int | list[str] | None]:
        """Apply default values for optional fields."""
        result = dict(frontmatter)

        for field, default in self.DEFAULT_VALUES.items():
            if field not in result:
                result[field] = default

        return result

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
