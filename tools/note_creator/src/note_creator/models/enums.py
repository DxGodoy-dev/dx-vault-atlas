from enum import Enum, IntEnum



class Priority(IntEnum):
    """Note urgency level; IntEnum allows numeric comparison."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    URGENT = 5


class NoteStatus(str, Enum):
    """Lifecycle status for project or task notes."""

    TO_DO = "To Do"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    ARCHIVED = "Archived"


class NoteSource(str, Enum):
    """Source of the note content."""

    IA = "ia"
    DOCUMENTATION = "documentation"
    RESEARCH = "research"
    YOUTUBE = "youtube"
    ME = "me"
    OTHER = "other"


class NoteTemplate(str, Enum):
    """Available note templates."""

    INFO = "info.md"
    MOC = "moc.md"
    PROJECT = "project.md"
    TASK = "task.md"

class NoteArea(str, Enum):
    """Note area"""

    PERSONAL = "Personal"
    WORK = "Work"

