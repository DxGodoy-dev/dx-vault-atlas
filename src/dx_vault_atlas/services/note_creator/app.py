"""Note Creator application orchestrator."""

import tempfile
from contextlib import suppress
from pathlib import Path

from dx_vault_atlas.services.note_creator.core.factory import NoteFactory
from dx_vault_atlas.services.note_creator.core.processor import NoteProcessor
from dx_vault_atlas.services.note_creator.services.templating import TemplatingService
from dx_vault_atlas.services.note_creator.tui import run_tui
from dx_vault_atlas.services.note_creator.utils.title_normalizer import TitleNormalizer
from dx_vault_atlas.shared.config import GlobalConfig
from dx_vault_atlas.shared.core.system_editor import SystemEditor
from dx_vault_atlas.shared.logger import logger
from dx_vault_atlas.shared.tui.result_app import run_result_tui


class NoteCreatorApp:
    """Orchestrates the note creation workflow.

    Responsibilities:
    - Run interactive wizard to gather note data
    - Open external editor for content
    - Create note file with proper template
    - Handle retry/quit loop
    """

    def __init__(
        self,
        settings: GlobalConfig,
        processor: NoteProcessor,
        show_header: bool = True,
    ) -> None:
        """Initialize with dependencies.

        Args:
            settings: Application configuration.
            processor: Note processor service.
            show_header: Whether to show header panel.
        """
        self.settings = settings
        self.processor = processor
        self.show_header = show_header

    def run(self) -> None:
        """Execute the note creation workflow."""
        logger.info("Starting note creator")

        while True:
            # 1. Wizard TUI
            # Returns dict with collected data or None if cancelled
            wizard_data = run_tui(self.settings)

            if not wizard_data:
                # User cancelled or quit
                return

            # 2. Editor (External Process)
            # Opens default editor for body content
            body_content = self._get_editor_content()

            # 3. Create Note
            try:
                title = str(wizard_data["title"])
                safe_title = TitleNormalizer.normalize(title)
                output_path = self.settings.vault_inbox / f"{safe_title}.md"

                note_instance = NoteFactory.create_note(wizard_data)

                logger.info(f"Creating note: {safe_title}")
                self.processor.create_note(
                    template_name=f"{note_instance.note_type}.md",
                    note_data=note_instance,
                    output_path=output_path,
                    body_content=body_content,
                )
                logger.info(f"Note created at {output_path}")

                note_path = output_path
            except Exception as e:
                logger.exception(f"Error creating note: {e}")

                # Show error to user via console
                from dx_vault_atlas.services.note_creator.services.console import (
                    console,
                )

                console.print(f"[bold red]Error creating note:[/bold red] {e}")

                # Give user a chance to read the error before returning
                from rich.prompt import Prompt

                Prompt.ask("\n[dim]Press Enter to return to main menu...[/dim]")

                return

            # 4. Result TUI
            # Shows success and asks for Retry/Quit
            action = run_result_tui(note_path)

            if action != "retry":
                break

    def _get_editor_content(self) -> str:
        """Open temporary file in editor and return content."""
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as tf:
            temp_path = tf.name

        try:
            # Open editor (blocks until closed)
            SystemEditor.open_file(temp_path)

            # Read content
            return Path(temp_path).read_text(encoding="utf-8")
        finally:
            # Cleanup
            with suppress(OSError):
                Path(temp_path).unlink()


def create_app(settings: GlobalConfig, show_header: bool = True) -> NoteCreatorApp:
    """Factory function to create NoteCreatorApp with dependencies.

    Args:
        settings: Application configuration.
        show_header: Whether to show header panel.

    Returns:
        Configured NoteCreatorApp instance.
    """
    template_service = TemplatingService()
    processor = NoteProcessor(template_service)
    return NoteCreatorApp(settings, processor, show_header)
