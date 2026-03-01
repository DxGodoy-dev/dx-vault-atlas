"""Note I/O Service for file operations."""

from pathlib import Path
from typing import Any

from dx_vault_atlas.services.note_migrator.services.yaml_parser import (
    ParsedNote,
    YamlParserService,
)
from dx_vault_atlas.shared.logger import logger


class NoteIOService:
    """Handles reading, writing, and renaming markdown notes."""

    def __init__(self, yaml_parser: YamlParserService) -> None:
        """Initialise NoteIOService with YAML parser."""
        self.yaml_parser = yaml_parser

    def read_note(self, note_path: Path) -> ParsedNote | None:
        """Read a note and parse its frontmatter."""
        try:
            content = note_path.read_text(encoding="utf-8")
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
            file_path.write_text(yaml_content + body, encoding="utf-8")
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
