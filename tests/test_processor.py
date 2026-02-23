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

    def test_create_note_writes_file(
        self, processor: NoteProcessor, sample_note: BaseNote, tmp_path: Path
    ) -> None:
        """Should render template and write to file."""
        output_path = tmp_path / "test_note.md"

        result = processor.create_note("info.md", sample_note, output_path)

        assert result == output_path
        assert output_path.exists()
        assert output_path.read_text(encoding="utf-8") == "Run mocked content"

        # Verify template service called correctly
        processor.templating.render.assert_called_once_with("info.md", sample_note)

    def test_create_note_raises_if_exists(
        self, processor: NoteProcessor, sample_note: BaseNote, tmp_path: Path
    ) -> None:
        """Should raise FileExistsError if file exists."""
        output_path = tmp_path / "test_note.md"
        output_path.write_text("existing content")

        with pytest.raises(FileExistsError):
            processor.create_note("info.md", sample_note, output_path)
