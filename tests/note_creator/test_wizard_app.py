"""Tests for wizard application."""

from unittest.mock import MagicMock

from dx_vault_atlas.shared.tui.wizard import WizardConfig
from dx_vault_atlas.shared.tui.wizard_app import WizardApp


class TestWizardApp:
    """Tests for WizardApp."""

    def test_has_skip_bindings(self) -> None:
        """WizardApp should have s and ctrl+s bindings for skipping."""
        bindings = {b.key for b in WizardApp.BINDINGS}

        assert "s" in bindings
        assert "ctrl+s" in bindings

        # Verify action mappings
        s_binding = next(b for b in WizardApp.BINDINGS if b.key == "s")
        assert s_binding.action == "skip"

        ctrl_s_binding = next(b for b in WizardApp.BINDINGS if b.key == "ctrl+s")
        assert ctrl_s_binding.action == "skip"
