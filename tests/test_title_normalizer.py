"""Tests for TitleNormalizer."""

import re

import pytest

from dx_vault_atlas.services.note_creator.utils.title_normalizer import TitleNormalizer


class TestTitleNormalizer:
    """Tests for TitleNormalizer utility."""

    def test_normalize_empty_title_raises_error(self) -> None:
        """Empty title should raise ValueError."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            TitleNormalizer.normalize("")

        with pytest.raises(ValueError, match="Title cannot be empty"):
            TitleNormalizer.normalize("   ")

    def test_normalize_sanitizes_string(self) -> None:
        """Special characters should be removed/replaced."""
        # We need to mock datetime to check timestamp, or just check format
        # Let's check format: YYYYMMDDHHMMSS_sanitized_name

        result = TitleNormalizer.normalize("My Note Title!")
        assert re.match(r"^\d{14}_my_note_title$", result)

    def test_sanitize_removes_accents(self) -> None:
        """Accents should be removed (e.g. é -> e)."""
        result = TitleNormalizer._sanitize("Créme Brûlée")
        assert result == "creme_brulee"

    def test_sanitize_removes_special_chars(self) -> None:
        """Non-alphanumeric chars should be replaced by underscores."""
        result = TitleNormalizer._sanitize("hello@world#python")
        assert result == "hello_world_python"

    def test_sanitize_trims_underscores(self) -> None:
        """Leading/trailing underscores should be removed."""
        result = TitleNormalizer._sanitize("  hello world  ")
        assert result == "hello_world"

        result = TitleNormalizer._sanitize("__hello__")
        assert result == "hello"
