"""Shared console interface for interactive CLI using questionary and Rich."""

from enum import Enum
from typing import TypeVar

import questionary
from questionary import Choice
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

_E = TypeVar("_E", bound=Enum)

console = Console()

# Style for questionary prompts
MENU_STYLE = questionary.Style(
    [
        ("qmark", "bold cyan"),
        ("question", ""),
        ("pointer", "bold cyan"),
        ("highlighted", "bold"),
        ("selected", "cyan"),
        ("answer", "bold cyan"),
    ]
)


class UserQuitError(Exception):
    """Raised when user quits with q or Ctrl+Q."""


def _format_enum_label(member: Enum, is_default: bool = False) -> tuple[str, bool]:
    """Format enum member for display with optional default marker.

    Args:
        member: Enum member to format.
        is_default: Whether this is the default option.

    Returns:
        Capitalized display string with colored (default) marker.
    """
    if isinstance(member.value, str):
        display = member.value.replace(".md", "").title()
    else:
        display = f"{member.name.title()} ({member.value})"

    return display, is_default


def show_header(subtitle: str = "") -> None:
    """Display application header panel."""
    title = Text("DX Vault Atlas", style="bold cyan")
    if subtitle:
        title.append(f" · {subtitle}", style="dim")

    panel = Panel(title, border_style="cyan", padding=(0, 2))
    console.print()
    console.print(panel)
    console.print()


def success_message(title: str, path: str, action: str = "created") -> None:
    """Display styled success message."""
    console.print()
    console.print(
        f'[bold cyan]●[/] Note "[bold]{title}[/]" {action} at: [cyan]{path}[/]'
    )
    console.print()


def error_message(message: str) -> None:
    """Display styled error message."""
    console.print()
    console.print(f"[bold red]✗[/] {message}")
    console.print()


def warning_message(message: str) -> None:
    """Display styled warning message."""
    console.print(f"[yellow]![/] {message}")


def info_message(message: str) -> None:
    """Display styled info message."""
    console.print(f"[cyan]●[/] {message}")


def query(prompt_text: str, default: str = "", allow_empty: bool = False) -> str:
    """Query user for text input. Ctrl+Q to quit.

    Args:
        prompt_text: The prompt message.
        default: Default value.
        allow_empty: Allow empty response.

    Returns:
        User input string.

    Raises:
        UserQuitError: If user presses Ctrl+Q.
        KeyboardInterrupt: If user presses Ctrl+C.
    """
    result = questionary.text(
        prompt_text,
        default=default,
        qmark="●",
        style=MENU_STYLE,
    ).ask()

    if result is None:
        raise KeyboardInterrupt

    # Check for quit command
    if result.strip().lower() == "q":
        raise UserQuitError()

    if not allow_empty and not result.strip():
        warning_message("Input cannot be empty.")
        return query(prompt_text, default=default, allow_empty=allow_empty)

    return result.strip()


def choose_enum[E: Enum](
    label: str,
    enum_cls: type[E],
    default_index: int = 0,
    show_quit: bool = True,
) -> E:
    """Show arrow-key selection menu for enum values. Q to quit.

    Args:
        label: Menu title.
        enum_cls: Enum class to display.
        default_index: Default selection index.
        show_quit: Show quit instruction.

    Returns:
        Selected enum member.

    Raises:
        UserQuitError: If user presses Q.
    """
    members = list(enum_cls)

    # Build choices with display names
    choices = []
    for i, m in enumerate(members):
        is_default = i == default_index
        display, _ = _format_enum_label(m, is_default)
        if is_default:
            display = f"{display} [dim](default)[/dim]"
        choices.append(Choice(title=display, value=m))

    # Add quit option
    if show_quit:
        choices.append(Choice(title="[dim]Quit (q)[/dim]", value="__quit__"))

    prompt_label = label
    if show_quit:
        prompt_label = f"{label} [dim](q to quit)[/dim]"

    result = questionary.select(
        prompt_label,
        choices=choices,
        default=choices[default_index] if choices else None,
        qmark="●",
        style=MENU_STYLE,
        use_shortcuts=False,
    ).ask()

    if result is None:
        raise KeyboardInterrupt

    if result == "__quit__":
        raise UserQuitError()

    return result


def confirm(message: str, default: bool = True) -> bool:
    """Ask for confirmation."""
    result = questionary.confirm(
        message,
        default=default,
        qmark="●",
        style=MENU_STYLE,
    ).ask()

    if result is None:
        raise KeyboardInterrupt
    return result


def show_preview(title: str, content: str, max_lines: int = 5) -> None:
    """Show a preview panel of content.

    Args:
        title: Panel title.
        content: Content to preview.
        max_lines: Maximum lines to show.
    """
    lines = content.strip().split("\n")[:max_lines]
    preview_text = "\n".join(lines)
    if len(content.strip().split("\n")) > max_lines:
        preview_text += "\n[dim]...[/dim]"

    panel = Panel(preview_text, title=title, border_style="dim", padding=(0, 1))
    console.print(panel)
