"""Tests for TemplatingService."""
from datetime import datetime

from note_creator.services.templating import TemplatingService
from note_creator.models.note import BaseNote
from note_creator.models.enums import NoteSource, Priority


def test_render_info_template():
    """render produces markdown with frontmatter from BaseNote."""
    service = TemplatingService()
    note = BaseNote(
        title="Test",
        date=datetime(2025, 2, 1),
        source=NoteSource.GEMINI,
        tags=["a", "b"],
        priority=Priority.MEDIUM,
    )
    result = service.render("info.md", note)

    assert "tags" in result
    assert "2025-02-01" in result
    assert "GEMINI" in result or "gemini" in result  # source enum
    assert "a" in result and "b" in result


def test_render_single_tag_becomes_list():
    """Note with single string tag is normalized to list and rendered."""
    service = TemplatingService()
    note = BaseNote(title="T", tags="single")
    result = service.render("info.md", note)
    assert "single" in result
