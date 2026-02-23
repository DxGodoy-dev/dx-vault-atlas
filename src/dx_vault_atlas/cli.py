"""CLI entry point for DX Vault Atlas.

Refactored to comply with:
- Skill 06: Error Lifecycle (Main Catch)
- Skill 01: Project Structure (Imports)
"""

import json
import sys
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.traceback import install as install_rich_traceback

# Adjust imports based on new src/ structure if necessary,
# assuming installed in editable mode or PYTHONPATH set.
from dx_vault_atlas.shared.config import (
    ConfigNotFoundError,
    get_config_manager,
)
from dx_vault_atlas.shared.tui.config_wizard import run_setup_wizard
from dx_vault_atlas.shared.logger import logger  # Skill 07

# Setup Rich for unhandled exceptions in TUI mode
install_rich_traceback(show_locals=False)

console = Console()

app = typer.Typer(
    name="dx-vault-atlas",
    help="CLI tool for managing Obsidian vaults.",
    add_completion=False,
    no_args_is_help=True,  # Improved UX
)

# Config subcommand group
config_app = typer.Typer(help="Manage application configuration.")
app.add_typer(config_app, name="config")


@app.callback(invoke_without_command=True)
def init_config(ctx: typer.Context) -> None:
    """Ensure configuration exists before running commands."""
    if ctx.invoked_subcommand == "config":
        return

    # Lazy import to avoid circular dependencies during bootstrap
    from dx_vault_atlas.shared.core.bootstrap import ensure_config_exists

    try:
        ensure_config_exists()
    except Exception as e:
        # Log internal error, show user friendly error
        logger.critical(f"Bootstrap failed: {e}", exc_info=True)
        console.print(
            f"[bold red]Critical Error:[/bold red] Could not initialize configuration. See logs at {logger.handlers[0].baseFilename}"
        )
        raise typer.Exit(1)


@config_app.command("show")
def config_show() -> None:
    """Display current configuration."""
    manager = get_config_manager()

    try:
        config = manager.load()
    except ConfigNotFoundError:
        console.print(
            "[yellow]No configuration found.[/yellow] "
            "Run any command to start the setup wizard."
        )
        raise typer.Exit(0)

    # Display as formatted JSON
    data = config.model_dump(mode="json")
    json_str = json.dumps(data, indent=2, ensure_ascii=False)

    console.print(
        Panel(
            Syntax(json_str, "json", theme="monokai"),
            title=f"[bold]Config[/bold] ({manager.config_path})",
            border_style="cyan",
        )
    )


@config_app.command("edit")
def config_edit() -> None:
    """Modify configuration values interactively."""
    from dx_vault_atlas.shared.tui.config_editor import ConfigEditor

    # TUI execution
    editor = ConfigEditor()
    editor.run()


@config_app.command("reset")
def config_reset() -> None:
    """Delete configuration and run setup wizard."""
    manager = get_config_manager()

    if manager.exists():
        from rich.prompt import Confirm

        if not Confirm.ask(
            "[yellow]Delete current configuration and start fresh?[/yellow]"
        ):
            console.print("Cancelled.")
            raise typer.Exit(0)

        manager.delete()
        logger.info("Configuration reset by user.")
        console.print("[dim]Configuration deleted.[/dim]\n")

    config = run_setup_wizard()
    if config:
        manager.save(config)
        logger.info("Configuration re-initialized.")


@app.command(name="note")
def note_creator() -> None:
    """Launch the interactive note creator wizard."""
    from dx_vault_atlas.services.note_creator.app import create_app
    from dx_vault_atlas.shared.config import get_settings

    settings = get_settings()
    app_instance = create_app(settings)
    app_instance.run()


@app.command(name="migrate")
def note_migrator(
    rename_only: bool = typer.Option(
        False,
        "--rename-only",
        help="Only rename fields based on config, skip schema migration.",
    ),
    debug_mode: bool = typer.Option(
        False,
        "--debug-mode",
        help="Enable debug logging and disable TUI for inputs.",
    ),
) -> None:
    """Migrate legacy notes to new schema versions."""
    from dx_vault_atlas.services.note_migrator.app import create_app
    from dx_vault_atlas.shared.config import get_settings
    from dx_vault_atlas.shared.logger import enable_debug_logging

    if debug_mode:
        enable_debug_logging()
        logger.debug("Debug mode enabled")

    settings = get_settings()
    app_instance = create_app(settings)
    app_instance.run(rename_only=rename_only, debug_mode=debug_mode)


@app.command(name="doctor")
def note_doctor(
    fix_date: bool = typer.Option(
        False,
        "--fix-date",
        help="Only fix created/updated dates and exit.",
    ),
    debug_mode: bool = typer.Option(
        False,
        "--debug-mode",
        help="Enable debug logging and disable TUI for inputs.",
    ),
) -> None:
    """Interactive doctor to fix invalid notes."""
    from dx_vault_atlas.services.note_doctor.main import main

    # Unused imports removed
    from dx_vault_atlas.shared.config import get_settings
    from dx_vault_atlas.services.note_doctor.app import create_app
    from dx_vault_atlas.shared.logger import enable_debug_logging

    if debug_mode:
        enable_debug_logging()
        logger.debug("Debug mode enabled")

    settings = get_settings()
    app_instance = create_app(settings)
    app_instance.run(fix_date=fix_date, debug_mode=debug_mode)


def main():
    """Entry point with the Skill 06 'Main Catch'."""
    try:
        app()
    except typer.Exit:
        # Typer exits are normal flow control
        raise
    except Exception as e:
        # THE MAIN CATCH: Captura todo lo que no fue manejado
        logger.critical(f"Unhandled exception at top level: {e}", exc_info=True)
        console.print("\n[bold red]FATAL ERROR[/bold red]")
        console.print(
            f"An unexpected error occurred. Please check the logs at: [cyan]{logger.handlers[0].baseFilename}[/cyan]"
        )
        console.print(f"Error details: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
