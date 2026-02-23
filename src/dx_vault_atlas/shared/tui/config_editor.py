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
                "Select option",
                choices=["0", "1", "2", "3", "4", "5"],
                default=5,
            )

            if choice == 0:
                ui.console.print("[yellow]Changes discarded.[/yellow]")
                return

            if choice == 5:
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
        elif choice == 4:
            self._edit_value_mappings(config)

    def _show_main_menu(self) -> None:
        """Display main menu options."""
        ui.console.clear()
        ui.console.rule("[bold]DX Vault Atlas · Configuration[/bold]")
        ui.console.print("\n[dim]Select a category to edit:[/dim]\n")
        ui.console.print("  [cyan]1.[/cyan] Paths (Vault & Inbox)")
        ui.console.print("  [cyan]2.[/cyan] Editor")
        ui.console.print("  [cyan]3.[/cyan] Field Mappings [dim](Rename keys)[/dim]")
        ui.console.print("  [cyan]4.[/cyan] Value Mappings [dim](Replace values)[/dim]")
        ui.console.print("  [cyan]5.[/cyan] Save & Exit")
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

    # -- value mappings -----------------------------------------------------

    def _edit_value_mappings(self, config: GlobalConfig) -> None:
        """Edit value mappings (per-field value replacement)."""
        while True:
            ui.console.clear()
            ui.console.rule("[bold]Value Mappings (Replace)[/bold]")
            ui.console.print(
                "\n[dim]Replace values in specific fields (Field → Old → New).[/dim]\n"
            )

            if not config.value_mappings:
                ui.console.print("  [dim]No value mappings defined.[/dim]")
            else:
                idx = 1
                for field, reps in config.value_mappings.items():
                    for old_v, new_v in reps.items():
                        ui.console.print(
                            f"  {idx}. [cyan]{field}[/cyan]:"
                            f" [yellow]{old_v}[/yellow]"
                            f" → [green]{new_v}[/green]"
                        )
                        idx += 1

            ui.console.print("\n  [cyan]A.[/cyan] Add Mapping")
            ui.console.print("  [cyan]D.[/cyan] Delete Mapping")
            ui.console.print("  [cyan]0.[/cyan] Back")
            ui.console.print()

            action = Prompt.ask(
                "Select action",
                choices=["0", "a", "A", "d", "D"],
                default="0",
            ).lower()

            if action == "0":
                break
            if action == "a":
                self._add_value_mapping(config)
            elif action == "d":
                self._delete_value_mapping(config)

    def _add_value_mapping(self, config: GlobalConfig) -> None:
        """Add a new value mapping."""
        field = Prompt.ask("Field name (e.g. source)")
        if not field:
            return
        old_val = Prompt.ask(f"Old value to replace in '{field}'")
        if not old_val:
            return
        new_val = Prompt.ask(f"New value for '{old_val}'")
        if new_val:
            config.value_mappings.setdefault(field, {})
            config.value_mappings[field][old_val] = new_val

    def _delete_value_mapping(
        self,
        config: GlobalConfig,
    ) -> None:
        """Delete an existing value mapping."""
        if not config.value_mappings:
            return

        field = Prompt.ask("Field name (or empty to cancel)")
        if not field or field not in config.value_mappings:
            if field:
                ui.console.print("[red]Field not found.[/red]")
                Prompt.ask("Press Enter to continue")
            return

        old_val = Prompt.ask(f"Old value to remove from '{field}' (or empty to cancel)")
        if not old_val:
            return
        if old_val in config.value_mappings[field]:
            del config.value_mappings[field][old_val]
            if not config.value_mappings[field]:
                del config.value_mappings[field]
            ui.console.print(f"[yellow]Deleted {field}: {old_val}[/yellow]")
        else:
            ui.console.print("[red]Value not found.[/red]")
            Prompt.ask("Press Enter to continue")
