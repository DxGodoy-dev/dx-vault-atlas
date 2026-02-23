"""Migration domain exceptions."""

from pathlib import Path


class MigrationError(Exception):
    """Base exception for migration failures."""

    def __init__(self, file_path: Path, message: str) -> None:
        """Initialize migration error.

        Args:
            file_path: Path to the affected file.
            message: Error description.
        """
        self.file_path = file_path
        self.message = message
        super().__init__(f"{file_path}: {message}")


class FileReadError(MigrationError):
    """Raised when a note file cannot be read."""


class FrontmatterParseError(MigrationError):
    """Raised when YAML frontmatter parsing fails."""


class MissingFieldsError(MigrationError):
    """Raised when required fields are missing after user input."""

    def __init__(self, file_path: Path, missing_fields: list[str]) -> None:
        """Initialize missing fields error.

        Args:
            file_path: Path to the affected file.
            missing_fields: List of missing field names.
        """
        self.missing_fields = missing_fields
        super().__init__(
            file_path, f"Missing required fields: {', '.join(missing_fields)}"
        )


class EditorCancelledError(MigrationError):
    """Raised when user cancels editor input."""
