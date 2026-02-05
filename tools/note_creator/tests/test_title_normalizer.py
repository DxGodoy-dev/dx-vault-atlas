"""Tests for TitleNormalizer."""
import pytest

from note_creator.utils.title_normalizer import TitleNormalizer


def test_to_obsidian_snake_case_basic():
    """Normal title becomes _Title_With_Underscores."""
    assert TitleNormalizer.to_obsidian_snake_case("My Note Title") == "_My_Note_Title"


def test_to_obsidian_snake_case_strips_accents():
    """Accents are stripped."""
    assert TitleNormalizer.to_obsidian_snake_case("Café") == "_Cafe"
    assert TitleNormalizer.to_obsidian_snake_case("Niño") == "_Nino"


def test_to_obsidian_snake_case_hyphens_to_underscores():
    """Hyphens and spaces become underscores."""
    assert TitleNormalizer.to_obsidian_snake_case("hello-world") == "_hello_world"
    assert TitleNormalizer.to_obsidian_snake_case("a b c") == "_a_b_c"


def test_to_obsidian_snake_case_removes_special_chars():
    """Non-alphanumeric chars (except underscore) are removed."""
    result = TitleNormalizer.to_obsidian_snake_case("Hello! World?")
    assert result == "_Hello_World"


def test_to_obsidian_snake_case_empty_raises():
    """Empty or whitespace-only input raises ValueError."""
    with pytest.raises(ValueError, match="Title cannot be empty"):
        TitleNormalizer.to_obsidian_snake_case("")
    with pytest.raises(ValueError, match="Title cannot be empty"):
        TitleNormalizer.to_obsidian_snake_case("   ")


def test_to_obsidian_snake_case_single_word():
    """Single word gets leading underscore."""
    assert TitleNormalizer.to_obsidian_snake_case("Note") == "_Note"
