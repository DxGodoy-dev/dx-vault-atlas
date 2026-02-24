import os
import sys
from pathlib import Path
from datetime import datetime

# Add src to sys.path
sys.path.insert(0, str(Path(os.getcwd()) / "src"))

from dx_vault_atlas.shared.config import GlobalConfig
from dx_vault_atlas.services.note_migrator.app import MigratorApp
from dx_vault_atlas.services.note_doctor.app import DoctorApp
from dx_vault_atlas.services.note_migrator.services.yaml_parser import YamlParserService


def test_repro():
    vault_path = Path(os.getcwd()) / "test_vault"
    note_path = (
        vault_path
        / "20260218024306_mejores_practicas_para_agentes_en_google_antigravity.md"
    )

    # Mock settings
    settings = GlobalConfig(
        vault_path=vault_path,
        vault_inbox=vault_path,
    )

    print("--- STEP 1: INITIAL STATE ---")
    print(note_path.read_text())

    print("\n--- STEP 2: RUNNING MIGRATE ---")
    migrator = MigratorApp(settings)
    # Target path can be the file itself
    migrator.run(target_path=note_path, debug_mode=True)

    print("\n--- AFTER MIGRATE ---")
    print(note_path.read_text())

    print("\n--- STEP 3: RUNNING DOCTOR ---")
    doctor = DoctorApp(settings)
    # We run _classify_note directly to see the auto-fix logic
    doctor._classify_note(note_path, debug_mode=True)

    print("\n--- AFTER DOCTOR ---")
    print(note_path.read_text())


if __name__ == "__main__":
    test_repro()
