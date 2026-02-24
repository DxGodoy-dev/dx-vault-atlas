"""Note writer service for persisting notes to disk."""

from pathlib import Path


class NoteWriter:
    """Handles writing note string content to the filesystem."""

    def write(self, content: str, path: Path) -> Path:
        """Write content to disk.

        Args:
            content: Note string content to write.
            path: Target file path.

        Returns:
            The Path where the note was saved.

        Raises:
            FileExistsError: If a file already exists at the target path.
        """
        if path.exists():
            msg = f"Note already exists at: {path}"
            raise FileExistsError(msg)
        path.write_text(content, encoding="utf-8")
        return path
