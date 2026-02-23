"""Generic Wizard TUI that runs from configuration."""

from typing import Any

from textual.app import ComposeResult
from textual.binding import Binding
from textual.widgets import Input, Label, OptionList, Static

from dx_vault_atlas.shared.tui.app import BaseApp
from dx_vault_atlas.shared.tui.widgets import StepDone, create_vim_option_list
from dx_vault_atlas.shared.tui.wizard import WizardConfig, WizardStep


class WizardApp(BaseApp):
    """Generic wizard TUI driven by configuration."""

    BINDINGS = [
        Binding("s", "skip", "Skip", show=True),
        Binding("ctrl+s", "skip", "Skip", show=False),
    ]

    def __init__(self, config: WizardConfig) -> None:
        """Initialize wizard.

        Args:
            config: Wizard configuration with steps and callbacks.
        """
        super().__init__()
        self.config = config
        self.HEADER_TITLE = config.title
        self.data: dict[str, Any] = {}
        self.step_index = 0
        self.active_steps: list[WizardStep] = []

    def compose(self) -> ComposeResult:
        """Compose the application."""
        yield from super().compose()

    def on_mount(self) -> None:
        """Start wizard on mount."""
        self._compute_active_steps()
        self._show_current_step()

    def _compute_active_steps(self) -> None:
        """Compute which steps are active based on conditions."""
        self.active_steps = [
            step
            for step in self.config.steps
            if step.condition is None or step.condition(self.data)
        ]

    def _show_current_step(self) -> None:
        """Show current wizard step."""
        if self.step_index >= len(self.active_steps):
            self._complete()
            return

        self.clear_wizard()

        # Show completed steps
        for i in range(self.step_index):
            step = self.active_steps[i]
            value = self._format_value(self.data.get(step.key))
            self.wizard.mount(
                StepDone(step.label.replace("Select ", "").replace("Enter ", ""), value)
            )

        # Show current step
        step = self.active_steps[self.step_index]
        hint = "[dim](j/k)[/]" if step.step_type == "select" else ""
        self.wizard.mount(
            Label(f"[bold cyan]●[/] {step.label} {hint}", classes="prompt-label")
        )

        if step.step_type == "input":
            input_widget = Input(
                value=step.default_value,
                placeholder=step.placeholder,
                id="wizard-input",
            )
            self.wizard.mount(input_widget)
            self.call_after_refresh(input_widget.focus)
        elif step.step_type == "select":
            # Cast to fix MyPy: create_vim_option_list expects type, not Optional[type]
            # We know it's not None here because of the check,
            # but logic might allow None in definition
            from enum import Enum

            enum_cls = step.enum_cls
            assert issubclass(enum_cls, Enum)

            # Resolve default Enum member to its positional index
            members = list(enum_cls)
            try:
                default_idx = members.index(step.default_value)
            except (ValueError, TypeError):
                default_idx = 0

            opt_list = create_vim_option_list(
                enum_cls,
                default_idx,
                step.key,
            )
            self.wizard.mount(opt_list)
            self.call_after_refresh(opt_list.focus)

    def _format_value(self, value: object) -> str:
        """Format value for display."""
        if value is None:
            return ""
        if hasattr(value, "value"):
            val = value.value
            if isinstance(val, str):
                return val.replace(".md", "").title()
            name = getattr(value, "name", "")
            return f"{name.title()} ({val})"
        return str(value)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission."""
        if event.value.strip():
            step = self.active_steps[self.step_index]
            self.data[step.key] = event.value.strip()
            self._advance()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle option selection."""
        parts = event.option_id.split("-")
        index = int(parts[-1])

        step = self.active_steps[self.step_index]
        self.data[step.key] = list(step.enum_cls)[index]
        self._advance()

    def _advance(self) -> None:
        """Advance to next step."""
        self.step_index += 1
        self._compute_active_steps()  # Recompute in case conditions changed
        self._show_current_step()

    def _complete(self) -> None:
        """Complete the wizard."""
        self.clear_wizard()

        # Show all completed steps
        for step in self.active_steps:
            value = self._format_value(self.data.get(step.key))
            label = step.label.replace("Select ", "").replace("Enter ", "")
            self.wizard.mount(StepDone(label, value))

        # Run callback if provided (for side effects like logging)
        if self.config.on_complete:
            try:
                self.config.on_complete(self.data)
            except Exception as e:
                self.wizard.mount(
                    Static(f"[bold red]✗[/] Error in callback: {e}", classes="error")
                )

        # Return data and exit
        self.exit(self.data)

    def action_skip(self) -> None:
        """Skip the current wizard."""
        self.exit({"__skip__": True})

    def action_quit(self) -> None:
        """Quit the application entirely."""
        self.exit({"__quit__": True})


def run_wizard(config: WizardConfig) -> dict[str, Any] | None:
    """Run a wizard TUI with the given configuration.

    Returns:
        Collected data dict or None if cancelled.
    """
    app = WizardApp(config)
    return app.run()
