"""Pydantic models for Obsidian notes."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from dx_vault_atlas.core.registry import register_note_type
from dx_vault_atlas.services.note_creator.core.registry import register_model
from dx_vault_atlas.services.note_creator.defaults import SCHEMA_VERSION
from dx_vault_atlas.services.note_creator.models.enums import (
    NoteArea,
    NoteSource,
    NoteStatus,
    NoteTemplate,
    Priority,
)


class BaseNote(BaseModel):
    """Base model for Obsidian notes with frontmatter fields."""

    model_config = {"extra": "forbid", "populate_by_name": True}

    version: str = Field(default=SCHEMA_VERSION)
    title: str = Field(..., min_length=1, description="Note title")
    aliases: list[str] = Field(default_factory=list, description="Note aliases")
    tags: list[str] = Field(default_factory=list)
    created: datetime = Field(default_factory=datetime.now)
    updated: datetime = Field(default_factory=datetime.now)
    note_type: str = Field(..., alias="type", description="Note type")

    @field_validator("tags", mode="before")
    @classmethod
    def ensure_list(cls, v: str | list[str]) -> list[str]:
        """Ensure tags is always a list."""
        if isinstance(v, str):
            return [v]
        return v

    @field_validator("version", mode="before")
    @classmethod
    def coerce_version(cls, v: str | int | float) -> str:
        """Ensure version is always a string."""
        return str(v)


@register_model(NoteTemplate.MOC)
@register_note_type("moc")
class MocNote(BaseNote):
    """Note model for Maps of Content (MOC)."""

    level: int | None = None
    up: str | None = None


@register_model(NoteTemplate.REF)
@register_note_type("ref")
class RefNote(BaseNote):
    """Reference note with minimal fields."""

    pass


class RankedNote(BaseNote):
    """Notes with source and priority fields."""

    source: NoteSource | str
    priority: Priority


class StatusNote(RankedNote):
    """Base note for status-tracking."""

    status: NoteStatus


@register_model(NoteTemplate.INFO)
@register_note_type("info")
class InfoNote(StatusNote):
    """Information note with status."""

    # User requested default "To Read" and implied no enum selection needed
    status: NoteStatus = Field(default=NoteStatus.TO_READ)


class WorkflowNote(StatusNote):
    """Notes with status and area fields."""

    # Override with Enum for workflow notes
    status: NoteStatus = Field(default=NoteStatus.TO_DO)
    area: NoteArea = Field(description="Note category (Personal or Work)")


@register_model(NoteTemplate.PROJECT)
@register_note_type("project")
class ProjectNote(WorkflowNote):
    """Note model for projects with dates and outcome."""

    start_date: datetime | None = None
    end_date: datetime | None = None
    outcome: int | None = None


@register_model(NoteTemplate.TASK)
@register_note_type("task")
class TaskNote(WorkflowNote):
    """Note model for tasks with deadline."""

    deadline: datetime | None = None


AnyNote = ProjectNote | TaskNote | InfoNote | RefNote | MocNote | BaseNote
