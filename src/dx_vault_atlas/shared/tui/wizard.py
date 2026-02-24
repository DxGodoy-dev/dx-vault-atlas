"""Wizard step definitions and builder for TUI applications."""

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Any


@dataclass
class WizardStep:
    """Definition of a wizard step."""

    key: str
    label: str
    step_type: str  # "input" or "select"
    enum_cls: type[Enum] | None = None
    default_value: Any = None
    placeholder: str = ""
    condition: Callable[[dict[str, Any]], bool] | None = None


@dataclass
class WizardConfig:
    """Configuration for a wizard TUI."""

    title: str
    steps: list[WizardStep]
    on_complete: Callable[[dict[str, Any]], None] | None = None
    success_message: str = "Complete!"
    auto_exit_delay: float = 1.5
