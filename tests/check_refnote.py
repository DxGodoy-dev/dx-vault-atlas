import sys
import json
from pathlib import Path

# Add src to pythonpath
src_dir = Path("c:/Users/Administrator/Desktop/Dev/code/programs/dx-vault-atlas/src")
sys.path.insert(0, str(src_dir))

from dx_vault_atlas.services.note_creator.models.note import RefNote
from dx_vault_atlas.shared.pydantic_utils import strip_unknown_fields

print("RefNote fields:", list(RefNote.model_fields.keys()))
print("Aliases:", [f.alias for f in RefNote.model_fields.values() if f.alias])

data = {"title": "test", "type": "ref", "source": "me", "extra": "foo"}
filtered = strip_unknown_fields(RefNote, data)
print("filtered:", filtered)
