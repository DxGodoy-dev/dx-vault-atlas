"""First-run configuration wizard using Rich prompts.

Provides an interactive setup experience for users who don't have
a configuration file yet.
"""

from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from dx_vault_atlas.shared.config import GlobalConfig
from dx_vault_atlas.shared.paths import validate_directory

console = Console()


def _validate_directory(path_str: str) -> Path | None:
    """Validate that a path exists and is a directory.

    Args:
        path_str: User-provided path string.

    Returns:
        Resolved Path if valid, None otherwise.
    """
    try:
        return validate_directory(path_str)
    except ValueError:
        return None


def _prompt_directory(prompt_text: str, default: str | None = None) -> Path:
    """Prompt user for a directory path with validation.

    Args:
        prompt_text: Text to display in the prompt.
        default: Optional default value.

    Returns:
        Validated directory Path.
    """
    while True:
        response = Prompt.ask(prompt_text, default=default or "")
        if not response.strip():
            console.print("[red]Please enter a valid path.[/red]")
            continue

        validated = _validate_directory(response)
        if validated:
            return validated

        console.print(f"[red]Path does not exist or is not a directory: {response}[/]")
        console.print("[dim]Tip: Use absolute paths like C:\\Users\\You\\Vault[/dim]")


def run_setup_wizard() -> GlobalConfig | None:
    """Run interactive setup wizard for first-time configuration.

    Collects vault_path, vault_inbox, and editor preference from user.

    Returns:
        GlobalConfig with user settings, or None if cancelled.
    """
    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]DX Vault Atlas Setup[/bold cyan]\n\n"
            "No configuration found. Let's set things up!",
            border_style="cyan",
        )
    )
    console.print()

    try:
        # 1. Vault Path
        console.print("[bold]Step 1/3:[/bold] Where is your Obsidian vault?")
        vault_path = _prompt_directory(
            "[cyan]Vault path[/cyan]",
            default=str(Path.home() / "Obsidian" / "Vault"),
        )
        console.print(f"[green]✓[/green] Vault: {vault_path}\n")

        # 2. Inbox Path
        console.print("[bold]Step 2/3:[/bold] Where should new notes be created?")
        default_inbox = vault_path / "Inbox"
        inbox_default = str(default_inbox) if default_inbox.exists() else None
        vault_inbox = _prompt_directory(
            "[cyan]Inbox path[/cyan]",
            default=inbox_default,
        )
        console.print(f"[green]✓[/green] Inbox: {vault_inbox}\n")

        # 3. Editor
        console.print("[bold]Step 3/3:[/bold] Which editor do you prefer?")
        console.print("[dim]Examples: code, vim, notepad, nano[/dim]")
        editor = Prompt.ask(
            "[cyan]Editor command[/cyan]",
            default="code",
        )
        console.print(f"[green]✓[/green] Editor: {editor}\n")

        # Create config
        config = GlobalConfig(
            vault_path=vault_path,
            vault_inbox=vault_inbox,
            editor=editor,
        )

        console.print(
            Panel.fit(
                "[bold green]Setup complete![/bold green]\n"
                "Your configuration has been saved.",
                border_style="green",
            )
        )
        console.print()

        return config

    except KeyboardInterrupt:
        console.print("\n[yellow]Setup cancelled.[/yellow]")
        return None
