"""Protocols and interfaces for the note migrator service."""

from collections.abc import Generator
from pathlib import Path
from typing import Any, Protocol

from dx_vault_atlas.services.note_migrator.services.yaml_parser import ParsedNote


class IYamlParser(Protocol):
    """Protocol for parsing and serializing YAML frontmatter."""

    def parse(self, content: str) -> ParsedNote:
        """Parse markdown content into frontmatter and body."""
        ...

    def serialize_frontmatter(
        self, frontmatter: dict[str, str | int | list[str] | None]
    ) -> str:
        """Convert frontmatter dict back to YAML string."""
        ...


class IEditorService(Protocol):
    """Protocol for prompting the user via an editor buffer."""

    def prompt_user(
        self,
        original_content: str,
        frontmatter: dict[str, Any],
        missing_fields: list[str],
    ) -> dict[str, Any]:
        """Open editor for user to fill missing fields."""
        ...


class ITypeHeuristics(Protocol):
    """Protocol for detecting note types."""

    def detect_type(self, frontmatter: dict[str, object]) -> str | None:
        """Extracts the note type from frontmatter 'type' field."""
        ...


class ISchemaUpgrader(Protocol):
    """Protocol for upgrading note schema to the current version."""

    def upgrade(self, frontmatter: dict[str, Any]) -> dict[str, Any]:
        """Upgrade frontmatter to current schema version and clean fields."""
        ...


class ITransformer(Protocol):
    """Protocol for handling core migration transformation logic."""

    def transform(
        self,
        frontmatter: dict[str, Any],
        file_path: Path,
        rename_only: bool = False,
        debug_mode: bool = False,
    ) -> tuple[dict[str, Any], bool]:
        """Apply migration transformations to frontmatter."""
        ...


class IScanner(Protocol):
    """Protocol for scanning the vault for markdown files."""

    def scan(self, vault_path: Path) -> Generator[Path, None, None]:
        """Yield all markdown files in the vault recursively."""
        ...


class IUserInterface(Protocol):
    """Protocol for user interface interactions."""

    def show_header(self, title: str = "") -> None:
        """Display a header to the user."""
        ...

    def confirm(self, message: str) -> bool:
        """Prompt the user for confirmation."""
        ...

    def print_summary(self, data: dict[str, Any]) -> None:
        """Print a summary of an operation."""
        ...

    def log_error(self, msg: str) -> None:
        """Log or display an error message."""
        ...

    def display_message(self, msg: str) -> None:
        """Display a general message to the user."""
        ...
