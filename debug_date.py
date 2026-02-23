from pathlib import Path
from datetime import datetime


class DateResolver:
    @staticmethod
    def resolve_created(file_path: Path) -> datetime | None:
        stem = file_path.stem
        print(f"Stem: {stem}")
        candidates = []
        if stem[:8].isdigit():
            if len(stem) >= 14 and stem[:14].isdigit():
                candidates.append(stem[:14])
            if len(stem) >= 12 and stem[:12].isdigit():
                candidates.append(stem[:12])

        print(f"Candidates: {candidates}")
        now = datetime.now()
        for cand in candidates:
            try:
                fmt = "%Y%m%d%H%M%S" if len(cand) == 14 else "%Y%m%d%H%M"
                dt = datetime.strptime(cand, fmt)
                if dt > now:
                    print("Future date")
                    return None
                return dt
            except ValueError:
                continue
        return None


p = Path("20250101120000_dated_task.md")
print(f"Result: {DateResolver.resolve_created(p)}")
