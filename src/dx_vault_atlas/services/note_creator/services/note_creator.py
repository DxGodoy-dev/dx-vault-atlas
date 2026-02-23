from typing import Any

from dx_vault_atlas.services.note_creator.models.enums import (
    NoteTemplate,
)
from dx_vault_atlas.services.note_creator.models.note import (
    BaseNote,
    MocNote,
    ProjectNote,
    RankedNote,
    TaskNote,
)


# Model mapping for final instantiation

# Model mapping for final instantiation
MODEL_MAP: dict[NoteTemplate, type[BaseNote]] = {
    NoteTemplate.PROJECT: ProjectNote,
    NoteTemplate.TASK: TaskNote,
    NoteTemplate.INFO: RankedNote,
    NoteTemplate.MOC: MocNote,
}


class NoteBuilderService:
    """Service for note construction from data."""

    @staticmethod
    def build_note(note_data: dict[str, Any]) -> BaseNote:
        """Build a note instance from data.

        Args:
            note_data: Dictionary containing note data. Must include 'template_type'.

        Returns:
            Validated note instance.
        """
        data = note_data.copy()
        template = data.pop("template_type", None)

        if not template:
            # Fallback or error if template is missing, though wizard should provide it.
            # For now, let's assume if it's not there, we might have issues or defaults.
            # But the factory logic implies we know the type.
            # If the data comes from wizard_steps, it has 'template_type'.
            raise ValueError("Missing 'template_type' in note data.")

        # Return validated instance
        note_class = MODEL_MAP.get(template, BaseNote)
        return note_class(**data)
