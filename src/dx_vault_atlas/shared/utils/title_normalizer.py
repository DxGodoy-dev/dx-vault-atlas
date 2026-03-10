"""Title normalization utilities for safe filenames."""

import re
import unicodedata
from datetime import datetime

_NON_ALPHANUM_RE = re.compile(r"[^a-z0-9]+")


class TitleNormalizer:
    """Transforms raw strings into standardized Obsidian filenames."""

    @classmethod
    def normalize(cls, raw_title: str) -> str:
        """Generate timestamped safe filename from title.

        Args:
            raw_title: User-provided title string.

        Returns:
            String in format: YYYYMMDDHHMMSS_sanitized_title

        Raises:
            ValueError: If title is empty.
        """
        if not raw_title or not raw_title.strip():
            msg = "Title cannot be empty."
            raise ValueError(msg)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        clean_name = cls.sanitize(raw_title)

        if not clean_name:
            msg = "Title cannot be empty."
            raise ValueError(msg)

        return f"{timestamp}_{clean_name}"

    @staticmethod
    def sanitize(text: str) -> str:
        """Clean string for use as filename.

        Args:
            text: Raw text to sanitize.

        Returns:
            Lowercase alphanumeric string with underscores.
        """
        # 1. Unicode decomposition and accent removal
        text = (
            unicodedata.normalize("NFKD", text)
            .encode("ascii", "ignore")
            .decode("ascii")
        )

        # 2. Lowercase and remove non-alphanumeric characters
        text = text.lower()
        text = _NON_ALPHANUM_RE.sub("_", text)

        # 3. Trim edges
        return text.strip("_")

    @staticmethod
    def normalize_frontmatter_title(raw_title: str) -> str:
        """Normalize YAML frontmatter title string.

        Takes raw title value, removes defective quotes layers,
        un-escapes previously escaped strings to avoid double escaping,
        and returns the strictly clean string.
        (Note: the final double quoting is left to PyYAML dumper.)
        """
        if not raw_title:
            return ""

        cleaned = raw_title.strip()

        # 1. Remove nested defective quotes at the boundaries
        while True:
            if len(cleaned) >= 2 and (
                (cleaned[0] == "'" and cleaned[-1] == "'")
                or (cleaned[0] == '"' and cleaned[-1] == '"')
            ):
                cleaned = cleaned[1:-1]
            else:
                break

        # 2. Undo previous escapes to prevent double escaping
        return cleaned.replace('\\"', '"').replace("\\'", "'")
