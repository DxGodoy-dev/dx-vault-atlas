"""Base TUI application with shared configuration."""

from collections.abc import Iterable

from textual.app import App, ComposeResult, SystemCommand
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Footer, Static

from dx_vault_atlas.shared.tui.theme import ThemeManager


class BaseApp(App[None]):
    """Base TUI application with common bindings and styling.

    Features:
    - Alternative Screen Buffer (automatic in Textual)
    - Q/Ctrl+Q/Escape to quit
    - Ctrl+P to cycle themes
    - F11 to toggle maximize
    - Catppuccin theme support
    - Header panel
    """

    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("ctrl+q", "quit", "Quit", show=False),
        Binding("escape", "quit", "Cancel", show=False),
        Binding("ctrl+p", "cycle_theme", "Theme", show=True),
        Binding("f11", "toggle_maximize", "Maximize", show=True),
    ]

    # Dynamic CSS from ThemeManager
    CSS = ThemeManager.get_css()

    # Override in subclass
    HEADER_TITLE = "DX Vault Atlas"

    def compose(self) -> ComposeResult:
        """Compose base layout with header and wizard container."""
        with Container(id="header-panel"):
            yield Static(self.HEADER_TITLE, id="header-title")
        with Vertical(id="wizard"):
            pass
        yield Footer()

    @property
    def wizard(self) -> Vertical:
        """Get wizard container for convenience."""
        return self.query_one("#wizard", Vertical)

    def clear_wizard(self) -> None:
        """Clear all children from wizard container."""
        self.wizard.remove_children()

    def action_cycle_theme(self) -> None:
        """Cycle through available themes."""
        new_theme = ThemeManager.cycle_theme()
        # Update CSS and force re-render
        self.CSS = ThemeManager.get_css()
        self.refresh_css()
        self.notify(f"Theme: {new_theme.title()}", timeout=1)

    def action_toggle_maximize(self) -> None:
        """Toggle maximize state on wizard container."""
        wizard = self.query_one("#wizard", Vertical)
        if wizard.has_class("maximized"):
            wizard.remove_class("maximized")
        else:
            wizard.add_class("maximized")

    def get_system_commands(self, screen: Screen) -> Iterable[SystemCommand]:
        """Override standard textual commands for the command palette.

        Removes default theme/screenshot/maximize commands and adds skip.
        """
        yield SystemCommand(
            "Quit",
            "Quit the application as soon as possible",
            self.action_quit,
        )

        if screen.query("HelpPanel"):
            yield SystemCommand(
                "Keys",
                "Hide the keys and widget help panel",
                self.action_hide_help_panel,
            )
        else:
            yield SystemCommand(
                "Keys",
                "Show help for the focused widget and a summary of available keys",
                self.action_show_help_panel,
            )

        yield SystemCommand(
            "Skip",
            "Skip the current step",
            self.action_skip,
        )

    def action_skip(self) -> None:
        """Skip the current step. Override in subclass if supported."""
        pass
