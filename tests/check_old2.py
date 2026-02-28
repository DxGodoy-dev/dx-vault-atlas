from pathlib import Path
from dx_vault_atlas.services.note_doctor.validator import NoteDoctorValidator
from dx_vault_atlas.services.note_doctor.core.fixer import NoteFixer

validator = NoteDoctorValidator()
fixer = NoteFixer()

note_path = Path("test_ref.md")

frontmatter = {
    "version": "1.0",
    "type": "ref",
    "title": "test_ref",
    "aliases": ["test_ref"],
    "tags": [],
    "source": "me",
    "created": "2026-02-18 02:43:06",
    "updated": "2026-02-18 02:43:06.960640",
}
body = "\n# body\n"

res = validator.validate_content(note_path, frontmatter, body)
print(f"Initial: is_valid={res.is_valid}, invalid={res.invalid_fields}")

has_changes, fm_final, _ = fixer.fix(note_path, res.frontmatter.copy(), res.body)
print(f"Fixer: has_changes={has_changes}")
print(f"fm_final has source? {'source' in fm_final}")

if has_changes:
    res2 = validator.validate_content(note_path, fm_final, body)
    print(f"Reval: is_valid={res2.is_valid}, invalid={res2.invalid_fields}")
