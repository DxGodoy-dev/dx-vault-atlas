"""UI service protocol and implementations for note migrator."""

from typing import Any

from dx_vault_atlas.services.note_migrator.core.interfaces import IUserInterface
from dx_vault_atlas.shared import console as ui


class CliUserInterface(IUserInterface):
    """Command-line implementation of UserInterface using rich console."""

    def show_header(self, title: str = "") -> None:
        """Display a rich header."""
        if title:
            ui.show_header(title)
        else:
            ui.show_header("Note Migrator")

    def confirm(self, message: str) -> bool:
        """Prompt for confirmation using rich."""
        return ui.confirm(message, default=False)

    def print_summary(self, data: dict[str, Any]) -> None:
        """Print formatted summary data."""
        ui.console.print("\n[bold]Migration Summary:[/bold]")

        # Example mapping of keys to styles, assuming basic stats
        for key, value in data.items():
            if (
                "migrated" in key.lower()
                or "updated" in key.lower()
                or "success" in key.lower()
            ):
                ui.console.print(f"[green]✓[/green] {value} {key}")
            elif "skip" in key.lower():
                ui.console.print(f"[dim]•[/dim] {value} {key}")
            elif "error" in key.lower() or "fail" in key.lower():
                ui.console.print(f"[red]✗[/red] {value} {key}")
            else:
                ui.console.print(f"[cyan]-[/cyan] {value} {key}")

    def display_message(self, msg: str) -> None:
        """Display a general message using rich console."""
        ui.console.print(msg)
