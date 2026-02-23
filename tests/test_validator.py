"""Tests for NoteValidator."""

from pathlib import Path

import pytest

from dx_vault_atlas.services.note_doctor.validator import NoteDoctorValidator


class TestNoteValidator:
    """Tests for NoteDoctorValidator."""

    @pytest.fixture
    def validator(self) -> NoteDoctorValidator:
        """Create validator instance."""
        return NoteDoctorValidator()

    @pytest.fixture
    def valid_info_note(self, tmp_path: Path) -> Path:
        """Create a valid info note file."""
        path = tmp_path / "valid_note.md"
        content = """---
title: "Valid Note"
aliases: ["Valid Note"]
tags: []
type: info
source: me
priority: 2
status: to_do
version: "1.0"
created: 2023-01-01T12:00:00
updated: 2023-01-01T12:00:00
---
Some content
"""
        path.write_text(content, encoding="utf-8")
        return path

    @pytest.fixture
    def invalid_note_missing_fields(self, tmp_path: Path) -> Path:
        """Create an info note missing required fields."""
        path = tmp_path / "invalid_missing.md"
        content = """---
title: "Invalid Note"
type: info
---
Content
"""
        path.write_text(content, encoding="utf-8")
        return path

    @pytest.fixture
    def invalid_note_bad_enum(self, tmp_path: Path) -> Path:
        """Create a note with invalid enum value (priority)."""
        # Filename matches title to avoid integrity error
        path = tmp_path / "bad_enum.md"
        content = """---
title: "Bad Enum"
aliases: ["Bad Enum"]
type: info
source: anything
priority: 999
---
Content
"""
        path.write_text(content, encoding="utf-8")
        return path

    def test_validate_valid_note(
        self, validator: NoteDoctorValidator, valid_info_note: Path
    ) -> None:
        """Should return valid result for correct note."""
        result = validator.validate(valid_info_note)

        assert result.is_valid
        assert result.missing_fields == []
        assert result.invalid_fields == []
        assert result.error is None
        assert result.frontmatter["title"] == "Valid Note"

    def test_validate_missing_fields(
        self, validator: NoteDoctorValidator, invalid_note_missing_fields: Path
    ) -> None:
        """Should detect missing required fields."""
        result = validator.validate(invalid_note_missing_fields)

        assert not result.is_valid
        # Required for info: aliases, source, priority
        # Note: source is kept required in structure check but validation is lenient
        assert "source" in result.missing_fields
        assert "priority" in result.missing_fields

    def test_validate_missing_type(
        self, validator: NoteDoctorValidator, tmp_path: Path
    ) -> None:
        """Should fail if type field is missing."""
        path = tmp_path / "no_type.md"
        path.write_text("---\ntitle: No Type\n---\n", encoding="utf-8")

        result = validator.validate(path)

        assert not result.is_valid
        assert "type" in result.missing_fields

    def test_validate_invalid_enum(
        self, validator: NoteDoctorValidator, invalid_note_bad_enum: Path
    ) -> None:
        """Should identify invalid priority enum."""
        result = validator.validate(invalid_note_bad_enum)

        assert not result.is_valid
        # Should identify priority as invalid
        assert "priority" in result.invalid_fields
        # Source should NOT be invalid, but might be a warning
        # (It was "anything", which is a string, so it should be a warning)
        assert "source" not in result.invalid_fields
        assert any("unknown_source" in w for w in result.warnings)

    def test_validate_valid_source_string(
        self, validator: NoteDoctorValidator, tmp_path: Path
    ) -> None:
        """Should accept arbitrary string for source."""
        path = tmp_path / "custom_source.md"
        content = """---
title: "Custom Source"
aliases: ["Custom Source"]
type: info
source: "custom_provider"
priority: 1
status: "to_do"
version: "1.0"
---
"""
        path.write_text(content, encoding="utf-8")
        result = validator.validate(path)

        assert result.is_valid
        # Should have warning
        assert any("unknown_source" in w for w in result.warnings)
        # Should have warning
        assert any("unknown_source" in w for w in result.warnings)

    def test_validate_nonexistent_file(
        self, validator: NoteDoctorValidator, tmp_path: Path
    ) -> None:
        """Should handle missing file gracefully."""
        result = validator.validate(tmp_path / "ghost.md")

        assert not result.is_valid
        assert "Read error" in str(result.error)

    def test_validate_bad_yaml(
        self, validator: NoteDoctorValidator, tmp_path: Path
    ) -> None:
        """Should handle malformed YAML."""
        path = tmp_path / "bad.yml"
        path.write_text("---\ntitle: [unclosed list\n---\n", encoding="utf-8")

        result = validator.validate(path)

        assert not result.is_valid
        assert "YAML error" in str(result.error)
