"""Tests for wizard configuration."""

from dx_vault_atlas.shared.models.enums import NoteTemplate
from dx_vault_atlas.shared.tui.common_steps import (
    AREA_STEP,
    NOTE_CREATOR_STEPS,
    PRIORITY_STEP,
    TEMPLATE_STEP,
    TITLE_STEP,
)
from dx_vault_atlas.shared.tui.wizard import WizardConfig


class TestWizardStep:
    """Tests for WizardStep dataclass."""

    def test_title_step_is_input_type(self) -> None:
        """Title step should be input type."""
        assert TITLE_STEP.step_type == "input"
        assert TITLE_STEP.key == "title"
        assert TITLE_STEP.placeholder != ""

    def test_template_step_is_select_type(self) -> None:
        """Template step should be select type."""
        assert TEMPLATE_STEP.step_type == "select"
        assert TEMPLATE_STEP.enum_cls == NoteTemplate

    def test_moc_skips_priority_area(self) -> None:
        """MOC template should skip priority/area steps."""
        moc_data = {"template": NoteTemplate.MOC}

        assert PRIORITY_STEP.condition(moc_data) is False
        assert AREA_STEP.condition(moc_data) is False

    def test_info_includes_priority_not_area(self) -> None:
        """Info template needs priority but not area."""
        info_data = {"template": NoteTemplate.INFO}

        assert PRIORITY_STEP.condition(info_data) is True
        assert AREA_STEP.condition(info_data) is False

    def test_task_includes_area(self) -> None:
        """Task template needs area."""
        task_data = {"template": NoteTemplate.TASK}

        assert AREA_STEP.condition(task_data) is True

    def test_project_includes_area(self) -> None:
        """Project template needs area."""
        project_data = {"template": NoteTemplate.PROJECT}

        assert AREA_STEP.condition(project_data) is True


class TestNoteCreatorSteps:
    """Tests for NOTE_CREATOR_STEPS configuration."""

    def test_has_four_steps(self) -> None:
        """Should have 4 steps total."""
        assert len(NOTE_CREATOR_STEPS) == 4

    def test_steps_in_correct_order(self) -> None:
        """Steps should be in correct order."""
        keys = [step.key for step in NOTE_CREATOR_STEPS]
        assert keys == ["title", "template", "priority", "area"]


class TestWizardConfig:
    """Tests for WizardConfig dataclass."""

    def test_config_with_defaults(self) -> None:
        """Config should have sensible defaults."""
        config = WizardConfig(
            title="Test Wizard",
            steps=NOTE_CREATOR_STEPS,
        )

        assert config.title == "Test Wizard"
        assert config.success_message == "Complete!"
        assert config.auto_exit_delay == 1.5
        assert config.on_complete is None
