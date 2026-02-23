import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Adjust path to import src
sys.path.append(r"c:\Users\Administrator\Desktop\Dev\code\programs\dx-vault-atlas\src")

from dx_vault_atlas.services.note_doctor.app import DoctorApp, ValidationResult
from dx_vault_atlas.shared.config import AppSettings


def test_gather_fixes_missing_title():
    print("\n--- Testing _gather_fixes_cli: Missing Title ---")
    mock_settings = MagicMock(spec=AppSettings)
    app = DoctorApp(mock_settings)

    # Mock result with missing title
    result = ValidationResult(
        file_path=Path("test_note.md"),
        is_valid=False,
        missing_fields=["title"],
        frontmatter={},
    )

    # Mock UI
    with (
        patch("dx_vault_atlas.shared.console.query") as mock_query,
        patch("dx_vault_atlas.shared.console.confirm") as mock_confirm,
    ):
        # Setup inputs
        mock_confirm.return_value = True  # Yes, fix it
        mock_query.return_value = "Fixed Title"

        fixes = app._gather_fixes_cli(result)

        print(f"Fixes gathered: {fixes}")

        # Verification
        assert "title" in fixes, "Title should be in fixes"
        assert fixes["title"] == "Fixed Title", "Title value mismatch"
        assert "aliases" in fixes, "Aliases should be auto-derived"
        assert fixes["aliases"] == ["Fixed Title"], "Aliases value mismatch"

        # Verify query was called once for title
        # And NOT for aliases (even if it was missing which it is implicitly)
        # Wait, result.missing_fields only had title.
        # If I want to test that it DOESN'T ask for aliases if aliases is also missing:

    print("PASS: Missing Title test")


def test_gather_fixes_missing_title_and_aliases():
    print("\n--- Testing _gather_fixes_cli: Missing Title AND Aliases ---")
    mock_settings = MagicMock(spec=AppSettings)
    app = DoctorApp(mock_settings)

    result = ValidationResult(
        file_path=Path("test_note.md"),
        is_valid=False,
        missing_fields=["title", "aliases"],
        frontmatter={},
    )

    with (
        patch("dx_vault_atlas.shared.console.query") as mock_query,
        patch("dx_vault_atlas.shared.console.confirm") as mock_confirm,
    ):
        mock_confirm.return_value = True
        mock_query.return_value = "Fixed Title"

        fixes = app._gather_fixes_cli(result)

        print(f"Fixes gathered: {fixes}")
        assert fixes["title"] == "Fixed Title"
        assert fixes["aliases"] == ["Fixed Title"]

        # Ensure query was called ONLY for title (and maybe other generic fields if I added them)
        # Check call args
        query_calls = [args[0] for args, _ in mock_query.call_args_list]
        print(f"Query calls: {query_calls}")

        # Should not contain "aliases" or "value for aliases"
        assert not any("aliases" in q for q in query_calls), (
            "Should not prompt for aliases"
        )

    print("PASS: Missing Title+Aliases test")


def test_gather_fixes_only_aliases_missing():
    print("\n--- Testing _gather_fixes_cli: Only Aliases Missing ---")
    mock_settings = MagicMock(spec=AppSettings)
    app = DoctorApp(mock_settings)

    result = ValidationResult(
        file_path=Path("test_note.md"),
        is_valid=False,
        missing_fields=["aliases"],
        frontmatter={"title": "Existing Title"},
    )

    with (
        patch("dx_vault_atlas.shared.console.query") as mock_query,
        patch("dx_vault_atlas.shared.console.confirm") as mock_confirm,
    ):
        fixes = app._gather_fixes_cli(result)

        print(f"Fixes gathered: {fixes}")
        assert "aliases" in fixes
        assert fixes["aliases"] == ["Existing Title"]

        # No query calls expected
        assert mock_query.call_count == 0

    print("PASS: Only Aliases Missing test")


if __name__ == "__main__":
    test_gather_fixes_missing_title()
    test_gather_fixes_missing_title_and_aliases()
    test_gather_fixes_only_aliases_missing()
