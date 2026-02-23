"""Date resolution logic for Note Doctor."""

from datetime import datetime
from pathlib import Path
from typing import Any


class DateResolver:
    """Resolves the creation date of a note based on a hierarchy of sources."""

    @staticmethod
    def resolve_created(
        file_path: Path, frontmatter: dict[str, Any]
    ) -> datetime | None:
        """Resolve the creation date.

        Strict Rules:
        1. Timestamp in filename (YYYYMMDDHHMM or YYYYMMDDHHmmss).
        2. NO metadata fallback.
        3. NO frontmatter fallback (we are verifying the frontmatter invalidity).
           Actually, if frontmatter has valid date, we use it?
           No, the goal is to Fix *missing* or *invalid* dates.
           If frontmatter has a valid date, we keep it (Fixer logic does that: if current != true_created).
           Wait, Fixer calls this to find "true_created".
           If "true_created" is purely from filename, then any note without timestamp in filename will have None.
           Then Fixer will set created=None.
           This matches the plan: "Derived ONLY from filename".

        Returns:
            datetime or None if not found/invalid/future.
        """
        # 1. Filename timestamp
        stem = file_path.stem
        # print(f"DEBUG: Resolving date for {stem}")
        # Try to parse timestamp from start of filename
        candidates = []
        if stem[:8].isdigit():
            # Try 14 chars (YYYYMMDDHHMMSS)
            if len(stem) >= 14 and stem[:14].isdigit():
                candidates.append(stem[:14])
            # Try 12 chars (YYYYMMDDHHMM)
            if len(stem) >= 12 and stem[:12].isdigit():
                candidates.append(stem[:12])

        now = datetime.now()

        for cand in candidates:
            try:
                fmt = "%Y%m%d%H%M%S" if len(cand) == 14 else "%Y%m%d%H%M"
                dt = datetime.strptime(cand, fmt)
                # Future check
                if dt > now:
                    return None
                return dt
            except ValueError:
                continue

        # Derived ONLY from filename.
        return None

    @staticmethod
    def resolve_updated(
        file_path: Path, frontmatter: dict[str, Any]
    ) -> datetime | None:
        """Resolve the updated date.

        If we are fixing, we usually want to ensure it exists.
        If we enforce strict rules, maybe we just use created date if missing?
        Or we leave it for the user?
        Plan said: "updated = created" if updated < created.
        """
        # We don't really have a source for "true updated" other than metadata,
        # but user said "NEVER use metadata".
        # So we probably return None or current frontmatter value?
        # The fixer uses this to populate missing field.
        # If we can't use metadata, we can't invent a date.
        # Maybe we return None and let Fixer handle it (e.g. use created).
        return None
