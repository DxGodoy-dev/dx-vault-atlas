"""File Repository service for the note migrator."""

from pathlib import Path
from typing import Protocol


class FileRepository(Protocol):
    """Protocol for file input/output operations."""

    def read_text(self, path: Path) -> str:
        """Read text content from a file.

        Args:
            path: The path to the file.

        Returns:
            The content of the file as a string.
        """
        ...

    def target_exists(self, path: Path) -> bool:
        """Check if a target file already exists.

        Args:
            path: The path to the file.

        Returns:
            True if the file exists, False otherwise.
        """
        ...

    def write_text(self, path: Path, content: str) -> None:
        """Write text content to a file.

        Args:
            path: The path to the file.
            content: The text content to write.
        """
        ...


class LocalFileRepository:
    """Implementation of FileRepository that uses the local filesystem."""

    def read_text(self, path: Path) -> str:
        """Read text from a local file using UTF-8 encoding."""
        return path.read_text(encoding="utf-8")

    def target_exists(self, path: Path) -> bool:
        """Check if a local file exists."""
        return path.exists()

    def write_text(self, path: Path, content: str) -> None:
        """Write text to a local file using UTF-8 encoding."""
        path.write_text(content, encoding="utf-8")
