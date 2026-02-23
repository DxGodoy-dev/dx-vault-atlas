"""Simple Result TUI for success screen."""

from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.widgets import Footer, Label, Static

from dx_vault_atlas.shared.tui.theme import ThemeManager


class ResultApp(App[str]):
    """TUI for showing success result.

    Returns 'retry' or 'quit' string on exit.
    """

    BINDINGS = [
        Binding("q", "quit_app", "Quit", show=True),
        Binding("s", "retry", "Create Another", show=True),
    ]

    CSS = ThemeManager.get_css()

    def __init__(self, note_path: Path) -> None:
        """Initialize with created note path."""
        super().__init__()
        self.note_path = note_path

    def compose(self) -> ComposeResult:
        """Compose the result screen."""
        with Container(id="header-panel"):
            yield Static("DX Vault Atlas · Success", id="header-title")
        with Vertical(id="wizard"):
            yield Label(
                "[bold green]✓ Note Created Successfully![/]", classes="success-title"
            )
            yield Static(f"Path: [cyan]{self.note_path}[/]", classes="path-display")
            yield Static(
                "\nPress [bold]q[/] to quit, [bold]s[/] to create another note.",
                classes="instructions",
            )
        yield Footer()

    def action_retry(self) -> None:
        """Exit with retry signal."""
        self.exit("retry")

    def action_quit_app(self) -> None:
        """Exit with quit signal."""
        self.exit("quit")


def run_result_tui(note_path: Path) -> str:
    """Run result TUI and return action ('quit' or 'retry')."""
    app = ResultApp(note_path)
    result = app.run()
    return result if isinstance(result, str) else "quit"
