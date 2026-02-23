"""Validator module for note_migrator."""

from dx_vault_atlas.services.note_creator.models.note import (
    BaseNote,
    InfoNote,
    MocNote,
    ProjectNote,
    RefNote,
    TaskNote,
)

# Model mapping for migration
MODEL_MAP: dict[str, type[BaseNote]] = {
    "project": ProjectNote,
    "task": TaskNote,
    "info": InfoNote,
    "moc": MocNote,
    "ref": RefNote,
}
