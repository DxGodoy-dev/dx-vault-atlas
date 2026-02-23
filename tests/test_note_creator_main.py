"""Tests for note creator factory."""

from dx_vault_atlas.services.note_creator.core.factory import NoteFactory
from dx_vault_atlas.services.note_creator.models.enums import (
    NoteArea,
    NoteSource,
    NoteTemplate,
    Priority,
)
from dx_vault_atlas.services.note_creator.models.note import (
    BaseNote,
    ProjectNote,
    RankedNote,
)


class TestNoteFactory:
    """Tests for NoteFactory."""

    def test_create_info_note(self) -> None:
        """Should create RankedNote for INFO template."""
        data = {
            "title": "My Note",
            "template": NoteTemplate.INFO,
            "source": NoteSource.ME,
            "priority": Priority.MEDIUM,
        }

        note = NoteFactory.create_note(data)

        assert isinstance(note, RankedNote)
        assert note.title == '"My Note"'
        assert note.note_type == "info"
        assert note.source == NoteSource.ME.value
        assert note.priority == Priority.MEDIUM.value
        assert note.status == "to read"

    def test_create_project_note(self) -> None:
        """Should create ProjectNote for PROJECT template."""
        data = {
            "title": "My Project",
            "template": NoteTemplate.PROJECT,
            "source": NoteSource.ME,
            "priority": Priority.HIGH,
            "area": NoteArea.WORK,
        }

        note = NoteFactory.create_note(data)

        assert isinstance(note, ProjectNote)
        assert note.area == NoteArea.WORK.value
        assert note.status == "to do"

    def test_handles_string_template_fallback(self) -> None:
        """Should handle string template gracefully."""
        data = {
            "title": "Fallback Note",
            "template": "some_custom_template.md",
        }

        note = NoteFactory.create_note(data)

        # Should be BaseNote (default fallback)
        assert isinstance(note, BaseNote)
        assert note.title == '"Fallback Note"'
        # Factory extracts stem from path string
        assert note.note_type == "some_custom_template"
