"""System editor utility."""

import os
import shlex
import subprocess
from pathlib import Path


class SystemEditor:
    """Handles interaction with system text editors."""

    @staticmethod
    def open_file(file_path: str | Path, editor_cmd: str | None = None) -> None:
        """Open file in the configured editor.

        Args:
            file_path: Path to file to open.
            editor_cmd: Optional editor command override.

        Raises:
            RuntimeError: If editor not found and fallback fails.
        """
        path_str = str(file_path)

        # Determine default editor based on OS
        default_editor = "notepad" if os.name == "nt" else "vim"

        # Resolve command: explicit -> env var -> fallback
        cmd_str: str = (
            editor_cmd
            or os.environ.get("DXVA_EDITOR")
            or os.environ.get("EDITOR", default_editor)
            or default_editor
        )

        parts = shlex.split(cmd_str, posix=(os.name != "nt"))
        if not parts:
            parts = [default_editor]

        cmd = parts + [path_str]

        try:
            # Use check_call to wait for editor to close
            subprocess.check_call(cmd, shell=(os.name == "nt"))
        except (FileNotFoundError, subprocess.CalledProcessError):
            # Fallback: try system default on Windows
            if os.name == "nt":
                try:
                    os.startfile(path_str)  # type: ignore[attr-defined]
                    return
                except Exception:
                    pass

            raise RuntimeError(
                f"Editor '{parts[0]}' not found and fallback failed."
            ) from None
