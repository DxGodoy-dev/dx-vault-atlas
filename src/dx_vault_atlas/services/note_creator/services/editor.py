"""Service for external editor operations."""

import tempfile
from contextlib import suppress
from pathlib import Path

from dx_vault_atlas.shared.core.system_editor import SystemEditor


class EditorService:
    """Handles external editor interactions."""

    def get_editor_content(self) -> str:
        """Open temporary file in editor and return content."""
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as tf:
            temp_path = tf.name

        try:
            # Open editor (blocks until closed)
            SystemEditor.open_file(temp_path)

            # Read content
            return Path(temp_path).read_text(encoding="utf-8")
        finally:
            # Cleanup
            with suppress(OSError):
                Path(temp_path).unlink()
