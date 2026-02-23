"""Note Migrator application orchestrator."""

from pathlib import Path
from typing import Any

from dx_vault_atlas.services.note_migrator.core.transformation_service import (
    TransformationService,
)
from dx_vault_atlas.services.note_migrator.services.yaml_parser import (
    YamlParseError,
    YamlParserService,
)
from dx_vault_atlas.shared import console as ui
from dx_vault_atlas.shared.config import GlobalConfig
from dx_vault_atlas.shared.core.scanner import VaultScanner
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

    def __init__(self, settings: GlobalConfig) -> None:
        """Initialize with dependencies."""
        self.settings = settings
        self.scanner = VaultScanner()
        self.yaml_parser = YamlParserService()
        self.transformer = TransformationService(settings)

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
        ui.show_header("Note Migrator")

        # Backup confirmation
        ui.console.print(f"[bold]Vault path:[/bold] {self.settings.vault_path}")
        if not ui.confirm("\n[?] Have you backed up your vault?", default=False):
            ui.warning_message("Aborting: Backup not confirmed.")
            return

        # Scan vault
        all_notes = list(self.scanner.scan(self.settings.vault_path))
        ui.console.print(f"\n[bold]Scanning {len(all_notes)} notes...[/bold]")
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
        ui.console.print("\n[bold]Migration Summary:[/bold]")
        ui.console.print(f"[green]✓[/green] {migrated_count} notes updated")
        ui.console.print(
            f"[dim]•[/dim] {skipped_count} notes skipped (no changes needed)"
        )
        if error_count > 0:
            ui.console.print(f"[red]✗[/red] {error_count} errors")

        ui.console.print("\n[bold]Migration complete.[/bold]")

    def _migrate_note_if_needed(
        self, file_path: Path, rename_only: bool, debug_mode: bool
    ) -> bool:
        """Check if note needs migration and apply it.

        Returns:
            True if migrated, False if skipped.
        """
        try:
            content = file_path.read_text(encoding="utf-8")
        except OSError:
            logger.warning(f"Could not read {file_path}")
            return False

        try:
            parsed = self.yaml_parser.parse(content)
        except YamlParseError:
            if debug_mode:
                logger.debug(
                    f"Skipping {file_path.name}: Frontmatter parse error or missing"
                )
            return False

        if not parsed.has_yaml:
            if debug_mode:
                logger.debug(f"Skipping {file_path.name}: No YAML frontmatter found")
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

    def _write_note(
        self, file_path: Path, frontmatter: dict[str, Any], body: str
    ) -> None:
        """Write note details."""
        yaml_content = self.yaml_parser.serialize_frontmatter(frontmatter)
        file_path.write_text(yaml_content + body, encoding="utf-8")
        logger.info(f"Updated {file_path.name}")


def create_app(settings: GlobalConfig) -> MigratorApp:
    """Factory function to create MigratorApp."""
    return MigratorApp(settings)
