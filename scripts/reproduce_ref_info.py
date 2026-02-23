from pathlib import Path
from dx_vault_atlas.services.note_creator.services.templating import TemplatingService
from dx_vault_atlas.services.note_creator.models.note import InfoNote, RefNote
from dx_vault_atlas.services.note_doctor.validator import NoteDoctorValidator


def test_templates():
    templating = TemplatingService()

    # 1. Info Note
    print("\n--- Testing Info Note ---")
    info_note = InfoNote(
        title="My Info",
        aliases=["Info"],
        type="info",
        source="me",
        # Default status should be "To Read"
    )
    print(f"Info Model Status: {info_note.status}")

    info_content = templating.render("info.md", info_note)
    print(f"Rendered Info:\n{info_content}")

    assert "status: To Read" in info_content
    assert "version: '1.0'" in info_content
    assert "priority:" in info_content

    # 2. Ref Note
    print("\n--- Testing Ref Note ---")
    ref_note = RefNote(title="My Ref", aliases=["Ref"], type="ref")

    ref_content = templating.render("ref.md", ref_note)
    print(f"Rendered Ref:\n{ref_content}")

    assert "version: '1.0'" in ref_content
    assert "status:" not in ref_content
    assert "priority:" not in ref_content

    # 3. Validator Check
    print("\n--- Testing Validator ---")
    validator = NoteDoctorValidator()

    # Mock file for validator
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".md") as tmp:
        tmp.write(info_content)
        tmp_path = Path(tmp.name)

    try:
        result = validator.validate(tmp_path)
        print(f"Info Validation: {result.is_valid}")
        if not result.is_valid:
            print(f"Errors: {result.missing_fields} {result.invalid_fields}")

    finally:
        tmp_path.unlink()


if __name__ == "__main__":
    try:
        test_templates()
        print("\nTEST PASSED")
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        import traceback

        traceback.print_exc()
