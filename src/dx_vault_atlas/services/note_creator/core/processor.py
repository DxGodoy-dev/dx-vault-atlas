"""Note processor for rendering and writing notes."""

from pathlib import Path

from dx_vault_atlas.services.note_creator.models.note import BaseNote
from dx_vault_atlas.services.note_creator.services.templating import TemplatingService


class NoteProcessor:
    """Processes notes by rendering templates and writing to disk."""

    def __init__(self, templating_service: TemplatingService) -> None:
        """Initialize with templating service.

        Args:
            templating_service: Service for template rendering.
        """
        self.templating = templating_service

    def create_note(
        self,
        template_name: str,
        note_data: BaseNote,
        output_path: Path,
        body_content: str = "",
    ) -> Path:
        """Render note and write to disk.

        Args:
            template_name: Template file name.
            note_data: Validated note data.
            output_path: Path to write the note.
            body_content: Optional body content to append.

        Returns:
            Path to the created note.

        Raises:
            FileExistsError: If note already exists at path.
        """
        content = self.templating.render(template_name, note_data)
        if body_content:
            content = f"{content.strip()}\n\n{body_content.strip()}\n"

        self._write_to_disk(content, output_path)
        return output_path

    def _write_to_disk(self, content: str, path: Path) -> None:
        """Write content to disk.

        Args:
            content: Note content.
            path: Target path.

        Raises:
            FileExistsError: If file already exists.
        """
        if path.exists():
            msg = f"Note already exists at: {path}"
            raise FileExistsError(msg)
        path.write_text(content, encoding="utf-8")
