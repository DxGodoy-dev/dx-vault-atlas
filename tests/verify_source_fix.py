"""End-to-end verification of the two bug fixes.

Test 1: _classify_note should NOT write note if re-validation fails
Test 2: _run_pydantic should ignore extra_forbidden errors
Test 3: Full flow — ref note with source:me should be cleaned by fixer
"""

import sys
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dx_vault_atlas.services.note_migrator.services.yaml_parser import YamlParserService
from dx_vault_atlas.services.note_doctor.validator import NoteDoctorValidator
from dx_vault_atlas.services.note_doctor.core.fixer import NoteFixer

parser = YamlParserService()
validator = NoteDoctorValidator()
fixer = NoteFixer()

passed = 0
total = 0


def check(name: str, condition: bool) -> None:
    global passed, total
    total += 1
    if condition:
        passed += 1
        print(f"  ✅ {name}")
    else:
        print(f"  ❌ {name}")


# ── Test 1: Ref note with source:me — validator should NOT flag source as invalid
print("\n=== Test 1: Validator ignores extra_forbidden for source ===")

NOTE_REF_WITH_SOURCE = """\
---
version: '1.0'
type: ref
title: Test Ref Note
created: 2025-02-18 02:43:06
updated: 2025-02-18 02:43:06
aliases:
- Test Ref Note
tags: []
source: me
---
Body
"""

tmp = Path(tempfile.mkdtemp(prefix="verify_"))
p = tmp / "20250218024306_test_ref_note.md"
p.write_text(NOTE_REF_WITH_SOURCE, encoding="utf-8")

result = validator.validate(p)
check("Validation passes (source silently ignored)", result.is_valid)
check("source NOT in invalid_fields", "source" not in result.invalid_fields)
check("source NOT in missing_fields", "source" not in result.missing_fields)

shutil.rmtree(tmp)

# ── Test 2: Fixer removes source from ref note
print("\n=== Test 2: Fixer removes source from ref note ===")

tmp = Path(tempfile.mkdtemp(prefix="verify_"))
p = tmp / "20250218024306_test_ref_note.md"
p.write_text(NOTE_REF_WITH_SOURCE, encoding="utf-8")

result = validator.validate(p)
has_changes, fm_final, body = fixer.fix(p, result.frontmatter.copy(), result.body)
check("Fixer detects changes", has_changes)
check("source removed from fm_final", "source" not in fm_final)

# Re-validate
fixed_result = validator.validate_content(p, fm_final, body)
check("Re-validation passes", fixed_result.is_valid)
check(
    "source NOT in invalid_fields after fix",
    "source" not in fixed_result.invalid_fields,
)

shutil.rmtree(tmp)

# ── Test 3: Post-migrate note (no source) — doctor classify logic
print("\n=== Test 3: Post-migrate note stays clean ===")

NOTE_POST_MIGRATE = """\
---
version: '1.0'
type: ref
title: Mejores Prácticas
created: 2025-02-18 02:43:06
updated: 2025-02-18 02:43:06.960640
aliases:
- Mejores Prácticas
tags: []
---
Body
"""

tmp = Path(tempfile.mkdtemp(prefix="verify_"))
p = tmp / "20250218024306_mejores_practicas.md"
p.write_text(NOTE_POST_MIGRATE, encoding="utf-8")

result = validator.validate(p)
check("Post-migrate note passes validation", result.is_valid)
check("No source in frontmatter", "source" not in result.frontmatter)

has_changes, fm_final, body = fixer.fix(p, result.frontmatter.copy(), result.body)
check("Fixer makes no changes", not has_changes)
check("Still no source in output", "source" not in fm_final)

# Verify file on disk unchanged
final = parser.parse(p.read_text(encoding="utf-8"))
check("File on disk unchanged (no source)", "source" not in final.frontmatter)

shutil.rmtree(tmp)

# ── Test 4: Info note with custom source — should be warning only
print("\n=== Test 4: Info note with custom source → warning only ===")

NOTE_INFO_CUSTOM_SOURCE = """\
---
version: '1.0'
type: info
title: Custom Source Note
created: 2025-01-01 12:00:00
updated: 2025-01-01 12:00:00
aliases:
- Custom Source Note
tags: []
source: custom_provider
priority: 1
status: to_do
---
Body
"""

tmp = Path(tempfile.mkdtemp(prefix="verify_"))
p = tmp / "custom_source_note.md"
p.write_text(NOTE_INFO_CUSTOM_SOURCE, encoding="utf-8")

result = validator.validate(p)
check("Info note with custom source passes validation", result.is_valid)
check(
    "Has warning about unknown source",
    any("unknown_source" in w for w in result.warnings),
)
check("source NOT in invalid_fields", "source" not in result.invalid_fields)

shutil.rmtree(tmp)

# ── Summary
print(f"\n{'=' * 50}")
print(f"Results: {passed}/{total} passed")
if passed == total:
    print("✅ All verifications passed!")
else:
    print("❌ Some verifications failed!")
    sys.exit(1)
