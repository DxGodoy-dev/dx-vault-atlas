"""Note Migrator application orchestrator."""

from pathlib import Path
from typing import Any

from dx_vault_atlas.services.note_migrator.core.interfaces import (
    IScanner,
    ITransformer,
    IUserInterface,
    IYamlParser,
)
from dx_vault_atlas.services.note_migrator.services.file_repository import (
    FileRepository,
)
from dx_vault_atlas.services.note_migrator.services.yaml_parser import (
    ParsedYaml,
    YamlParseError,
)
from dx_vault_atlas.shared.config import GlobalConfig
from dx_vault_atlas.shared.logger import logger


class MigratorApp:
    """Orchestrates the note migration workflow.

    Responsibilities:
    - Scan vault for markdown files
    - Apply dynamic field renaming (configured in settings)
    - Check for schema updates (version mismatch, legacy fields)
    - Apply schema transformations automatically
    - Mappings: date -> created
    - Add default values for new required schema fields
    - Remove obsolete fields
    - Enforce field ordering
    """

    def __init__(
        self,
        settings: GlobalConfig,
        scanner: IScanner,
        yaml_parser: IYamlParser,
        transformer: ITransformer,
        ui: IUserInterface,
        file_repo: FileRepository,
    ) -> None:
        """Initialize with dependencies."""
        self.settings = settings
        self.scanner = scanner
        self.yaml_parser = yaml_parser
        self.transformer = transformer
        self.ui = ui
        self.file_repo = file_repo

    def run(self, rename_only: bool = False, debug_mode: bool = False) -> None:
        """Execute the migration workflow.

        Args:
            rename_only: If True, only rename fields based on config map.
            debug_mode: If True, enable verbose logging.
        """
        mode_str = "(rename only)" if rename_only else "(full migration)"
        if debug_mode:
            logger.debug(f"Migrator starting in DEBUG MODE {mode_str}")

        logger.info(f"Starting note migrator {mode_str}")
        self.ui.show_header("Note Migrator")

        # Backup confirmation
        self.ui.display_message(f"[bold]Vault path:[/bold] {self.settings.vault_path}")
        if not self.ui.confirm("\n[?] Have you backed up your vault?"):
            self.ui.display_message("[yellow]Aborting: Backup not confirmed.[/yellow]")
            return

        # Scan vault
        all_notes = list(self.scanner.scan(self.settings.vault_path))
        self.ui.display_message(f"\n[bold]Scanning {len(all_notes)} notes...[/bold]")
        if debug_mode:
            logger.debug(f"Found {len(all_notes)} notes to migrate")

        migrated_count = 0
        error_count = 0
        skipped_count = 0

        for note_path in all_notes:
            try:
                if self._migrate_note_if_needed(note_path, rename_only, debug_mode):
                    migrated_count += 1
                else:
                    skipped_count += 1
            except Exception as e:
                logger.error(f"Failed to migrate {note_path.name}: {e}")
                error_count += 1

        # Report summary
        summary_data = {
            "notes updated": migrated_count,
            "notes skipped (no changes needed)": skipped_count,
        }
        if error_count > 0:
            summary_data["errors"] = error_count

        self.ui.print_summary(summary_data)
        self.ui.display_message("\n[bold]Migration complete.[/bold]")

    def _migrate_note_if_needed(
        self, file_path: Path, rename_only: bool, debug_mode: bool
    ) -> bool:
        """Check if note needs migration and apply it.

        Returns:
            True if migrated, False if skipped.
        """
        parsed = self._read_and_parse_note(file_path, debug_mode)
        if not parsed:
            return False

        # Transform
        new_frontmatter, has_changes = self.transformer.transform(
            parsed.frontmatter, file_path, rename_only, debug_mode
        )

        if has_changes:
            if debug_mode:
                logger.debug(f"Applying changes to {file_path.name}")
            self._write_note(file_path, new_frontmatter, parsed.body)
            return True

        if debug_mode:
            logger.debug(f"No changes needed for {file_path.name}")

        return False

    def _read_and_parse_note(
        self, file_path: Path, debug_mode: bool
    ) -> ParsedYaml | None:
        """Read and parse note content, handling errors."""
        try:
            content = self.file_repo.read_text(file_path)
        except OSError:
            logger.warning(f"Could not read {file_path}")
            return None

        try:
            parsed = self.yaml_parser.parse(content)
        except YamlParseError:
            if debug_mode:
                logger.debug(
                    f"Skipping {file_path.name}: Frontmatter parse error or missing"
                )
            return None

        if not parsed.has_yaml:
            if debug_mode:
                logger.debug(f"Skipping {file_path.name}: No YAML frontmatter found")
            return None

        return parsed

    def _write_note(
        self, file_path: Path, frontmatter: dict[str, Any], body: str
    ) -> None:
        """Write note details."""
        yaml_content = self.yaml_parser.serialize_frontmatter(frontmatter)
        self.file_repo.write_text(file_path, yaml_content + body)
        logger.info(f"Updated {file_path.name}")


def create_app(settings: GlobalConfig) -> MigratorApp:
    """Factory function to create MigratorApp and inject dependencies."""
    # Ensure models are registered in NoteModelRegistry
    import dx_vault_atlas.services.note_creator.models.note  # noqa: F401
    from dx_vault_atlas.services.note_migrator.core.transformation_service import (
        TransformationService,
    )
    from dx_vault_atlas.services.note_migrator.services.file_repository import (
        LocalFileRepository,
    )
    from dx_vault_atlas.services.note_migrator.services.ui_service import (
        CliUserInterface,
    )
    from dx_vault_atlas.services.note_migrator.services.yaml_parser import (
        YamlParserService,
    )
    from dx_vault_atlas.shared.core.scanner import VaultScanner

    scanner = VaultScanner()
    yaml_parser = YamlParserService()
    transformer = TransformationService(settings)
    ui = CliUserInterface()
    file_repo = LocalFileRepository()

    return MigratorApp(
        settings=settings,
        scanner=scanner,
        yaml_parser=yaml_parser,
        transformer=transformer,
        ui=ui,
        file_repo=file_repo,
    )
