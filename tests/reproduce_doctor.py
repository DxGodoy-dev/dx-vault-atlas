"""Reproduction script for Note Doctor Validation.

Iterates over scenarios in tests/doctor_scenarios/,
runs Fixer & Validator, and checks results.
"""

import re
import shutil
import sys
from pathlib import Path

import yaml


class NoAliasDumper(yaml.SafeDumper):
    """YAML dumper that avoids &id001 anchors."""

    def ignore_aliases(self, data):  # noqa: ANN001, ANN201
        return True


# Add src to path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from dx_vault_atlas.services.note_doctor.core.fixer import (  # noqa: E402
    NoteFixer,
)
from dx_vault_atlas.services.note_doctor.validator import (  # noqa: E402
    NoteDoctorValidator,
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
    # 17: Has unknown_field. Fixer doesn't remove unknowns → no changes.
    # Pydantic extra="forbid" → invalid.
    "17_extra_fields": {
        "changes_made": False,
        "valid_after_fix": False,
    },
    # 18: source: "Aliens" (invalid enum, no NoteSource match).
    # Fixer doesn't modify it → no changes. Validator catches it.
    "18_unknown_enum_source": {
        "changes_made": False,
        "valid_after_fix": False,
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


def main() -> None:  # noqa: C901
    """Run all 20 doctor scenarios and check expectations."""
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
    TEMP_DIR.mkdir()

    fixer = NoteFixer()
    validator = NoteDoctorValidator()

    results: list[bool] = []
    scenarios = sorted(SCENARIOS_DIR.glob("*.md"))

    print(f"Running {len(scenarios)} scenarios...\n")  # noqa: T201

    for scenario_path in scenarios:
        case_name = scenario_path.stem
        temp_path = TEMP_DIR / scenario_path.name
        shutil.copy2(scenario_path, temp_path)

        # ── Pre-rename to match title (for integrity check) ──
        # Skip rename for scenario 14 to test integrity mismatch.
        if "14_alias_consistency_fail" not in case_name:
            try:
                content = temp_path.read_text("utf-8")
                parsed = fixer.parser.parse(content)
                title = parsed.frontmatter.get("title")
                if title and isinstance(title, str):
                    safe = title.lower().replace(" ", "_").replace("-", "_")
                    # Preserve timestamp prefix from filename
                    ts = re.search(r"(\d{12,14})$", scenario_path.stem)
                    if ts:
                        safe = f"{ts.group(1)}_{safe}"
                    safe += ".md"
                    new_path = TEMP_DIR / safe
                    if new_path != temp_path:
                        shutil.move(str(temp_path), str(new_path))
                        temp_path = new_path
                        print(  # noqa: T201
                            f"  Renamed to {temp_path.name}"
                        )
            except Exception:
                pass

        # ── Run Fixer ──
        has_changes, fixed_fm, body = fixer.fix(temp_path)

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
        expectation = None
        for key, exp in EXPECTATIONS.items():
            if key in case_name:
                expectation = exp
                break
        if not expectation:
            print(f"[SKIP] {case_name}")  # noqa: T201
            continue

        failed = False
        reasons: list[str] = []

        if has_changes != expectation["changes_made"]:
            failed = True
            reasons.append(
                f"changes_made: expected "
                f"{expectation['changes_made']}, "
                f"got {has_changes}"
            )

        if val_result.is_valid != expectation["valid_after_fix"]:
            failed = True
            reasons.append(
                f"valid_after_fix: expected "
                f"{expectation['valid_after_fix']}, "
                f"got {val_result.is_valid} "
                f"(inv={val_result.invalid_fields} "
                f"miss={val_result.missing_fields})"
            )

        final = temp_path.read_text("utf-8")
        for s in expectation.get("content_contains", []):
            if s not in final:
                failed = True
                reasons.append(f"missing content: '{s}'")

        if failed:
            print(f"[FAIL] {case_name}")  # noqa: T201
            for r in reasons:
                print(f"  - {r}")  # noqa: T201
            # Show snippet for debugging
            print(  # noqa: T201
                f"    content: {final[:300]!r}..."
            )
            results.append(False)
        else:
            print(f"[PASS] {case_name}")  # noqa: T201
            results.append(True)

    passed = sum(results)
    total = len(results)
    print(f"\nSummary: {passed}/{total} passed.")  # noqa: T201
    sys.exit(0 if passed == total and total > 0 else 1)


if __name__ == "__main__":
    main()
