import os
import re

from pathlib import Path

# Adjust path to match the crazy nesting observed in the original hardcoded path:
# ...\dx-vault-atlas\dx_vault\dx_vault\dx_vault\00_Inbox
# Script is in ...\dx-vault-atlas\scripts
# So we need to go up one level to root, then down into dx_vault...
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INBOX = PROJECT_ROOT / "dx_vault" / "dx_vault" / "dx_vault" / "00_Inbox"


def fix_notes():
    for filename in os.listdir(INBOX):
        if not filename.endswith(".md"):
            continue

        path = os.path.join(INBOX, filename)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        if not content.startswith("---"):
            continue

        # Extract frontmatter
        try:
            _, fm, body = content.split("---", 2)
        except ValueError:
            continue

        changed = False

        # Check title
        if "title:" not in fm:
            title = filename.replace(".md", "").replace("_", " ")
            fm += f'\ntitle: "{title}"'
            changed = True
        else:
            # Extract existing title for aliases
            match = re.search(r"title:\s*(.*)", fm)
            if match:
                title = match.group(1).strip().strip("\"'")
            else:
                title = filename.replace(".md", "").replace("_", " ")

        # Check aliases
        if "aliases:" not in fm:
            fm += f'\naliases:\n- "{title}"'
            changed = True

        # Check type
        if "type:" not in fm:
            fm += "\ntype: info"
            changed = True

        # Custom handling per type
        if "type: moc" in fm:
            # Remove source if present (MOC shouldn't have it)
            if "source:" in fm:
                lines = fm.splitlines()
                fm = "\n".join(
                    [l for l in lines if not l.strip().startswith("source:")]
                )
                changed = True
            # Level should be integer (already handled manually or defaulted?)
            if "level:" not in fm:
                fm += "\nlevel: 1"
                changed = True

            # Remove priority if present (MOC shouldn't have it either)
            if "priority:" in fm:
                lines = fm.splitlines()
                fm = "\n".join(
                    [l for l in lines if not l.strip().startswith("priority:")]
                )
                changed = True
        else:
            # Non-MOC notes generally need source (RankedNote)
            if "source:" not in fm:
                fm += "\nsource: me"
                changed = True

            # Task/Project specific
            if "type: project" in fm or "type: task" in fm:
                # Fix invalid status "Ideas" -> "To Do"
                if "status: Ideas" in fm:
                    lines = fm.splitlines()
                    fm = "\n".join(
                        [l.replace("status: Ideas", "status: To Do") for l in lines]
                    )
                    changed = True

                # Normalize status case (to_do -> To Do)
                if "status: to_do" in fm:
                    lines = fm.splitlines()
                    fm = "\n".join(
                        [l.replace("status: to_do", "status: To Do") for l in lines]
                    )
                    changed = True

                if "status:" not in fm:
                    fm += "\nstatus: To Do"  # Title Case
                    changed = True
                if "area:" not in fm:
                    fm += "\narea: Personal"  # Title Case
                    changed = True

            # Fix dates (DD-MM-YYYY -> YYYY-MM-DD)
            # And ensure YYYY-MM-DD has time component (T00:00:00) to satisfy strict datetime
            # Regex to find YYYY-MM-DD not followed by T. matches optional whitespace/CR at end
            if re.search(r"created: \d{4}-\d{2}-\d{2}\s*$", fm, re.MULTILINE):
                fm = re.sub(
                    r"(created: \d{4}-\d{2}-\d{2})(\s*)$",
                    r"\1T00:00:00\2",
                    fm,
                    flags=re.MULTILINE,
                )
                changed = True

            if re.search(r"updated: \d{4}-\d{2}-\d{2}\s*$", fm, re.MULTILINE):
                fm = re.sub(
                    r"(updated: \d{4}-\d{2}-\d{2})(\s*)$",
                    r"\1T00:00:00\2",
                    fm,
                    flags=re.MULTILINE,
                )
                changed = True

            # Specific fix for _Arquitectura if regex failed
            if "created: 2026-02-04" in fm and "T00:00:00" not in fm:
                fm = fm.replace("created: 2026-02-04", "created: 2026-02-04T00:00:00")
                changed = True

            # Legacy fix
            if "created: 24-01-2026" in fm:
                fm = fm.replace("created: 24-01-2026", "created: 2026-01-24T00:00:00")
                changed = True

            # Info specific
            if "type: info" in fm and "status:" not in fm:
                fm += "\nstatus: To Read"
                changed = True

            # Ensure dates exist
            if "created:" not in fm:
                fm += "\ncreated: 2026-02-04T00:00:00"
                changed = True
            if "updated:" not in fm:
                fm += "\nupdated: 2026-02-04T00:00:00"
                changed = True

        # Check priority (RankedNote)
        if "priority:" not in fm and "type: moc" not in fm:
            fm += "\npriority: 1"
            changed = True

        if changed:
            print(f"Fixing {filename}...")
            new_content = f"---{fm}\n---{body}"
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)


if __name__ == "__main__":
    fix_notes()
