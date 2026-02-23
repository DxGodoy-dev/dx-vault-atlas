from pathlib import Path
from dx_vault_atlas.services.note_doctor.core.fixer import NoteFixer
from dx_vault_atlas.services.note_migrator.services.yaml_parser import YamlParserService


def integration_test():
    print("Running Integration Test...")
    fixer = NoteFixer()
    parser = YamlParserService()

    # Create a test file
    test_file = Path("integration_test_note.md")
    content = """---
title: Integration Test
type: task
aliases: [Integration Test]
priority: 1
area: personal
source: me
---
Body content
"""
    test_file.write_text(content, encoding="utf-8")

    try:
        # Load
        parsed = parser.parse(test_file.read_text(encoding="utf-8"))
        fm = parsed.frontmatter

        # Check defaults
        # We expect status to be missing initially
        assert "status" not in fm

        # Apply fix
        ok, fixed_fm = fixer.check_and_fix_defaults(fm)

        if not ok:
            print("Fixer applied changes.")
            # Verify status is added
            print(f"Status: {fixed_fm.get('status')}")
            print(f"Version: {fixed_fm.get('version')}")

            # Save back (simulate App)
            new_yaml = parser.serialize_frontmatter(fixed_fm)
            test_file.write_text(new_yaml + parsed.body, encoding="utf-8")

            # Verify on disk
            final_content = test_file.read_text(encoding="utf-8")
            if "status: to_do" in final_content:
                print("SUCCESS: File updated with status: to_do")
            else:
                print("FAILURE: File not updated correctly")
                print(final_content)
        else:
            print("FAILURE: Fixer did not report changes.")

    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()


if __name__ == "__main__":
    integration_test()
