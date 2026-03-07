"""Pydantic schema for note frontmatter validation."""

from pydantic import BaseModel, Field

from dx_vault_atlas.shared.models.enums import (
    NoteArea,
    NoteStatus,
    Priority,
)


class FrontmatterSchema(BaseModel):
    """Schema for validating/serializing note frontmatter.

    All fields that can be present in a frontmatter are defined here
    with their proper types. Optional fields use None as default.
    """

    version: str | None = None
    title: str | None = None
    aliases: list[str] = Field(default_factory=list)
    type: str | None = None
    tags: list[str] = Field(default_factory=list)
    priority: Priority | int | None = None
    area: NoteArea | str | None = None
    status: NoteStatus | str | None = None

    model_config = {"extra": "allow"}  # Allow additional YAML fields
