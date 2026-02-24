"""Note Creator TUI - minimal config only."""

from typing import Any

from dx_vault_atlas.shared.config import GlobalConfig
from dx_vault_atlas.shared.tui import WizardConfig, run_wizard
from dx_vault_atlas.services.note_creator.tui_steps import NOTE_CREATOR_STEPS


def run_tui(settings: GlobalConfig) -> dict[str, Any] | None:
    """Run the Note Creator TUI and return collected data.

    Args:
        settings: Application settings.

    Returns:
        Collected wizard data or None if cancelled.
    """
    config = WizardConfig(
        title="DX Vault Atlas · Note Creator",
        steps=NOTE_CREATOR_STEPS,
        on_complete=None,  # No callback, return data directly
        success_message="Note ready to create!",
        auto_exit_delay=0.1,  # Exit immediately after completion
    )
    return run_wizard(config)
