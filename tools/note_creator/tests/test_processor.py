"""Tests for NoteProcessor."""
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from note_creator.core.processor import NoteProcessor
from note_creator.models.note import BaseNote
from note_creator.models.enums import NoteSource, Priority
from note_creator.datetime import datetime


@pytest.fixture
def mock_templating():
    """Templating service that returns fixed content."""
    svc = MagicMock()
    svc.render.return_value = "---\ntitle: Test\n---\n"
    return svc


@pytest.fixture
def sample_note():
    """Sample BaseNote for tests."""
    return BaseNote(
        title="Test Note",
        date=datetime.now(),
        source=NoteSource.GEMINI,
        tags=["test"],
        priority=Priority.MEDIUM,
    )


@pytest.fixture
def note_processor(mock_templating):
    """NoteProcessor with mocked templating."""
    with patch("src.core.processor.ProjectPaths.ensure_dirs"):
        yield NoteProcessor(mock_templating)


def test_create_note_renders_and_writes(note_processor, sample_note, mock_templating, tmp_path):
    """create_note calls render, writes file, and opens editor (mocked)."""
    output_path = tmp_path / "_Test_Note.md"
    with patch("src.core.processor.TextEditor.open_file"):
        note_processor.create_note("info.md", sample_note, output_path)

    mock_templating.render.assert_called_once_with("info.md", sample_note)
    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == "---\ntitle: Test\n---\n"


def test_create_note_raises_if_file_exists(note_processor, sample_note, tmp_path):
    """create_note raises FileExistsError when output path already exists."""
    output_path = tmp_path / "_Existing.md"
    output_path.write_text("existing", encoding="utf-8")

    with patch("src.core.processor.TextEditor.open_file"):
        with pytest.raises(FileExistsError, match="ya existe"):
            note_processor.create_note("info.md", sample_note, output_path)


def test_write_to_disk_raises_if_exists(note_processor, tmp_path):
    """_write_to_disk raises FileExistsError when path exists."""
    path = tmp_path / "exists.md"
    path.write_text("x", encoding="utf-8")

    with pytest.raises(FileExistsError):
        note_processor._write_to_disk("content", path)


def test_write_to_disk_writes_content(note_processor, tmp_path):
    """_write_to_disk writes content to new file."""
    path = tmp_path / "new.md"
    content = "---\nfrontmatter\n---\nbody"

    note_processor._write_to_disk(content, path)

    assert path.exists()
    assert path.read_text(encoding="utf-8") == content
