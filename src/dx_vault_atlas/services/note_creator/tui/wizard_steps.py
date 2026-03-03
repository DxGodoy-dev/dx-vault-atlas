"""TUI steps for gathering note creation data."""

from collections.abc import Callable
from pathlib import Path
from typing import Any

from dx_vault_atlas.services.note_creator.core.registry import has_field
from dx_vault_atlas.services.note_creator.defaults import (
    DEFAULT_AREA,
    DEFAULT_PRIORITY,
    DEFAULT_TAGS,
    DEFAULT_TEMPLATE,
)
from dx_vault_atlas.services.note_creator.models.enums import (
    NoteArea,
    NoteTemplate,
    Priority,
)
from dx_vault_atlas.services.note_creator.services.console import ConsoleInterface


def _get_workflow_info() -> dict[str, Any]:
    """Get workflow fields (priority)."""
    return {
        "priority": ConsoleInterface.choose_enum(
            "Priority", Priority, default=DEFAULT_PRIORITY
        ),
    }


def _get_context_info() -> dict[str, Any]:
    """Get context fields (area)."""
    return {
        "area": ConsoleInterface.choose_enum("Area", NoteArea, default=DEFAULT_AREA)
    }


def get_note_wizard_data(raw_title: str) -> dict[str, Any]:
    """Run the interactive wizard to collect note data.

    Args:
        raw_title: Raw note title from user input.

    Returns:
        Dictionary with all collected data for note creation.
    """
    # 1. Select template first
    template = ConsoleInterface.choose_enum(
        "Template", NoteTemplate, default=DEFAULT_TEMPLATE
    )

    # 2. Build base data
    note_data: dict[str, Any] = {
        "title": f'"{raw_title}"',
        "aliases": [raw_title],
        "tags": DEFAULT_TAGS,
        "type": Path(template.value).stem,
        "template_type": template,  # Keep track of template for factory
    }

    # 3. Execute dynamic steps based on model fields
    steps: list[Callable[[], dict[str, Any]]] = []

    if has_field(template, "priority"):
        steps.append(_get_workflow_info)

    if has_field(template, "area"):
        steps.append(_get_context_info)

    for step_func in steps:
        note_data.update(step_func())

    return note_data
