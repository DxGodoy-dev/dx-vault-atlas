"""Note processor for rendering and writing notes."""

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

    def render_note(
        self,
        template_name: str,
        note_data: BaseNote,
        body_content: str = "",
    ) -> str:
        """Render note content from template and variables.

        Args:
            template_name: Template file name.
            note_data: Validated note data.
            body_content: Optional body content to append.

        Returns:
            The rendered note content as a string.
        """
        content = self.templating.render(template_name, note_data)
        if body_content:
            content = f"{content.strip()}\n\n{body_content.strip()}\n"

        return content
