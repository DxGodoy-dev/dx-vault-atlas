"""Bootstrap logic for environment initialization."""

import sys
from typing import NoReturn

from dx_vault_atlas.shared.config import (
    GlobalConfig,
    get_config_manager,
)
from dx_vault_atlas.shared.console import console
from dx_vault_atlas.shared.tui.config_wizard import run_setup_wizard


def _exit_app(code: int = 0) -> NoReturn:
    """Exit the application."""
    sys.exit(code)


def ensure_config_exists() -> GlobalConfig:
    """Ensure configuration exists, running setup wizard if needed.

    Returns:
        Loaded GlobalConfig.

    Raises:
        SystemExit: If setup is cancelled or fails.
    """
    manager = get_config_manager()

    if manager.exists():
        return manager.load()

    # If we are here, we need to run setup
    # Note: We are running TUI here, which prints to stdout.
    # This is acceptable for a bootstrap process that initiates interaction.
    console.print("No configuration found. Starting setup...")

    config = run_setup_wizard()
    if config is None:
        # User cancelled
        _exit_app(1)

    manager.save(config)
    console.print("Configuration saved.")

    return config
