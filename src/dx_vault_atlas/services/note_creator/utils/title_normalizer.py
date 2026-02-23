"""Title normalization utilities for safe filenames."""

import re
import unicodedata
from datetime import datetime


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
        clean_name = cls._sanitize(raw_title)

        return f"{timestamp}_{clean_name}"

    @staticmethod
    def _sanitize(text: str) -> str:
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
        text = re.sub(r"[^a-z0-9]+", "_", text)

        # 3. Trim edges
        return text.strip("_")
