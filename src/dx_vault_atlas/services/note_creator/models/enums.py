"""Enumerations for note models."""

from enum import IntEnum, StrEnum


class Priority(IntEnum):
    """Note urgency level; IntEnum allows numeric comparison."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    URGENT = 5


class NoteStatus(StrEnum):
    """Lifecycle status for project or task notes."""

    TO_DO = "to_do"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"
    TO_READ = "to_read"


class NoteSource(StrEnum):
    """Source of the note content."""

    IA = "ia"
    DOCUMENTATION = "documentation"
    RESEARCH = "research"
    YOUTUBE = "youtube"
    ME = "me"
    OTHER = ""


class NoteTemplate(StrEnum):
    """Available note templates."""

    INFO = "info.md"
    REF = "ref.md"
    MOC = "moc.md"
    PROJECT = "project.md"
    TASK = "task.md"


class NoteArea(StrEnum):
    """Note category (personal or work)."""

    PERSONAL = "personal"
    WORK = "work"
