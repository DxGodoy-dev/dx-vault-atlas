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
from dx_vault_atlas.shared.tui.widgets import (
    StepDone,
    VimOptionList,
    create_enum_options,
    create_vim_option_list,
)
from dx_vault_atlas.shared.tui.wizard import (
    WizardConfig,
    WizardStep,
)
from dx_vault_atlas.shared.tui.wizard_app import WizardApp, run_wizard

__all__ = [
    "BaseApp",
    "SHARED_CSS",
    "StepDone",
    "ThemeManager",
    "VimOptionList",
    "WizardApp",
    "WizardConfig",
    "WizardStep",
    "create_enum_options",
    "create_vim_option_list",
    "run_wizard",
]
