"""Ports (interfaces/protocols) for the Note Creator module."""

from pathlib import Path
from typing import Protocol

from dx_vault_atlas.services.note_creator.models.note import BaseNote


class ITemplatingService(Protocol):
    """Interface for rendering templates."""

    def render(self, template_name: str, note_data: BaseNote) -> str:
        """Render a template with note data."""
        ...


class INoteWriter(Protocol):
    """Interface for persisting notes."""

    def write(self, content: str, path: Path) -> Path:
        """Write note content to a path."""
        ...


class INoteProcessor(Protocol):
    """Interface for processing notes."""

    def render_note(
        self,
        template_name: str,
        note_data: BaseNote,
        body_content: str = "",
    ) -> str:
        """Render note content from template and variables."""
        ...


class IOutputPresenter(Protocol):
    """Interface for presenting UI elements to the user."""

    def present_error(self, error: Exception) -> None:
        """Display an error to the user."""
        ...
