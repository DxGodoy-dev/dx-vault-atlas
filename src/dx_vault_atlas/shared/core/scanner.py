"""Shared vault scanner."""

from collections.abc import Generator
from pathlib import Path


class VaultScanner:
    """Scans the vault for markdown files using a generator."""

    DEFAULT_EXCLUDES: set[str] = {".obsidian", ".trash", ".git", "templates"}

    def __init__(self, exclude_dirs: set[str] | None = None) -> None:
        """Initialize scanner with optional custom exclusions.

        Args:
            exclude_dirs: Set of directory names to exclude.
                          If None, uses DEFAULT_EXCLUDES.
        """
        self.exclude_dirs = exclude_dirs or self.DEFAULT_EXCLUDES

    def scan(self, vault_path: Path) -> Generator[Path, None, None]:
        """Yield all markdown files in the vault recursively.

        Args:
            vault_path: Path to the vault root directory.

        Yields:
            Path objects for each markdown file found.

        Raises:
            ValueError: If vault_path is not a directory.
        """
        import os

        if not vault_path.is_dir():
            raise ValueError(f"Vault path is not a directory: {vault_path}")

        for root_str, dirs, files in os.walk(vault_path):
            # Prune excluded directories in-place
            dirs[:] = [
                d for d in dirs if not d.startswith(".") and d not in self.exclude_dirs
            ]

            root_path = Path(root_str)
            for file in files:
                if file.endswith(".md") and not file.startswith("."):
                    yield root_path / file
