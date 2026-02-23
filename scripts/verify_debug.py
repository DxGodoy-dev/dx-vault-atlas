import sys
from unittest.mock import MagicMock, patch
from pathlib import Path
import logging

# Ensure src is in path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from dx_vault_atlas.shared.config import GlobalConfig

# Patch ConfigManager to return our test config
test_vault = (PROJECT_ROOT / ".test-vault").resolve()

# Clean up previous runs
import shutil

if test_vault.exists():
    shutil.rmtree(test_vault)

test_inbox = test_vault / "inbox"
test_inbox.mkdir(parents=True, exist_ok=True)

# Create a bad note
bad_note = test_inbox / "bad_note.md"
bad_note.write_text("---\ncreated: 2021-01-01\n---\n# Bad Note", encoding="utf-8")

print(f"Created bad note at {bad_note}")

# Run CLI
from dx_vault_atlas.cli import app
from typer.testing import CliRunner

runner = CliRunner()

with (
    patch("dx_vault_atlas.shared.config.ConfigManager.load") as mock_load,
    patch(
        "dx_vault_atlas.services.note_doctor.app.ui.query", return_value="Fixed Title"
    ) as mock_ask,
    patch(
        "dx_vault_atlas.services.note_doctor.app.ui.confirm", return_value=True
    ) as mock_confirm,
):
    mock_load.return_value = GlobalConfig(
        vault_path=test_vault, vault_inbox=test_inbox, editor="code"
    )

    print("Running doctor with --debug-mode...")
    result = runner.invoke(app, ["doctor", "--debug-mode"])

    print("Exit Code:", result.exit_code)
    if result.exception:
        print("Exception:", result.exception)
        import traceback

        traceback.print_tb(result.exception.__traceback__)
    # print("Output:", result.stdout) # Output might be huge

    success = False
    if "DEBUG" in result.stdout or "Doctor starting in DEBUG MODE" in result.stdout:
        print("VERIFICATION SUCCESS: Debug logs found.")
        success = True
    else:
        print("VERIFICATION FAILURE: Debug logs NOT found.")
        # Handle unicode printing issues on Windows console
        try:
            print("Context:", result.stdout)
        except UnicodeEncodeError:
            print(
                "Context (encoded):",
                result.stdout.encode("utf-8", errors="replace"),
            )

    # Check if file was actually fixed
    content = bad_note.read_text(encoding="utf-8")
    if "type: Fixed Title" in content:
        print("VERIFICATION SUCCESS: File was modified with fixed type.")
    else:
        print("VERIFICATION FAILURE: File was NOT modified properly.")
        print("File Content:\n", content)
