"""Reproduction script for Note Doctor Validation.

Iterates over scenarios in tests/doctor_scenarios/,
runs Fixer & Validator, and checks results.
"""

import re
import shutil
from pathlib import Path

import yaml


class NoAliasDumper(yaml.SafeDumper):
    """YAML dumper that avoids &id001 anchors."""

    def ignore_aliases(self, data):  # noqa: ANN001, ANN201
        return True


from dx_vault_atlas.shared.utils.date_resolver import (
    DateResolver,
)
from dx_vault_atlas.services.note_doctor.core.fixer import (
    DateFixRule,
    DefaultsFixRule,
    EnumFixRule,
    ExtraneousFieldsFixRule,
    NoteFixer,
)
from dx_vault_atlas.services.note_doctor.validator import (
    NoteDoctorValidator,
)
from dx_vault_atlas.shared.yaml_parser import (
    YamlParserService,
    YamlParseError,
)

SCENARIOS_DIR = Path(__file__).parent / "doctor_scenarios"
TEMP_DIR = Path(__file__).parent / "temp_doctor_repro"

# ── Expected outcomes ────────────────────────────────────────────
#   changes_made  : Did fixer modify frontmatter?
#   valid_after_fix: Is it valid after fix?
#   content_contains: Substrings expected in final YAML content
EXPECTATIONS = {
    # 01: Already perfect task note. Fixer should change nothing.
    "01_valid_note": {
        "changes_made": False,
        "valid_after_fix": True,
    },
    # 02: Missing dates but filename has timestamp → fixer adds them
    "02_missing_dates_filename_20250101120000": {
        "changes_made": True,
        "valid_after_fix": True,
        "content_contains": ["created: 2025-01-01 12:00:00"],
    },
    # 03: Missing dates, no filename timestamp → created=None → invalid
    "03_missing_dates_no_filename": {
        "changes_made": True,
        "valid_after_fix": False,  # null created fails Pydantic
    },
    # 04: Future dates → set to None → validator flags
    "04_future_creation_date": {
        "changes_made": True,
        "valid_after_fix": False,  # null created fails Pydantic
    },
    # 05: Status TO-DO → to_do
    "05_bad_status_casing": {
        "changes_made": True,
        "valid_after_fix": True,
        "content_contains": ["status: to_do"],
    },
    # 06: Status 'doing' (invalid) → deleted → default to_do
    "06_bad_status_default": {
        "changes_made": True,
        "valid_after_fix": True,
        "content_contains": ["status: to_do"],
    },
    # 07: priority: "High" (string). Fixer doesn't convert strings→int.
    # All other fields valid → no changes. Validator fails on priority.
    "07_priority_string": {
        "changes_made": False,
        "valid_after_fix": False,
    },
    # 08: All fields valid including priority: 3. No changes.
    "08_priority_int_valid": {
        "changes_made": False,
        "valid_after_fix": True,
    },
    # 09: Missing 'type'. Fixer adds type='note'. But 'note' is not
    # in MODEL_MAP for Pydantic validation → check_and_fix_defaults
    # returns early. Validator will see 'note' type and check MODEL_MAP.
    "09_missing_required_no_default": {
        "changes_made": True,
        "valid_after_fix": True,
    },
    # 10: Missing 'tags'. Fixer adds tags=[].
    "10_missing_optional_has_default": {
        "changes_made": True,
        "valid_after_fix": True,
    },
    # 11: status: [to_do] (list) → fix to string "to_do"
    "11_list_status": {
        "changes_made": True,
        "valid_after_fix": True,
        "content_contains": ["status: to_do"],
    },
    # 12: tags: null → tags: []
    "12_null_tags": {
        "changes_made": True,
        "valid_after_fix": True,
    },
    # 13: Title "My Job", file renamed to "my_job.md" → ok.
    # All fields present and valid → no changes.
    "13_alias_consistency_ok": {
        "changes_made": False,
        "valid_after_fix": True,
    },
    # 14: Title "Mismatch Title", file stays "14_alias_consistency_fail.md"
    # → integrity check fails. All fields valid → no fixer changes.
    "14_alias_consistency_fail": {
        "changes_made": False,
        "valid_after_fix": False,
    },
    # 15: aliases: "String Alias Task" (string → list)
    "15_string_alias": {
        "changes_made": True,
        "valid_after_fix": True,
    },
    # 16: updated(01) < created(02). Fixer sets updated=created.
    "16_updated_before_created_20250102120000": {
        "changes_made": True,
        "valid_after_fix": True,
        "content_contains": [
            "updated: 2025-01-02 12:00:00",
        ],
    },
    # 17: Has unknown_field. Fixer strips unknowns → valid.
    "17_extra_fields": {
        "changes_made": True,
        "valid_after_fix": True,
    },
    # 19: Malformed YAML → parser fails → no changes, invalid
    "19_malformed_frontmatter": {
        "changes_made": False,
        "valid_after_fix": False,
    },
    # 20: Multiple issues: status TO-DO, aliases string, tags null,
    # no dates. Fixer fixes what it can but null dates fail Pydantic.
    "20_complex_mixed": {
        "changes_made": True,
        "valid_after_fix": False,  # null created/updated fail Pydantic
        "content_contains": [
            "status: to_do",
        ],
    },
}


