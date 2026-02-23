"""Configuration Editor TUI."""

from pathlib import Path

from rich.prompt import IntPrompt, Prompt

from dx_vault_atlas.shared import console as ui
from dx_vault_atlas.shared.config import (
    GlobalConfig,
    get_config_manager,
)
from dx_vault_atlas.shared.tui.config_wizard import run_setup_wizard


class ConfigEditor:
    """Handles interactive configuration editing."""

    def run(self) -> None:
        """Run the configuration editor loop."""
        config = self._ensure_config()
        if not config:
            return

        while True:
            self._show_main_menu()
            choice = IntPrompt.ask(
                "Select option", choices=["0", "1", "2", "3", "4"], default=4
            )

            if choice == 0:
                ui.console.print("[yellow]Changes discarded.[/yellow]")
                return

            if choice == 4:
                get_config_manager().save(config)
                ui.console.print("\n[green]✓ Configuration saved.[/green]")
                return

            self._handle_menu_choice(choice, config)

    def _ensure_config(self) -> GlobalConfig | None:
        """Ensure configuration exists, creating if needed."""
        manager = get_config_manager()
        if not manager.exists():
            ui.console.print(
                "[yellow]No configuration found. Starting setup...[/yellow]\n"
            )
            config = run_setup_wizard()
            if config:
                manager.save(config)
            return config
        return manager.load()

    def _handle_menu_choice(self, choice: int, config: GlobalConfig) -> None:
        """Handle main menu selection."""
        if choice == 1:
            self._edit_paths(config)
        elif choice == 2:
            self._edit_editor(config)
        elif choice == 3:
            self._edit_mappings(config)

    def _show_main_menu(self) -> None:
        """Display main menu options."""
        ui.console.clear()
        ui.console.rule("[bold]DX Vault Atlas · Configuration[/bold]")
        ui.console.print("\n[dim]Select a category to edit:[/dim]\n")
        ui.console.print("  [cyan]1.[/cyan] Paths (Vault & Inbox)")
        ui.console.print("  [cyan]2.[/cyan] Editor")
        ui.console.print(
            "  [cyan]3.[/cyan] Field Mappings [dim](Rename variables)[/dim]"
        )
        ui.console.print("  [cyan]4.[/cyan] Save & Exit")
        ui.console.print("  [cyan]0.[/cyan] Cancel (Discard changes)")
        ui.console.print()

    def _edit_paths(self, config: GlobalConfig) -> None:
        """Edit path settings."""
        while True:
            ui.console.clear()
            ui.console.rule("[bold]Paths Configuration[/bold]")
            ui.console.print(
                f"\n  [cyan]1.[/cyan] Vault Path: [green]{config.vault_path}[/green]"
            )
            ui.console.print(
                f"  [cyan]2.[/cyan] Inbox Path: [green]{config.vault_inbox}[/green]"
            )
            ui.console.print("  [cyan]0.[/cyan] Back")
            ui.console.print()

            sub_choice = IntPrompt.ask(
                "Select option", choices=["0", "1", "2"], default=0
            )

            if sub_choice == 0:
                break

            if sub_choice == 1:
                self._update_path(config, "vault_path", "New Vault Path")
            elif sub_choice == 2:
                self._update_path(config, "vault_inbox", "New Inbox Path")

    def _update_path(self, config: GlobalConfig, attr: str, prompt: str) -> None:
        """Update a path attribute with validation."""
        current_val = getattr(config, attr)
        new_val = Prompt.ask(prompt, default=str(current_val))
        try:
            GlobalConfig.validate_path(Path(new_val))
            setattr(config, attr, Path(new_val))
        except Exception as e:
            ui.console.print(f"[red]Invalid path: {e}[/red]")
            Prompt.ask("Press Enter to continue")

    def _edit_editor(self, config: GlobalConfig) -> None:
        """Edit editor setting."""
        new_editor = Prompt.ask("Editor Command", default=config.editor)
        config.editor = new_editor

    def _edit_mappings(self, config: GlobalConfig) -> None:
        """Edit field mappings."""
        while True:
            ui.console.clear()
            ui.console.rule("[bold]Field Mappings (Rename)[/bold]")
            ui.console.print(
                "\n[dim]Define how legacy fields should be renamed "
                "(Old -> New).[/dim]\n"
            )

            if not config.field_mappings:
                ui.console.print("  [dim]No mappings defined.[/dim]")
            else:
                for i, (old, new) in enumerate(config.field_mappings.items(), 1):
                    ui.console.print(
                        f"  {i}. [yellow]{old}[/yellow] → [green]{new}[/green]"
                    )

            ui.console.print("\n  [cyan]A.[/cyan] Add Mapping")
            ui.console.print("  [cyan]D.[/cyan] Delete Mapping")
            ui.console.print("  [cyan]0.[/cyan] Back")
            ui.console.print()

            action = Prompt.ask(
                "Select action", choices=["0", "a", "A", "d", "D"], default="0"
            ).lower()

            if action == "0":
                break

            if action == "a":
                self._add_mapping(config)
            elif action == "d":
                self._delete_mapping(config)

    def _add_mapping(self, config: GlobalConfig) -> None:
        """Add a new field mapping."""
        old_key = Prompt.ask("Old field name (e.g. date)")
        if old_key:
            new_key = Prompt.ask(f"New field name for '{old_key}' (e.g. created)")
            if new_key:
                config.field_mappings[old_key] = new_key

    def _delete_mapping(self, config: GlobalConfig) -> None:
        """Delete an existing field mapping."""
        if not config.field_mappings:
            return

        key_to_del = Prompt.ask(
            "Enter old field name to delete (or leave empty to cancel)"
        )
        if key_to_del in config.field_mappings:
            del config.field_mappings[key_to_del]
            ui.console.print(f"[yellow]Deleted mapping for {key_to_del}[/yellow]")
        elif key_to_del:
            ui.console.print("[red]Mapping not found.[/red]")
            Prompt.ask("Press Enter to continue")
