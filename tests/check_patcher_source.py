from dx_vault_atlas.services.note_doctor.validator import NoteDoctorValidator
from dx_vault_atlas.services.note_doctor.core.patcher import FrontmatterPatcher
from dx_vault_atlas.services.note_doctor.core.fixer import NoteFixer
from pathlib import Path

validator = NoteDoctorValidator()
fixer = NoteFixer()
patcher = FrontmatterPatcher()
path = Path("test_vault/00_Inbox/000_Home.md")

fm = {
    "version": "1.0",
    "title": "000_Home",
    "type": "moc",
    "created": "2026-02-18 02:43:06",
    "updated": "2026-02-18 02:43:06.960640",
}

# 1. Base validation
res = validator.validate_content(path, fm, "")
print("1. Base invalid:", res.invalid_fields)

# 2. Add aliases wizard fix
fixes = {"aliases": ["000_Home"]}
fm2 = patcher.apply_fixes(res.frontmatter.copy(), fixes)
print("2. Patcher output keys:", list(fm2.keys()))
print("   Has source?", "source" in fm2)

# 3. Fixer
_, fm3, _ = fixer.fix(path, fm2, "")
print("3. Fixer output keys:", list(fm3.keys()))
print("   Has source?", "source" in fm3)

# 4. Revalidate
res2 = validator.validate_content(path, fm3, "")
print("4. Reval invalid:", res2.invalid_fields)
