"""UI utilities - re-exports from console module for backwards compatibility."""

from dx_vault_atlas.shared.console import (
    UserQuit,
    choose_enum,
    confirm,
    console,
    error_message,
    info_message,
    query,
    show_header,
    show_preview,
    success_message,
    warning_message,
)

__all__ = [
    "UserQuit",
    "choose_enum",
    "confirm",
    "console",
    "error_message",
    "info_message",
    "query",
    "show_header",
    "show_preview",
    "success_message",
    "warning_message",
]