import pytest


def get_scenarios() -> list[Path]:
    """Get all scenario files for parameterization."""
    return sorted(SCENARIOS_DIR.glob("*.md"))


@pytest.mark.parametrize("scenario_path", get_scenarios(), ids=lambda p: p.stem)
def test_doctor_scenario(scenario_path: Path, tmp_path: Path) -> None:
    """Run a single doctor scenario and check expectations."""
    case_name = scenario_path.stem

    expectation = None
    for key, exp in EXPECTATIONS.items():
        if key in case_name:
            expectation = exp
            break

    if not expectation:
        pytest.skip(f"No expectations defined for {case_name}")

    dr = DateResolver()
    fixer = NoteFixer(
        rules=[
            DateFixRule(dr),
            EnumFixRule(),
            DefaultsFixRule(),
            ExtraneousFieldsFixRule(),
        ]
    )
    parser = YamlParserService()
    validator = NoteDoctorValidator(yaml_parser=parser)

    temp_path = tmp_path / scenario_path.name
    shutil.copy2(scenario_path, temp_path)

    # ── Pre-rename to match title (for integrity check) ──
    if "14_alias_consistency_fail" not in case_name:
        try:
            content = temp_path.read_text("utf-8")
            parsed = parser.parse(content)
            title = parsed.frontmatter.get("title")
            if title and isinstance(title, str):
                safe = title.lower().replace(" ", "_").replace("-", "_")
                ts = re.search(r"(\d{12,14})$", scenario_path.stem)
                if ts:
                    safe = f"{ts.group(1)}_{safe}"
                safe += ".md"
                new_path = tmp_path / safe
                if new_path != temp_path:
                    shutil.move(str(temp_path), str(new_path))
                    temp_path = new_path
        except Exception:
            pass

    # ── Run Fixer ──
    try:
        parsed_current = parser.parse(temp_path.read_text("utf-8"))
        has_changes, fixed_fm, body = fixer.fix(
            temp_path, parsed_current.frontmatter, parsed_current.body
        )
    except YamlParseError:
        has_changes, fixed_fm, body = False, {}, ""

    # ── Write back if changed ──
    if has_changes:
        new_yaml = yaml.dump(
            fixed_fm,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            Dumper=NoAliasDumper,
        )
        new_content = f"---\n{new_yaml}---\n{body}"
        temp_path.write_text(new_content, "utf-8")

    # ── Run Validator ──
    val_result = validator.validate(temp_path)

    # ── Match expectations ──
    assert has_changes == expectation["changes_made"], "Mismatch in changes_made"
    assert val_result.is_valid == expectation["valid_after_fix"], (
        f"Mismatch in valid_after_fix (invalid={val_result.invalid_fields}, missing={val_result.missing_fields})"
    )

    final_content = temp_path.read_text("utf-8")
    for s in expectation.get("content_contains", []):
        assert s in final_content, (
            f"Expected '{s}' not in content:\n{final_content[:300]}"
        )
