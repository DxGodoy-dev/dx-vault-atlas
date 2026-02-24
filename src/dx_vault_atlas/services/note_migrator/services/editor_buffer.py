"""Editor buffer service for manual note classification."""

import tempfile
from pathlib import Path
from typing import Any

from dx_vault_atlas.services.note_migrator.services.yaml_parser import (
    YamlParseError,
    YamlParserService,
)
from dx_vault_atlas.shared.core.system_editor import SystemEditor


class EditorAbortedError(Exception):
    """Raised when user closes editor without valid changes."""


class EditorBufferService:
    """Creates temp buffer for manual note classification ("Rock" logic).

    Opens the system editor with a pre-filled buffer containing the original
    note content and prompts for missing fields.
    """

    def __init__(self, editor: str = "vim") -> None:
        """Initialize with editor command.

        Args:
            editor: Editor command (e.g., "vim", "code --wait").
        """
        self.editor = editor
        self.yaml_parser = YamlParserService()

    def prompt_user(
        self,
        original_content: str,
        frontmatter: dict[str, Any],
        missing_fields: list[str],
    ) -> dict[str, Any]:
        """Open editor for user to fill missing fields.

        Args:
            original_content: Original markdown file content.
            frontmatter: Current frontmatter (may be empty).
            missing_fields: List of field names that need to be filled.

        Returns:
            Updated frontmatter dictionary after user edits.

        Raises:
            EditorAbortedError: If user closes without saving or leaves
                required fields empty.
        """
        buffer_content = self._create_buffer(
            original_content, frontmatter, missing_fields
        )

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".md",
            delete=False,
            encoding="utf-8",
        ) as tmp:
            tmp.write(buffer_content)
            tmp_path = Path(tmp.name)

        try:
            self._open_editor(str(tmp_path))
            return self._parse_buffer(tmp_path)
        finally:
            tmp_path.unlink(missing_ok=True)

    def _create_buffer(
        self,
        original_content: str,
        frontmatter: dict[str, Any],
        missing_fields: list[str],
    ) -> str:
        """Create the editor buffer with instructions."""
        # Build header with missing field prompts
        header_lines = ["---"]
        header_lines.append("# FILL THE MISSING FIELDS BELOW:")

        for field in missing_fields:
            current_value = frontmatter.get(field, "")
            header_lines.append(f"{field}: {current_value}  # <- REQUIRED")

        header_lines.append("---")
        header_lines.append("")
        header_lines.append("# === ORIGINAL CONTENT (for reference) ===")
        header_lines.append("")

        return "\n".join(header_lines) + original_content

    def _open_editor(self, file_path: str) -> None:
        """Open the configured editor and wait for it to close."""
        try:
            SystemEditor.open_file(file_path, editor_cmd=self.editor)
        except RuntimeError as e:
            # Re-raise as EditorAbortedError for consistency with existing error handling logic
            raise EditorAbortedError(str(e)) from e

    def _parse_buffer(self, buffer_path: Path) -> dict[str, Any]:
        """Parse the edited buffer and extract frontmatter.

        Raises:
            EditorAbortedError: If YAML is invalid or file wasn't saved.
        """
        content = buffer_path.read_text(encoding="utf-8")

        # Guard: File is empty  # noqa: ERA001
        if not content.strip():
            msg = "Editor buffer is empty. Did you save the file?"
            raise EditorAbortedError(msg)

        try:
            parsed = self.yaml_parser.parse(content)
        except YamlParseError as e:
            msg = f"Invalid YAML in editor buffer: {e}"
            raise EditorAbortedError(msg) from e

        # Guard: No frontmatter
        if not parsed.has_yaml:
            msg = "No YAML frontmatter found in editor buffer."
            raise EditorAbortedError(msg)

        return parsed.frontmatter
