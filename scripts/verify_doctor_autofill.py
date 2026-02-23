import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Adjust path to import src
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT / "src"))

from dx_vault_atlas.services.note_doctor.tui import DoctorTUI
from dx_vault_atlas.services.note_doctor.validator import ValidationResult
from dx_vault_atlas.services.note_creator.models.enums import NoteTemplate


def test_autofill_existing_info_missing_status():
    print("\n--- Testing Auto-fill: Type=Info, Status Missing ---")
    tui = DoctorTUI()

    # Validation Result: type=info, status missing
    result = ValidationResult(
        file_path=Path("test_info.md"),
        is_valid=False,
        missing_fields=["status"],
        frontmatter={"type": "info", "title": "Test Info"},
    )

    # Mock run_wizard to ensure it's NOT called or called with empty steps
    with patch("dx_vault_atlas.services.note_doctor.tui.run_wizard") as mock_wizard:
        fixes = tui.gather_fixes(result)

        print(f"Fixes: {fixes}")
        assert "status" in fixes
        assert fixes["status"] == "To Read"

        # Verify wizard was NOT called because steps should be empty
        # (missing 'status' was discarded, so no dependencies added)
        mock_wizard.assert_not_called()

    print("PASS: Existing Info Auto-fill")


def test_autofill_selected_info_missing_status():
    print("\n--- Testing Auto-fill: Type Missing -> Select Info ---")
    tui = DoctorTUI()

    # Validation Result: type missing, status missing
    result = ValidationResult(
        file_path=Path("test_new.md"),
        is_valid=False,
        missing_fields=["type", "status"],
        frontmatter={},
    )

    with patch("dx_vault_atlas.services.note_doctor.tui.run_wizard") as mock_wizard:
        # Mock wizard returning Template=INFO
        mock_wizard.return_value = {"template": NoteTemplate.INFO}

        fixes = tui.gather_fixes(result)

        print(f"Fixes: {fixes}")
        assert "status" in fixes
        assert fixes["status"] == "To Read"
        assert fixes["template"] == NoteTemplate.INFO

        # Verify wizard WAS called (to ask for type)
        mock_wizard.assert_called_once()

    print("PASS: Selected Info Auto-fill")


def test_no_autofill_for_task():
    print("\n--- Testing No Auto-fill: Type=Task ---")
    tui = DoctorTUI()

    # Validation Result: type=task, status missing
    result = ValidationResult(
        file_path=Path("test_task.md"),
        is_valid=False,
        missing_fields=["status"],
        frontmatter={"type": "task"},
    )

    with patch("dx_vault_atlas.services.note_doctor.tui.run_wizard") as mock_wizard:
        # User manually selects status in wizard
        mock_wizard.return_value = {"status": "In Progress"}

        fixes = tui.gather_fixes(result)

        print(f"Fixes: {fixes}")
        assert fixes["status"] == "In Progress"

        # Wizard should be called
        mock_wizard.assert_called_once()

    print("PASS: No Auto-fill for Task")


if __name__ == "__main__":
    test_autofill_existing_info_missing_status()
    test_autofill_selected_info_missing_status()
    test_no_autofill_for_task()
