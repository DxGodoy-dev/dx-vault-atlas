"""Test that the doctor auto-strips extraneous fields (e.g. source on ref notes)."""

from pathlib import Path

import pytest

from dx_vault_atlas.shared.utils.date_resolver import DateResolver
from dx_vault_atlas.services.note_doctor.core.fixer import (
    DateFixRule,
    DefaultsFixRule,
    EnumFixRule,
    ExtraneousFieldsFixRule,
    NoteFixer,
)
from dx_vault_atlas.services.note_doctor.validator import NoteDoctorValidator
from dx_vault_atlas.shared.yaml_parser import YamlParserService


class TestExtraneousFieldStripping:
    """Verify that extraneous fields are removed during the auto-fix step."""

    @pytest.fixture
    def yaml_parser(self) -> YamlParserService:
        return YamlParserService()

    @pytest.fixture
    def validator(self, yaml_parser: YamlParserService) -> NoteDoctorValidator:
        return NoteDoctorValidator(yaml_parser=yaml_parser)

    @pytest.fixture
    def fixer(self) -> NoteFixer:
        dr = DateResolver()
        return NoteFixer(
            rules=[
                DateFixRule(dr),
                EnumFixRule(),
                DefaultsFixRule(),
                ExtraneousFieldsFixRule(),
            ]
        )

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

    def test_info_note_keeps_priority(
        self, validator: NoteDoctorValidator, fixer: NoteFixer, tmp_path: Path
    ) -> None:
        """An info note with priority should keep it (priority is a valid field)."""
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
priority: 2
status: to_do
---
# body
"""
        path.write_text(content, encoding="utf-8")

        result = validator.validate(path)
        assert result.is_valid

        _, fixed_fm, _ = fixer.fix(path, dict(result.frontmatter), result.body)
        assert "priority" in fixed_fm, "priority should be kept for info notes"

    def test_fix_type_strips_md_suffix(self, fixer: NoteFixer, tmp_path: Path) -> None:
        """Fixer should normalise 'ref.md' to 'ref' in the type field."""
        path = tmp_path / "20260218024306_test_md_suffix.md"
        content = """\
---
version: '1.0'
title: Test MD Suffix
aliases:
- Test MD Suffix
tags: []
created: 2026-02-18 02:43:06
updated: 2026-02-18 02:43:06
type: ref.md
source: ia
---
# body
"""
        path.write_text(content, encoding="utf-8")
        result = NoteDoctorValidator(yaml_parser=YamlParserService()).validate(path)
        has_changes, fixed_fm, _ = fixer.fix(
            path, dict(result.frontmatter), result.body
        )
        assert has_changes, "Expected changes (type normalisation + source strip)"
        assert fixed_fm["type"] == "ref", f"Expected 'ref', got {fixed_fm['type']!r}"
        assert "source" not in fixed_fm, "source should be stripped for ref notes"

    def test_ref_note_extraneous_after_fixer(
        self, validator: NoteDoctorValidator, fixer: NoteFixer, tmp_path: Path
    ) -> None:
        """Re-validation after fixer should be clean for ref notes."""
        path = tmp_path / "20260218024306_clean_ref.md"
        content = """\
---
version: '1.0'
title: Clean Ref
aliases:
- Clean Ref
tags: []
created: 2026-02-18 02:43:06
updated: 2026-02-18 02:43:06
type: ref.md
source: ia
---
# body
"""
        path.write_text(content, encoding="utf-8")

        # Fixer normalises type and strips source
        result = validator.validate(path)
        has_changes, fixed_fm, body = fixer.fix(
            path, dict(result.frontmatter), result.body
        )
        assert fixed_fm["type"] == "ref"
        assert "source" not in fixed_fm

        # Re-validation should pass
        fixed_result = validator.validate_content(path, fixed_fm, body)
        assert fixed_result.is_valid, (
            f"Re-validation failed: missing={fixed_result.missing_fields} "
            f"invalid={fixed_result.invalid_fields}"
        )
