"""Default values for note creation.

Centralized configuration for easy customization.
"""

from dx_vault_atlas.shared.models.enums import (
    NoteArea,
    NoteStatus,
    NoteTemplate,
    Priority,
)

# Schema version for frontmatter
SCHEMA_VERSION = "1.0"

# Default tags for new notes
DEFAULT_TAGS: list[str] = []


# Default values for workflow fields
DEFAULT_PRIORITY = Priority.LOW
DEFAULT_STATUS = NoteStatus.TO_DO
DEFAULT_AREA = NoteArea.PERSONAL
DEFAULT_TEMPLATE = NoteTemplate.INFO
