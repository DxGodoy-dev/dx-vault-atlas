"""Console interface for interactive CLI using questionary and Rich."""

from enum import Enum
from typing import TypeVar

import questionary
from rich.console import Console

_E = TypeVar("_E", bound=Enum)

console = Console()

# Custom questionary style: highlighted text changes color
MENU_STYLE = questionary.Style(
    [
        ("qmark", "bold cyan"),
        ("question", ""),
        ("pointer", "bold cyan"),
        ("highlighted", "bold cyan"),
        ("selected", "cyan"),
        ("answer", "bold cyan"),
    ]
)


def _format_enum_label(member: Enum, is_default: bool = False) -> str:
    """Format enum member for display with optional default marker.

    Args:
        member: Enum member to format.
        is_default: Whether this is the default option.

    Returns:
        Capitalized display string with optional (default) marker.
    """
    if isinstance(member.value, str) and member.value:
        # Strip .md extension for template names
        display = member.value.replace(".md", "").title()
    else:
        # Fallback to name for empty strings (e.g. OTHER="") or non-strings
        display = member.name.title()

    if is_default:
        display = f"{display} (default)"

    return display


class ConsoleInterface:
    """Service for clean I/O operations with modern interactive prompts."""

    @staticmethod
    def query(prompt_text: str) -> str:
        """Query user for text input.

        Args:
            prompt_text: The prompt message.

        Returns:
            User input string.
        """
        result = questionary.text(
            prompt_text,
            qmark="●",
            style=MENU_STYLE,
        ).ask()

        if result is None:
            raise KeyboardInterrupt
        return result

    @staticmethod
    def choose_enum(label: str, enum_cls: type[_E], default: _E | None = None) -> _E:
        """Show arrow-key selection menu for enum values.

        Args:
            label: Menu title.
            enum_cls: Enum class to display.
            default: Default selection (Enum member).

        Returns:
            Selected enum member.
        """
        members = list(enum_cls)

        # Build choices with capitalized display names and default marker
        choices = []
        default_choice = None

        for m in members:
            # Check if this member matches the default
            is_default = (default is not None) and (m == default)
            display = _format_enum_label(m, is_default)

            choice = questionary.Choice(title=display, value=m)
            choices.append(choice)

            if is_default:
                default_choice = choice

        # If no default explicitly matched, but we have choices, optional: default to first?
        # Questionary defaults to first if 'default' param is None.

        result = questionary.select(
            label,
            choices=choices,
            default=default_choice,
            qmark="●",
            style=MENU_STYLE,
        ).ask()

        if result is None:
            raise KeyboardInterrupt
        return result

    @staticmethod
    def confirm(message: str, default: bool = True) -> bool:
        """Ask for confirmation.

        Args:
            message: Confirmation prompt.
            default: Default value.

        Returns:
            True if confirmed, False otherwise.
        """
        result = questionary.confirm(
            message,
            default=default,
            qmark="●",
            style=MENU_STYLE,
        ).ask()

        if result is None:
            raise KeyboardInterrupt
        return result
