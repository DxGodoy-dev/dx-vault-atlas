"""Tests for TitleNormalizer."""

import re

import pytest

from dx_vault_atlas.shared.utils.title_normalizer import TitleNormalizer


class TestTitleNormalizer:
    """Tests for TitleNormalizer utility."""

    def test_normalize_empty_title_raises_error(self) -> None:
        """Empty title should raise ValueError."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            TitleNormalizer.normalize("")

        with pytest.raises(ValueError, match="Title cannot be empty"):
            TitleNormalizer.normalize("   ")

        # After sanitation, if only empty string remains
        with pytest.raises(ValueError, match="Title cannot be empty"):
            TitleNormalizer.normalize("🚀🌟!!")

    def test_normalize_sanitizes_string(self) -> None:
        """Special characters should be removed/replaced."""
        # We need to mock datetime to check timestamp, or just check format
        # Let's check format: YYYYMMDDHHMMSS_sanitized_name

        result = TitleNormalizer.normalize("My Note Title!")
        assert re.match(r"^\d{14}_my_note_title$", result)

    def test_sanitize_removes_accents(self) -> None:
        """Accents should be removed (e.g. é -> e)."""
        result = TitleNormalizer.sanitize("Créme Brûlée")
        assert result == "creme_brulee"

    def test_sanitize_removes_special_chars(self) -> None:
        """Non-alphanumeric chars should be replaced by underscores."""
        result = TitleNormalizer.sanitize("hello@world#python")
        assert result == "hello_world_python"

        # Extensive symbols case
        symbol_heavy = TitleNormalizer.sanitize("C++ / C# & F# !! 100%")
        assert symbol_heavy == "c_c_f_100"

    def test_sanitize_removes_non_latin(self) -> None:
        """Should handle non-latin characters by removing them if unidecode fails or leaving mostly empty."""
        result = TitleNormalizer.sanitize("Hello こんにちは World")
        # Since unidecode or ascii encoding strips unicode, Japanese chars will likely be stripped.
        # As long as it removes them cleanly without crashing and keeps valid characters:
        assert result == "hello_world"

    def test_sanitize_trims_underscores(self) -> None:
        """Leading/trailing underscores should be removed and sequential underscores collapsed."""
        result = TitleNormalizer.sanitize("  hello world  ")
        assert result == "hello_world"

        result = TitleNormalizer.sanitize("__hello__")
        assert result == "hello"

        result = TitleNormalizer.sanitize("hello___world")
        assert result == "hello_world"

    @pytest.mark.parametrize(
        ("input_title", "expected_sanitized"),
        [
            # Emojis mixed with punctuation
            ("My 🚀 Note!! (Draft)", "my_note_draft"),
            # Unicode/Heavy accents
            ("Café y Brûlée en el Ático", "cafe_y_brulee_en_el_atico"),
            # Concurrent special symbols
            ("C++ / C# & F# - 100%", "c_c_f_100"),
            # Excessive spaces
            ("  A   B  ", "a_b"),
            # Mixed unicode strings that become valid ascii equivalents
            ("Pokémon: The First Movie", "pokemon_the_first_movie"),
        ],
    )
    def test_sanitize_edge_cases(
        self, input_title: str, expected_sanitized: str
    ) -> None:
        """Parametrized test for complex edge cases requested by user."""
        assert TitleNormalizer.sanitize(input_title) == expected_sanitized
