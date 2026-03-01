"""Tests for NoteProcessor."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from dx_vault_atlas.services.note_creator.core.processor import NoteProcessor
from dx_vault_atlas.services.note_creator.models.enums import (
    Priority,
)
from dx_vault_atlas.services.note_creator.models.note import BaseNote, RankedNote
from dx_vault_atlas.services.note_creator.services.templating import TemplatingService


class TestNoteProcessor:
    """Tests for NoteProcessor."""

    @pytest.fixture
    def mock_templating(self) -> MagicMock:
        """Mock templating service."""
        service = MagicMock(spec=TemplatingService)
        service.render.return_value = "Run mocked content"
        return service

    @pytest.fixture
    def processor(self, mock_templating: MagicMock) -> NoteProcessor:
        """Create processor instance."""
        return NoteProcessor(mock_templating)

    @pytest.fixture
    def sample_note(self) -> BaseNote:
        """Create sample note data."""
        return RankedNote(
            title="Test Note",
            aliases=["Alias"],
            note_type="Ranked",  # Pydantic alias for 'type'
            source="Book",
            priority=Priority.HIGH,
        )

    def test_render_note(self, processor: NoteProcessor, sample_note: BaseNote) -> None:
        """Should render template and return content."""
        content = processor.render_note("info.md", sample_note)
        assert "Run mocked content" in content
        processor.templating.render.assert_called_once_with("info.md", sample_note)

    def test_render_note_with_body(
        self, processor: NoteProcessor, sample_note: BaseNote
    ) -> None:
        """Should render template and append body."""
        content = processor.render_note("info.md", sample_note, "body text")
        assert "Run mocked content" in content
        assert "body text" in content
