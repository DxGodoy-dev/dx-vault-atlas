"""Shared TUI module for DX Vault Atlas.

Provides reusable components:
- BaseApp: Base application with bindings and theme
- WizardApp: Generic wizard driven by config
- VimOptionList: OptionList with j/k navigation
- StepDone: Completed wizard step display
- WizardConfig: Wizard configuration
"""

from dx_vault_atlas.shared.tui.app import BaseApp
from dx_vault_atlas.shared.tui.theme import SHARED_CSS, ThemeManager
from dx_vault_atlas.shared.tui.wizard import (
    WizardConfig,
)
from dx_vault_atlas.shared.tui.wizard_app import WizardApp, run_wizard

__all__ = [
    "WizardApp",
    "WizardConfig",
    "create_enum_options",
    "create_vim_option_list",
    "run_wizard",
]
