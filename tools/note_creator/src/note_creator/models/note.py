from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

from note_creator.models.enums import Priority, NoteStatus, NoteSource, NoteArea

schema_v = "1.0"

class BaseNote(BaseModel):
    """Base model for Obsidian notes; defines frontmatter fields and validation."""

    # Configuración para prohibir campos extra en toda la jerarquía
    model_config = {
        "extra": "forbid",
        "populate_by_name": True
    }

    title: str = Field(..., min_length=1, description="Título de la nota")
    aliases: list[str] = Field(..., min_length=1, description="[Alias de la nota]")
    date: datetime = Field(default_factory=datetime.now)
    tags: List[str] = Field(default_factory=list)
    version: str = Field(default=schema_v)
    note_type: str = Field(..., 
        alias="type",
        description="Tipo de la nota",
    ) 

    @field_validator("tags", mode="before")
    @classmethod
    def ensure_list(cls, v):
        """Ensures tags is always a list; converts a single string to a one-element list."""
        if isinstance(v, str):
            return [v]
        return v

class MocNote(BaseNote):
    "Note model for MOCs"
    level: Optional[int] = None
    up: Optional[str] = None

class RankedNote(BaseNote):
    """Notas que tienen una fuente y una prioridad definida."""
    source: NoteSource = Field(default=NoteSource.OTHER)
    priority: Priority = Field(default=Priority.LOW)

class WorkflowNote(RankedNote):
    """Clase abstracta para notas que tienen estado y pertenecen a un área."""
    status: NoteStatus = Field(default=NoteStatus.TO_DO)
    area: NoteArea = Field(default=NoteArea.PERSONAL, description="Categoría técnica de la nota (Personal or Work)")

class ProjectNote(WorkflowNote):
    """Note model for projects; adds status and optional start/end dates."""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    outcome: Optional[int] = None

class TaskNote(WorkflowNote):
    """Note model for tasks; adds optional deadline."""
    deadline: Optional[datetime] = None