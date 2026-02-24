"""Factory for creating note instances from raw data."""

from pathlib import Path
from typing import Any

from dx_vault_atlas.services.note_creator.defaults import DEFAULT_TAGS
from dx_vault_atlas.services.note_creator.models.enums import NoteTemplate
from dx_vault_atlas.services.note_creator.models.note import (
    BaseNote,
    InfoNote,
    MocNote,
    ProjectNote,
    RefNote,
    TaskNote,
)

# Mapping of template enums to Pydantic models
MODEL_MAP: dict[NoteTemplate, type[BaseNote]] = {
    NoteTemplate.PROJECT: ProjectNote,
    NoteTemplate.TASK: TaskNote,
    NoteTemplate.INFO: InfoNote,
    NoteTemplate.REF: RefNote,
    NoteTemplate.MOC: MocNote,
}


class NoteFactory:
    """Factory for creating note instances."""

    @staticmethod
    def create_note(data: dict[str, Any]) -> BaseNote:
        """Create a note instance from dictionary data.

        Args:
            data: Dictionary containing note data.

        Returns:
            Instantiated Note model.
        """
        title = str(data["title"])
        # Handle template: might be string or Enum
        raw_template = data.get("template")

        # Ensure we have a valid template enum for the mapping
        template_enum: NoteTemplate
        if isinstance(raw_template, NoteTemplate):
            template_enum = raw_template
        elif isinstance(raw_template, str):
            try:
                # Try to map string to enum if possible, or iterate
                # This assumes raw_template matches value or name
                # Simple approach: existing logic handled it loosely.
                # Let's rely on what main.py did: it assumed it was valid.
                # However, for MODEL_MAP lookups we need the Enum or careful handling.
                # If it's a string like "template.md", we might need logic.
                # But typically the wizard returns an Enum.
                # Let's try to pass it as is if it fails.
                template_enum = NoteTemplate(raw_template)
            except ValueError:
                # Fallback if it's not a direct value match
                # logic in main.py defaults to BaseNote if string
                # We will try to be robust.
                template_enum = None  # type: ignore
        else:
            template_enum = None  # type: ignore

        # Logic from main.py: Path(str(template)).stem
        type_str = (
            Path(str(raw_template)).stem
            if isinstance(raw_template, str)
            else Path(raw_template.value).stem
        )

        escaped_title = title.replace('"', '\\"')

        note_data: dict[str, Any] = {
            "title": f'"{escaped_title}"',
            "aliases": [title],
            "tags": DEFAULT_TAGS,
            "type": type_str,
        }

        # Optional fields
        if source := data.get("source"):
            note_data["source"] = source
        if priority := data.get("priority"):
            note_data["priority"] = priority
        if area := data.get("area"):
            note_data["area"] = area
        if status := data.get("status"):
            note_data["status"] = status

        # Instantiate
        note_class = MODEL_MAP.get(template_enum, BaseNote)
        return note_class(**note_data)
