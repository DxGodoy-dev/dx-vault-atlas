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
        if not vault_path.is_dir():
            raise ValueError(f"Vault path is not a directory: {vault_path}")

        # rglob is recursive. We must filter manually for excluded dirs.
        # Alternatively, we can use os.walk to prune directories for performance,
        # but rglob is simpler and usually fast enough for typical vaults.
        for file_path in vault_path.rglob("*.md"):
            if self._is_excluded(file_path, vault_path):
                continue
            yield file_path

    def _is_excluded(self, file_path: Path, vault_path: Path) -> bool:
        """Check if file is in an excluded directory relative to vault."""
        try:
            rel_path = file_path.relative_to(vault_path)
        except ValueError:
            # Should not happen if scanning properly
            return True

        # Check each part of the path relative to the vault root
        for part in rel_path.parts:
            # Skip hidden directories (starting with .)
            if part.startswith("."):
                return True
            # Skip explicitly excluded directories
            if part in self.exclude_dirs:
                return True
        return False
