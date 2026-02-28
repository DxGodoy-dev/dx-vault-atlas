import logging
import sys
import tempfile
import shutil
from pathlib import Path

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).parent / "src"))

logging.basicConfig(level=logging.DEBUG, format="%(message)s")

from dx_vault_atlas.shared.config import GlobalConfig
from dx_vault_atlas.services.note_doctor.app import DoctorApp

NOTE_CONTENT = """\
---
version: '1.0'
title: "test_ref_note"
type: ref
created: 2026-02-18 02:43:06
updated: 2026-02-18 02:43:06.960640
aliases: []
tags: []
---

# Body
"""


def test_repro():
    tmp = Path(tempfile.mkdtemp(prefix="dxva_doctor_"))
    vault_path = tmp / "vault"
    vault_path.mkdir()

    note_path = vault_path / "test_ref_note.md"
    note_path.write_text(NOTE_CONTENT, encoding="utf-8")

    settings = GlobalConfig(
        vault_path=vault_path,
        vault_inbox=vault_path,
    )

    print("--- RUNNING DOCTOR ---")
    doctor = DoctorApp(settings)
    doctor.run(debug_mode=True)

    print("\n--- AFTER DOCTOR ---")
    print(note_path.read_text(encoding="utf-8"))

    shutil.rmtree(tmp)


if __name__ == "__main__":
    test_repro()
