from dx_vault_atlas.services.note_creator.models.note import BaseNote
from dx_vault_atlas.services.note_creator.defaults import SCHEMA_VERSION

print(f"SCHEMA_VERSION: '{SCHEMA_VERSION}'")

note = BaseNote(title="Test Note", aliases=["Test"], type="info")

data = note.model_dump(mode="json", by_alias=True)
print(f"Dumped Data: {data}")

if "version" in data:
    print(f"Version present: {data['version']}")
else:
    print("Version MISSING")
