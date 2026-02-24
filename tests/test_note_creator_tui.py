"""Tests for note creator TUI configuration."""

from unittest.mock import MagicMock, patch

from dx_vault_atlas.services.note_creator.tui import run_tui
from dx_vault_atlas.shared.config import GlobalConfig
from dx_vault_atlas.shared.tui import WizardConfig


class TestNoteCreatorTUI:
    """Tests for TUI entry point."""

    @patch("dx_vault_atlas.services.note_creator.tui.run_wizard")
    def test_run_tui_configures_wizard(self, mock_run_wizard: MagicMock) -> None:
        """run_tui should configure wizard and return result."""
        mock_settings = MagicMock(spec=GlobalConfig)
        mock_run_wizard.return_value = {"some": "data"}

        result = run_tui(mock_settings)

        assert result == {"some": "data"}
        mock_run_wizard.assert_called_once()

        # Check config
        args = mock_run_wizard.call_args[0]
        config: WizardConfig = args[0]
        assert config.title == "DX Vault Atlas · Note Creator"
        assert config.on_complete is None
