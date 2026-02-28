"""Test that the doctor auto-strips extraneous fields (e.g. source on ref notes)."""

from pathlib import Path

import pytest

from dx_vault_atlas.services.note_doctor.core.fixer import NoteFixer
from dx_vault_atlas.services.note_doctor.validator import NoteDoctorValidator


class TestExtraneousFieldStripping:
    """Verify that extraneous fields are removed during the auto-fix step."""

    @pytest.fixture
    def validator(self) -> NoteDoctorValidator:
        return NoteDoctorValidator()

    @pytest.fixture
    def fixer(self) -> NoteFixer:
        return NoteFixer()

    def test_ref_note_source_stripped(
        self, validator: NoteDoctorValidator, fixer: NoteFixer, tmp_path: Path
    ) -> None:
        """A ref note with source should have it auto-stripped by the fixer."""
        path = tmp_path / "20260218024306_test_note.md"
        content = """---
version: '1.0'
title: Test Note
aliases:
- Test Note
tags: []
created: 2026-02-18 02:43:06
updated: 2026-02-18 02:43:06
type: ref
source: ia
---
# body
"""
        path.write_text(content, encoding="utf-8")

        # Step 1: validator says note is valid (source silently ignored)
        result = validator.validate(path)
        assert result.is_valid, (
            f"Expected valid, got missing={result.missing_fields} "
            f"invalid={result.invalid_fields}"
        )

        # Step 2: fixer should strip 'source' as extraneous
        has_changes, fixed_fm, _ = fixer.fix(
            path, dict(result.frontmatter), result.body
        )
        assert has_changes, "Expected fixer to detect changes (strip source)"
        assert "source" not in fixed_fm, "source should have been stripped"

        # Step 3: re-validate the fixed frontmatter in memory
        fixed_result = validator.validate_content(path, fixed_fm, result.body)
        assert fixed_result.is_valid, (
            f"Expected valid after fix, got missing={fixed_result.missing_fields} "
            f"invalid={fixed_result.invalid_fields}"
        )

    def test_info_note_source_kept(
        self, validator: NoteDoctorValidator, fixer: NoteFixer, tmp_path: Path
    ) -> None:
        """An info note with source should keep it (source is a valid field)."""
        path = tmp_path / "20260218024306_info_note.md"
        content = """---
version: '1.0'
title: Info Note
aliases:
- Info Note
tags: []
created: 2026-02-18 02:43:06
updated: 2026-02-18 02:43:06
type: info
source: ia
priority: 2
status: to_do
---
# body
"""
        path.write_text(content, encoding="utf-8")

        result = validator.validate(path)
        assert result.is_valid

        _, fixed_fm, _ = fixer.fix(path, dict(result.frontmatter), result.body)
        assert "source" in fixed_fm, "source should be kept for info notes"
