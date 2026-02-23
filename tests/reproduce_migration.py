import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
import logging

# Ensure src is in pythonpath
sys.path.append(str(Path(__file__).parent.parent / "src"))

from dx_vault_atlas.services.note_migrator.core.migrator import NoteMigrator

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Mock Inputs for interactive scenarios
MOCK_INPUTS = {
    "02_missing_type_explicit.md": {
        "type": "info",
        "source": "Other",
        "priority": "1",
    },
    "06_missing_required.md": {"area": "Personal"},
    "08_empty_file.md": {
        "title": "Empty Note",
        "type": "info",
        "priority": 1,
        "status": "active",
        "source": "Other",
        "aliases": [],
    },
}


class MockEditorBuffer:
    def __init__(self, editor="vim"):
        pass

    def prompt_user(self, original_content, frontmatter, missing_fields):
        global CURRENT_SCENARIO
        print(f"Mock user prompt for {CURRENT_SCENARIO}. Missing: {missing_fields}")

        # Validation for 08_empty_file explicit requirement (Title before Type)
        # Note: missing_fields order matters
        if "title" in missing_fields and "type" in missing_fields:
            if missing_fields.index("title") > missing_fields.index("type"):
                print("FAIL: Title was asked AFTER Type")
                raise AssertionError(
                    "FAIL: 'title' should be asked before 'type' for empty files."
                )
            else:
                print("PASS check: Title asked before Type")

        if CURRENT_SCENARIO in MOCK_INPUTS:
            updates = MOCK_INPUTS[CURRENT_SCENARIO]
            # Merge with existing
            return {**frontmatter, **updates}

        return frontmatter


CURRENT_SCENARIO = ""


def run_tests():
    global CURRENT_SCENARIO

    # Adjust path to where scenarios are
    base_path = Path(__file__).parent / "migration_scenarios"
    scenarios = sorted(list(base_path.glob("*.md")))

    results = {}

    print(f"Found {len(scenarios)} scenarios in {base_path}.")

    for scenario_path in scenarios:
        CURRENT_SCENARIO = scenario_path.name

        # Create a temp copy to migrate
        temp_file = scenario_path.with_name(f"temp_{scenario_path.name}")
        temp_file.write_text(
            scenario_path.read_text(encoding="utf-8"), encoding="utf-8"
        )

        status = "UNKNOWN"
        try:
            with (
                patch(
                    "dx_vault_atlas.services.note_migrator.core.migrator.EditorBufferService",
                    MockEditorBuffer,
                ),
                patch(
                    "dx_vault_atlas.services.note_migrator.core.migrator.get_settings"
                ) as mock_get_settings,
            ):
                # Mock settings with dummy paths
                mock_settings = MagicMock()
                mock_settings.vault_path = Path("/tmp/vault")
                mock_settings.vault_inbox = Path("/tmp/vault/Inbox")
                mock_get_settings.return_value = mock_settings

                migrator = NoteMigrator()
                try:
                    res = migrator.migrate(temp_file)
                    status = "SUCCESS"
                except Exception as e:
                    status = f"ERROR: {e.__class__.__name__}: {e}"

            # Validation logic
            final_content = temp_file.read_text(encoding="utf-8")

            if "01_perfect_note" in CURRENT_SCENARIO:
                if status == "SUCCESS" and "version: 1.0.0" in final_content:
                    results[CURRENT_SCENARIO] = "PASS"
                else:
                    results[CURRENT_SCENARIO] = f"FAIL ({status})"

            elif "02_missing_type" in CURRENT_SCENARIO:
                if status == "SUCCESS" and "type: info" in final_content:
                    results[CURRENT_SCENARIO] = "PASS"
                else:
                    results[CURRENT_SCENARIO] = (
                        f"FAIL ({status}) - Expected 'type: info'"
                    )

            elif "03_missing_dates" in CURRENT_SCENARIO:
                # Expect keys created/updated to be present (even if null)
                # In YAML, "created: null" or "created:"
                if (
                    status == "SUCCESS"
                    and "created" in final_content
                    and "updated" in final_content
                ):
                    results[CURRENT_SCENARIO] = "PASS"
                else:
                    results[CURRENT_SCENARIO] = (
                        f"FAIL ({status}) - Expected keys created/updated"
                    )

            elif "04_old_version" in CURRENT_SCENARIO:
                # Check for version key and 1.0 (with flexible quoting)
                if status == "SUCCESS" and (
                    "version: 1.0" in final_content or "version: '1.0'" in final_content
                ):
                    results[CURRENT_SCENARIO] = "PASS"
                else:
                    results[CURRENT_SCENARIO] = (
                        f"FAIL ({status}) - Version not upgraded"
                    )

            elif "05_extra_fields" in CURRENT_SCENARIO:
                if status == "SUCCESS" and "extra_field" not in final_content:
                    results[CURRENT_SCENARIO] = "PASS"
                else:
                    results[CURRENT_SCENARIO] = (
                        f"FAIL ({status}) - Extra field not removed"
                    )

            elif "06_missing_required" in CURRENT_SCENARIO:
                if status == "SUCCESS" and "area: Personal" in final_content:
                    results[CURRENT_SCENARIO] = "PASS"
                else:
                    results[CURRENT_SCENARIO] = (
                        f"FAIL ({status}) - Missing area not filled"
                    )

            elif "07_malformed" in CURRENT_SCENARIO:
                if "FrontmatterParseError" in status:
                    results[CURRENT_SCENARIO] = "PASS"
                else:
                    results[CURRENT_SCENARIO] = (
                        f"FAIL - Expected FrontmatterParseError, got {status}"
                    )

            elif "08_empty_file" in CURRENT_SCENARIO:
                if status == "SUCCESS" and "title: Empty Note" in final_content:
                    results[CURRENT_SCENARIO] = "PASS"
                else:
                    results[CURRENT_SCENARIO] = f"FAIL ({status})"

            elif "09_date_string" in CURRENT_SCENARIO:
                # We expect the string to be preserved exactly as is
                if status == "SUCCESS" and ("October 27, 2023" in final_content):
                    results[CURRENT_SCENARIO] = "PASS"
                else:
                    results[CURRENT_SCENARIO] = (
                        f"FAIL ({status}) - Date format shouldn't change"
                    )

            elif "10_conflict" in CURRENT_SCENARIO:
                if status == "SUCCESS" and "<<< HEAD" in final_content:
                    results[CURRENT_SCENARIO] = "PASS"
                else:
                    results[CURRENT_SCENARIO] = f"FAIL ({status}) - Content damaged"

        except Exception as e:
            import traceback

            traceback.print_exc()
            results[CURRENT_SCENARIO] = f"CRASH: {e}"
            print(f"Content at crash:\n{temp_file.read_text(encoding='utf-8')}")

        finally:
            if results.get(CURRENT_SCENARIO, "").startswith("FAIL"):
                content = temp_file.read_text(encoding="utf-8")
                print(f"FAILED CONTENT for {CURRENT_SCENARIO}:\n{content}")
            temp_file.unlink(missing_ok=True)

    print("\n\n=== SUMMARY ===")
    for name, res in results.items():
        print(f"{name}: {res}")


if __name__ == "__main__":
    run_tests()
