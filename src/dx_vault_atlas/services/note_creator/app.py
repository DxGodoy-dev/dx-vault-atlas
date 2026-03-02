"""Note Creator application orchestrator."""

from pathlib import Path

from dx_vault_atlas.services.note_creator.core.factory import NoteFactory
from dx_vault_atlas.services.note_creator.core.ports import (
    INoteProcessor,
    INoteWriter,
    IOutputPresenter,
)
from dx_vault_atlas.services.note_creator.core.processor import NoteProcessor
from dx_vault_atlas.services.note_creator.core.writer import NoteWriter
from dx_vault_atlas.services.note_creator.services.editor import EditorService
from dx_vault_atlas.services.note_creator.services.templating import TemplatingService
from dx_vault_atlas.services.note_creator.tui import run_tui
from dx_vault_atlas.services.note_creator.utils.title_normalizer import TitleNormalizer
from dx_vault_atlas.shared.config import GlobalConfig
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
        vault_inbox: Path,
        processor: INoteProcessor,
        writer: INoteWriter,
        editor: EditorService,
        error_presenter: IOutputPresenter,
        show_header: bool = True,
    ) -> None:
        """Initialize with dependencies.

        Args:
            vault_inbox: Directory where new notes will be created.
            processor: Note processor service.
            writer: Service to write notes to disk.
            editor: Service to handle external editor interactions.
            error_presenter: Service to handle error UI presentation.
            show_header: Whether to show header panel.
        """
        self.vault_inbox = vault_inbox
        self.processor = processor
        self.writer = writer
        self.editor = editor
        self.error_presenter = error_presenter
        self.show_header = show_header

    def run(self) -> None:
        """Execute the note creation workflow."""
        logger.info("Starting note creator")

        while True:
            # 1. Wizard TUI
            # Returns dict with collected data or None if cancelled
            wizard_data = run_tui()

            if not wizard_data:
                # User cancelled or quit
                return

            # 2. Editor (External Process)
            # Opens default editor for body content
            body_content = self.editor.get_editor_content()

            # 3. Create Note
            try:
                title = str(wizard_data["title"])
                safe_title = TitleNormalizer.normalize(title)
                output_path = self.vault_inbox / f"{safe_title}.md"

                note_instance = NoteFactory.create_note(wizard_data)

                logger.info(f"Creating note: {safe_title}")
                rendered_content = self.processor.render_note(
                    template_name=f"{note_instance.note_type}.md",
                    note_data=note_instance,
                    body_content=body_content,
                )
                self.writer.write(rendered_content, output_path)
                logger.info(f"Note created at {output_path}")

                note_path = output_path
            except Exception as e:
                logger.exception(f"Error creating note: {e}")

                # Show error to user via injected presenter
                self.error_presenter.present_error(e)

                return

            # 4. Result TUI
            # Shows success and asks for Retry/Quit
            action = run_result_tui(note_path)

            if action != "retry":
                break


class DefaultErrorPresenter:
    """Default error presentation using rich console."""

    def present_error(self, error: Exception) -> None:
        """Display an error to the user."""
        from rich.prompt import Prompt

        from dx_vault_atlas.services.note_creator.services.console import console

        console.print(f"[bold red]Error creating note:[/bold red] {error}")
        Prompt.ask("\n[dim]Press Enter to return to main menu...[/dim]")


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
    writer = NoteWriter()
    editor = EditorService()
    return NoteCreatorApp(
        vault_inbox=settings.vault_inbox,
        processor=processor,
        writer=writer,
        editor=editor,
        error_presenter=DefaultErrorPresenter(),
        show_header=show_header,
    )
