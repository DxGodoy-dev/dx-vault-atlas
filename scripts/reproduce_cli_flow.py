import sys
from unittest.mock import MagicMock

# NUCLEAR OPTION: Mock questionary in sys.modules BEFORE any import
mock_questionary = MagicMock()
sys.modules["questionary"] = mock_questionary

# Also mock rich.console if needed, but questionary is the main interactive one
# mock_console = MagicMock()
# sys.modules["rich.console"] = mock_console

import os

from pathlib import Path

# Adjust path to import src
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT / "src"))

from dx_vault_atlas.services.note_creator.main import main
from dx_vault_atlas.services.note_creator.models.enums import (
    NoteTemplate,
    NoteSource,
    Priority,
    NoteArea,
    NoteStatus,
)


def run_tests():
    print("\n--- Testing MOC Creation ---")

    # Configure mocks
    # questionary.text("...").ask() -> returns title
    mock_questionary.text.return_value.ask.return_value = "Test MOC Note"

    # questionary.select("...").ask() -> returns template (Enum member)
    # The first select call is for Template
    mock_questionary.select.return_value.ask.return_value = NoteTemplate.MOC

    try:
        main()
        print("MOC Note creation flow completed.")
    except SystemExit:
        pass
    except Exception as e:
        print(f"Error MOC: {e}")

    print("\n--- Testing INFO Creation ---")
    mock_questionary.text.return_value.ask.return_value = "Test INFO Note"
    # Sequence: Template, Source, Priority
    mock_questionary.select.return_value.ask.side_effect = [
        NoteTemplate.INFO,
        NoteSource.ME,
        Priority.MEDIUM,
    ]

    try:
        main()
        print("INFO Note creation flow completed.")
    except SystemExit:
        pass
    except Exception as e:
        print(f"Error INFO: {e}")

    mock_questionary.select.return_value.ask.side_effect = None

    print("\n--- Testing TASK Creation ---")
    mock_questionary.text.return_value.ask.return_value = "Test TASK Note"
    # Sequence: Template, Source, Priority, Area
    mock_questionary.select.return_value.ask.side_effect = [
        NoteTemplate.TASK,
        NoteSource.ME,
        Priority.HIGH,
        NoteArea.WORK,
    ]

    try:
        main()
        print("TASK Note creation flow completed.")
    except SystemExit:
        pass
    except Exception as e:
        print(f"Error TASK: {e}")

    mock_questionary.select.return_value.ask.side_effect = None

    print("\n--- Testing PROJECT Creation ---")
    mock_questionary.text.return_value.ask.return_value = "Test PROJECT Note"
    # Sequence: Template, Source, Priority, Area
    mock_questionary.select.return_value.ask.side_effect = [
        NoteTemplate.PROJECT,
        NoteSource.RESEARCH,
        Priority.CRITICAL,
        NoteArea.PERSONAL,
    ]

    try:
        main()
        print("PROJECT Note creation flow completed.")
    except SystemExit:
        pass
    except Exception as e:
        print(f"Error PROJECT: {e}")


if __name__ == "__main__":
    run_tests()
