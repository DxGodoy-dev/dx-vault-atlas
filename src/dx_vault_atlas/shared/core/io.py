"""Shared I/O and File Repository utilities for reading/writing notes."""

from pathlib import Path
from typing import Any, Protocol

from dx_vault_atlas.shared.yaml_parser import (
    ParsedNote,
    YamlParserService,
)
from dx_vault_atlas.shared.logger import logger


class FileRepository(Protocol):
    """Protocol for basic file input/output operations."""

    def read_text(self, path: Path) -> str:
        """Read text content from a file."""
        ...

    def target_exists(self, path: Path) -> bool:
        """Check if a target file already exists."""
        ...

    def write_text(self, path: Path, content: str) -> None:
        """Write text content to a file."""
        ...


class LocalFileRepository(FileRepository):
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


class NoteIOService:
    """Handles reading, writing, and renaming markdown notes with YAML frontmatter."""

    def __init__(
        self, yaml_parser: YamlParserService, file_repo: FileRepository | None = None
    ) -> None:
        """Initialise NoteIOService with dependencies.

        Args:
            yaml_parser: Service to parse and serialize YAML frontmatter.
            file_repo: File repository for raw I/O. Defaults to LocalFileRepository.
        """
        self.yaml_parser = yaml_parser
        self.file_repo = file_repo or LocalFileRepository()

    def read_note(self, note_path: Path) -> ParsedNote | None:
        """Read a note and parse its frontmatter."""
        try:
            content = self.file_repo.read_text(note_path)
            return self.yaml_parser.parse(content)
        except Exception as e:
            logger.error(f"Error reading {note_path.name}: {e}")
            return None

    def write_note(
        self,
        file_path: Path,
        frontmatter: dict[str, Any],
        body: str,
    ) -> bool:
        """Write updated frontmatter and body to a note."""
        try:
            yaml_content = self.yaml_parser.serialize_frontmatter(frontmatter)
            self.file_repo.write_text(file_path, yaml_content + body)
            return True
        except Exception as e:
            logger.error(f"Error writing {file_path.name}: {e}")
            return False

    def rename_note(self, old_path: Path, new_path: Path) -> bool:
        """Rename a note file."""
        if old_path == new_path:
            return True
        try:
            old_path.rename(new_path)
            return True
        except Exception as e:
            logger.error(f"Error renaming {old_path.name} to {new_path.name}: {e}")
            return False
