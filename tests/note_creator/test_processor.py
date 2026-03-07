"""Tests for NoteProcessor."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from dx_vault_atlas.services.note_creator.core.processor import NoteProcessor
from dx_vault_atlas.shared.models.enums import (
    Priority,
)
from dx_vault_atlas.shared.models.note import BaseNote, InfoNote
from dx_vault_atlas.services.note_creator.services.templating import TemplatingService


class TestNoteProcessor:
    """Tests for NoteProcessor."""

    @pytest.fixture
    def test_templating(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> TemplatingService:
        """Create a real TemplatingService loaded from tmp_path."""
        import dx_vault_atlas.services.note_creator.services.templating as templating_mod

        monkeypatch.setattr(templating_mod, "TEMPLATES_DIR", tmp_path)

        # Create a dummy template
        template_file = tmp_path / "info.md"
        template_file.write_text(
            "Hello {{ title }}\nType: {{ type }}\n", encoding="utf-8"
        )

        return TemplatingService()

    @pytest.fixture
    def processor(self, test_templating: TemplatingService) -> NoteProcessor:
        """Create processor instance."""
        return NoteProcessor(test_templating)

    @pytest.fixture
    def sample_note(self) -> BaseNote:
        """Create sample note data."""
        return InfoNote(
            title="Test Note",
            aliases=["Alias"],
            note_type="info",  # Pydantic alias for 'type'
            priority=Priority.HIGH,
        )

    def test_render_note(self, processor: NoteProcessor, sample_note: BaseNote) -> None:
        """Should render real template and return content."""
        content = processor.render_note("info.md", sample_note)
        assert "Hello Test Note" in content
        assert "Type: info" in content

    def test_render_note_with_body(
        self, processor: NoteProcessor, sample_note: BaseNote
    ) -> None:
        """Should render real template and append body."""
        content = processor.render_note("info.md", sample_note, "body text")
        assert "Hello Test Note" in content
        assert "body text" in content
