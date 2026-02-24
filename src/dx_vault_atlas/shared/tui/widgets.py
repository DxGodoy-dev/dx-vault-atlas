"""Reusable TUI widgets."""

from enum import Enum
from typing import Any

from rich.text import Text
from textual.binding import Binding
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option


class VimOptionList(OptionList):
    """OptionList with vim-style hjkl navigation.

    Supports:
    - j/k or ↑/↓ for navigation
    - Enter or Space to select
    """

    BINDINGS = [
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
        Binding("down", "cursor_down", "Down", show=False),
        Binding("up", "cursor_up", "Up", show=False),
        Binding("enter", "select", "Select", show=False),
        Binding("space", "select", "Select", show=False),
    ]


class StepDone(Static):
    """Display a completed wizard step."""

    def __init__(self, label: str, value: str, **kwargs: Any) -> None:  # noqa: ANN401
        """Initialize step.

        Args:
            label: Step label (e.g. "Title").
            value: Selected value.
            **kwargs: Additional arguments for Static widget.
        """
        super().__init__(
            f"[dim]●[/] {label} [cyan]{value}[/]", classes="step-done", **kwargs
        )


def create_enum_options[E: Enum](
    enum_cls: type[E],
    default_idx: int,
    id_prefix: str,
) -> tuple[list[Option], int]:
    """Create options list from enum.

    Args:
        enum_cls: Enum class to create options from.
        default_idx: Index of default option.
        id_prefix: Prefix for option IDs.

    Returns:
        Tuple of (options list, default index).
    """
    from dx_vault_atlas.shared.console import format_enum_label

    options = []
    for i, member in enumerate(enum_cls):
        display, _ = format_enum_label(member, is_default=(i == default_idx))
        if i == default_idx:
            display = f"{display} [dim](default)[/]"
        options.append(Option(Text.from_markup(display), id=f"{id_prefix}-{i}"))
    return options, default_idx


def create_vim_option_list(
    enum_cls: type,
    default_idx: int,
    id_prefix: str,
    widget_id: str | None = None,
) -> VimOptionList:
    """Create VimOptionList from enum.

    Args:
        enum_cls: Enum class to create options from.
        default_idx: Index of default option.
        id_prefix: Prefix for option IDs (used as list ID if widget_id not provided).
        widget_id: Optional custom ID for the widget.
            If None, uses f"{id_prefix}-options".

    Returns:
        Configured VimOptionList.
    """
    options, default = create_enum_options(enum_cls, default_idx, id_prefix)
    list_id = widget_id if widget_id is not None else f"{id_prefix}-options"
    opt_list = VimOptionList(*options, id=list_id)
    opt_list.highlighted = default
    return opt_list
