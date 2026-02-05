import os
import shlex
import subprocess


class TextEditor:
    """Handles interaction with system text editors."""

    @staticmethod
    def open_file(file_path: str, editor: str | None = None) -> None:
        """Opens the given file in the configured editor and blocks until it is closed.

        Uses the EDITOR environment variable if editor is not passed; defaults to "vim".

        Args:
            file_path: Absolute or relative path to the file to edit.
            editor: Editor command (e.g. "vim", "code --wait"). If None, uses os.environ["EDITOR"]
                or "vim".

        Raises:
            RuntimeError: If the editor executable is not found or not on PATH.
        """
        cmd_str: str = editor or os.environ.get("EDITOR", "vim") or "vim"
        parts = shlex.split(cmd_str)
        if not parts:
            parts = ["vim"]
        cmd = parts + [file_path]
        try:
            subprocess.call(cmd)
        except FileNotFoundError:
            raise RuntimeError(
                f"Editor '{parts[0]}' not found. Set EDITOR or install the desired editor."
            )

    @staticmethod
    def open_vim(file_path: str) -> None:
        """Opens the given file in Vim. Prefer open_file() to respect EDITOR."""
        TextEditor.open_file(file_path, editor="vim")
