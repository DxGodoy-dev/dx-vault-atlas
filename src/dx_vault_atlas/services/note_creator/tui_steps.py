"""Wizard steps for Note Creator TUI."""

from dx_vault_atlas.services.note_creator.defaults import (
    DEFAULT_AREA,
    DEFAULT_PRIORITY,
    DEFAULT_SOURCE,
    DEFAULT_TEMPLATE,
)
from dx_vault_atlas.services.note_creator.models.enums import (
    NoteArea,
    NoteSource,
    NoteStatus,
    NoteTemplate,
    Priority,
)
from dx_vault_atlas.shared.tui.wizard import WizardStep

# Standard steps for note wizard
TITLE_STEP = WizardStep(
    key="title",
    label="Enter note title",
    step_type="input",
    placeholder="My new note...",
)

TEMPLATE_STEP = WizardStep(
    key="template",
    label="Select template",
    step_type="select",
    enum_cls=NoteTemplate,
    default_value=DEFAULT_TEMPLATE,
)

SOURCE_STEP = WizardStep(
    key="source",
    label="Select source",
    step_type="select",
    enum_cls=NoteSource,
    default_value=DEFAULT_SOURCE,
    condition=lambda data: (
        data.get("template") not in (NoteTemplate.MOC, NoteTemplate.REF)
    ),
)

PRIORITY_STEP = WizardStep(
    key="priority",
    label="Select priority",
    step_type="select",
    enum_cls=Priority,
    default_value=DEFAULT_PRIORITY,
    condition=lambda data: (
        data.get("template") not in (NoteTemplate.MOC, NoteTemplate.REF)
    ),
)

AREA_STEP = WizardStep(
    key="area",
    label="Select area",
    step_type="select",
    enum_cls=NoteArea,
    default_value=DEFAULT_AREA,
    condition=lambda data: (
        data.get("template") in (NoteTemplate.TASK, NoteTemplate.PROJECT)
    ),
)

STATUS_STEP = WizardStep(
    key="status",
    label="Select status",
    step_type="select",
    enum_cls=NoteStatus,
    default_value=NoteStatus.TO_DO,
    condition=lambda data: (
        data.get("template") in (NoteTemplate.PROJECT, NoteTemplate.TASK)
    ),
)

# Pre-built step sequences
NOTE_CREATOR_STEPS = [
    TITLE_STEP,
    TEMPLATE_STEP,
    SOURCE_STEP,
    PRIORITY_STEP,
    AREA_STEP,
]
