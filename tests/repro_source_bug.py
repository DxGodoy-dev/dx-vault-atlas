"""Reproduce: Full DoctorApp._classify_note + _process_note flow.

Scenario: Note of type 'ref' has 'source: me'.
Migration was NOT run. Doctor runs.
What happens?
"""

import sys
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import logging

logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")

from dx_vault_atlas.services.note_migrator.services.yaml_parser import YamlParserService
from dx_vault_atlas.services.note_doctor.validator import (
    NoteDoctorValidator,
    ValidationResult,
)
from dx_vault_atlas.services.note_doctor.core.fixer import NoteFixer

parser = YamlParserService()
validator = NoteDoctorValidator()
fixer = NoteFixer()

# Note with source:me, type ref — NOT migrated
NOTE = """\
---
version: '1.0'
type: ref
title: Mejores Prácticas para Agentes en Google Antigravity
created: 2026-02-18 02:43:06
updated: 2026-02-18 02:43:06.960640
aliases:
- Mejores Prácticas para Agentes en Google Antigravity
tags: []
source: me
---

# Body
"""

tmp = Path(tempfile.mkdtemp(prefix="dxva_full_"))
note_path = (
    tmp / "20260218024306_mejores_practicas_para_agentes_en_google_antigravity.md"
)
note_path.write_text(NOTE, encoding="utf-8")

print("=" * 70)
print("Simulating _classify_note exactly as written in app.py")
print("=" * 70)

# ── Step 1: validate (from disk)
debug_mode = True
if debug_mode:
    print(f"\n[DEBUG] Validating: {note_path.name}")

result = validator.validate(note_path)

if result.error:
    print(f"  ERROR: {result.error}")
    sys.exit(1)

if debug_mode and not result.is_valid:
    print(
        f"[DEBUG] Invalid | {note_path.name}"
        f" | missing={result.missing_fields}"
        f" | invalid={result.invalid_fields}"
    )

print(f"\n  [TRACE] result.is_valid = {result.is_valid}")
print(f"  [TRACE] 'source' in result.frontmatter = {'source' in result.frontmatter}")
print(f"  [TRACE] result.frontmatter = {result.frontmatter}")

# ── Step 2: fixer.fix
has_changes, fm_final, body = fixer.fix(
    note_path,
    result.frontmatter.copy(),
    result.body,
)

print(f"\n  [TRACE] fixer.fix completed:")
print(f"    has_changes = {has_changes}")
print(f"    'source' in fm_final = {'source' in fm_final}")

# ── Step 3: Config-driven mappings (simulated as no-ops)
# field_mappings and value_mappings are empty/default in this scenario

# ── Step 4: classify
print(f"\n  [TRACE] Decision point:")
print(f"    result.is_valid = {result.is_valid}")
print(f"    has_changes     = {has_changes}")

if result.is_valid and not has_changes:
    print(f"\n  → CLASSIFIED AS 'valid' (NO CHANGES)")
    print(f"  ⚠️  But source:me is STILL in the file on disk!")
    print(f"  The note was NOT written, so source stays untouched.")
    print(f"\n  This means the bug is NOT in doctor re-injecting source,")
    print(f"  but in doctor FAILING TO REMOVE source from ref notes.")
    print(f"  The validator silently swallows it via strip_unknown_fields.")
elif has_changes:
    print(f"\n  → AUTO-FIXING (has_changes=True)")
    if debug_mode:
        print(f"[DEBUG] Auto-fixing | {note_path.name}")

    fixed_result = validator.validate_content(note_path, fm_final, body)

    print(f"\n  [TRACE] Re-validation:")
    print(f"    is_valid = {fixed_result.is_valid}")
    print(f"    missing  = {fixed_result.missing_fields}")
    print(f"    invalid  = {fixed_result.invalid_fields}")
    print(f"    'source' in fm_final = {'source' in fm_final}")

    # Write note
    yaml_content = parser.serialize_frontmatter(fm_final)
    note_path.write_text(yaml_content + body, encoding="utf-8")

    if fixed_result.is_valid:
        print(f"\n  → CLASSIFIED AS 'valid' after auto-fix")
    else:
        print(f"\n  → CLASSIFIED AS INVALID - goes to _process_note")
        print(f"    invalid_fields = {fixed_result.invalid_fields}")

        # Simulate what _process_note would show
        print(f"\n  ━━━ [1/33] {note_path.name} ━━━")
        real_invalids = [x for x in fixed_result.invalid_fields if x != "dates"]
        if real_invalids:
            print(f"  Invalid: {', '.join(real_invalids)}")

print(f"\n--- Final state of file on disk ---")
print(note_path.read_text(encoding="utf-8"))

final = parser.parse(note_path.read_text(encoding="utf-8"))
print(f"\n  'source' in final frontmatter: {'source' in final.frontmatter}")

shutil.rmtree(tmp)
