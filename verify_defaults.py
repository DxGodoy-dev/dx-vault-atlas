from pathlib import Path
from dx_vault_atlas.services.note_doctor.core.fixer import NoteFixer
from dx_vault_atlas.services.note_creator.models.enums import NoteStatus


def test_fix_defaults():
    fixer = NoteFixer()

    # Test Case 1: Task missing status (Should be fixed to 'to_do')
    print("Test 1: Task missing status -> Expect 'to_do'")
    fm_task = {
        "title": "Test Task",
        "type": "task",
        # status missing
        "priority": 1,
        "area": "personal",
        "source": "me",
    }

    ok, fixed_task = fixer.check_and_fix_defaults(fm_task)
    assert not ok, "Should have changes"
    assert fixed_task["status"] == NoteStatus.TO_DO.value, (
        f"Status should be to_do, got {fixed_task.get('status')}"
    )
    print("PASS\n")

    # Test Case 2: Task with status (Should remain unchanged)
    print("Test 2: Task with status -> Expect unchanged")
    # We must provide ALL SAFE_FIELDS to ensure no changes are triggered
    fm_task_ok = {
        "title": "Test Task OK",
        "type": "task",
        "status": "in_progress",
        "priority": 1,
        "area": "personal",
        "source": "me",
        "version": "1.0.0",
        "tags": [],
    }
    ok, fixed_task_ok = fixer.check_and_fix_defaults(fm_task_ok)
    assert ok, f"Should not have changes, but got: {fixed_task_ok}"
    assert fixed_task_ok["status"] == "in_progress"
    print("PASS\n")

    # Test Case 3: Priority missing (Should NOT be fixed)
    print("Test 3: Priority missing -> Expect NOT fixed")
    fm_prio = {
        "title": "Test Prio",
        "type": "task",
        "status": "to_do",
        # priority missing
        "area": "personal",
        "source": "me",
    }
    ok, fixed_prio = fixer.check_and_fix_defaults(fm_prio)
    # Changes might happen (version, tags), but 'priority' should NOT be added
    assert "priority" not in fixed_prio, "Priority should NOT be fixed automatically"
    print("PASS\n")


if __name__ == "__main__":
    try:
        test_fix_defaults()
        print("ALL TESTS PASSED")
    except Exception as e:
        print(f"FAILED: {e}")
        exit(1)
