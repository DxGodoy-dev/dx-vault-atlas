"""Transformation service for note migration logic."""

from pathlib import Path
from typing import Any

from packaging.version import parse as parse_version

from dx_vault_atlas.services.note_creator.defaults import SCHEMA_VERSION
from dx_vault_atlas.services.note_creator.models.note import (
    BaseNote,
    InfoNote,
    MocNote,
    ProjectNote,
    RefNote,
    TaskNote,
)
from dx_vault_atlas.shared.config import GlobalConfig


# Model mapping for migration
MODEL_MAP: dict[str, type[BaseNote]] = {
    "project": ProjectNote,
    "task": TaskNote,
    "info": InfoNote,
    "moc": MocNote,
    "ref": RefNote,
}


from dx_vault_atlas.shared.logger import logger


class TransformationService:
    """Service to handle core migration transformation logic."""

    def __init__(self, settings: GlobalConfig) -> None:
        self.settings = settings

    def transform(
        self,
        frontmatter: dict[str, Any],
        file_path: Path,
        rename_only: bool = False,
        debug_mode: bool = False,
    ) -> tuple[dict[str, Any], bool]:
        """Apply migration transformations to frontmatter.

        Args:
            frontmatter: Original frontmatter.
            file_path: Path to the note file (for date resolution).
            rename_only: If True, only apply field renames.
            debug_mode: If True, enable verbose logging.

        Returns:
            Tuple of (updated_frontmatter, has_changes).
        """
        # Work on a copy
        data = frontmatter.copy()
        has_changes = False

        if debug_mode:
            logger.debug(
                f"Transforming {file_path.name}. Original keys: {list(data.keys())}"
            )

        # 1. Apply Field Mappings (Renaming)
        for old_field, new_field in self.settings.field_mappings.items():
            if old_field in data:
                # Move check
                if new_field not in data:
                    data[new_field] = data[old_field]
                    del data[old_field]
                    has_changes = True
                    if debug_mode:
                        logger.debug(f"Renamed field '{old_field}' -> '{new_field}'")
                else:
                    # Both exist, clean old
                    del data[old_field]
                    has_changes = True
                    if debug_mode:
                        logger.debug(
                            f"Removed old field '{old_field}' (new '{new_field}' already exists)"
                        )

        if rename_only:
            return data, has_changes

        # Full Migration Steps

        # 2. Check version
        current_version_str = str(data.get("version") or "")
        current_version = (
            parse_version(current_version_str) if current_version_str else None
        )
        target_version = parse_version(SCHEMA_VERSION)

        should_update_version = False
        if not current_version or current_version < target_version:
            should_update_version = True
            has_changes = True
            if debug_mode:
                logger.debug(f"Version outdated: {current_version} < {target_version}")

        # 3. Check for missing 'created'/'updated'
        # We DO NOT resolve dates here. That is the job of Note Doctor.
        # We only ensure the keys exist (as null) if they are completely missing.
        if "created" not in data:
            data["created"] = None
            has_changes = True
            if debug_mode:
                logger.debug("Added missing 'created' key (null)")

        if "updated" not in data:
            data["updated"] = None
            has_changes = True
            if debug_mode:
                logger.debug("Added missing 'updated' key (null)")

        # Update version
        if should_update_version:
            data["version"] = SCHEMA_VERSION
            has_changes = True
            if debug_mode:
                logger.debug(f"Updated version to {SCHEMA_VERSION}")

        # Filter and Reorder based on Model
        # This ALWAYS happens in full migration to ensure schema compliance
        if self._enforce_model_schema(data, debug_mode):
            has_changes = True

        return data, has_changes

    def _enforce_model_schema(self, data: dict[str, Any], debug_mode: bool) -> bool:
        """Enforce model schema fields and ordering.

        Modifies data in-place if changes are needed.

        Returns:
            True if data was modified, False otherwise.
        """
        note_type = data.get("type")
        if not (
            note_type
            and isinstance(note_type, str)
            and (model_cls := MODEL_MAP.get(note_type))
        ):
            return False

        clean_data = {}
        for field_name, field_info in model_cls.model_fields.items():
            key = field_info.alias or field_name
            if key in data:
                clean_data[key] = data[key]
            elif field_name in data:
                clean_data[field_name] = data[field_name]

        if "type" not in clean_data and "note_type" not in clean_data:
            clean_data["type"] = note_type

        # Check if this changed anything (content OR order)
        if clean_data != data or list(clean_data.keys()) != list(data.keys()):
            if debug_mode:
                logger.debug(
                    f"Reordered/Cleaned fields for type '{note_type}'. Removed keys: {set(data.keys()) - set(clean_data.keys())}"
                )
            data.clear()
            data.update(clean_data)
            return True

        return False
