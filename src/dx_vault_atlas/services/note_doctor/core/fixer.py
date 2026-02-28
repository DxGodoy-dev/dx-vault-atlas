"""Note Fixing Domain Service."""

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic_core import PydanticUndefined

from dx_vault_atlas.services.note_creator.models.enums import (
    NoteArea,
    NoteStatus,
)
from dx_vault_atlas.services.note_doctor.core.date_resolver import (
    DateResolver,
)
from dx_vault_atlas.services.note_doctor.validator import MODEL_MAP
from dx_vault_atlas.services.note_migrator.services.yaml_parser import (
    YamlParserService,
)
from dx_vault_atlas.shared.logger import logger

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _strip_tz(dt: datetime) -> datetime:
    """Return a naive (tz-unaware) copy of *dt*."""
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt


def _normalize_key(text: str) -> str:
    """Lowercase, strip, and collapse whitespace/dashes."""
    return text.strip().lower().replace(" ", "_").replace("-", "_")


_SENTINEL = object()
"""Unique marker to distinguish 'no default' from ``None``."""


def _match_status_enum(raw: str) -> str | None:
    """Return the canonical NoteStatus value matching *raw*, or None."""
    norm = _normalize_key(raw)
    for member in NoteStatus:
        if _normalize_key(member.value) == norm:
            return member.value
    return None


# ---------------------------------------------------------------------------
# Fixer
# ---------------------------------------------------------------------------


class NoteFixer:
    """Applies fixes to note frontmatter based on rules."""

    def __init__(self) -> None:
        """Initialise the fixer with date resolver and YAML parser."""
        self.date_resolver = DateResolver()
        self.parser = YamlParserService()

    # -- public API ---------------------------------------------------------

    def check_and_fix_dates(
        self,
        file_path: Path,
        frontmatter: dict[str, Any],
    ) -> tuple[bool, dict[str, Any]]:
        """Check and fix dates according to hierarchy.

        Returns:
            (is_unchanged, updated_frontmatter)
        """
        updated = frontmatter.copy()
        has_changes = False

        from dx_vault_atlas.shared.logger import logger

        logger.debug(
            f"[Doctor Debug] Fixer 'check_and_fix_dates' start | frontmatter={updated}"
        )

        has_changes = self._fix_created(
            file_path,
            frontmatter,
            updated,
            has_changes,
        )
        has_changes = self._fix_updated(updated, has_changes)

        if has_changes:
            logger.debug(
                f"[Doctor Debug] Fixer 'check_and_fix_dates' applied changes | updated={updated}"
            )
            return False, updated
        return True, frontmatter

    def check_and_fix_enums(
        self,
        frontmatter: dict[str, Any],
    ) -> tuple[bool, dict[str, Any]]:
        """Check and fix enum values (case, whitespace, coercion).

        Returns:
            (is_unchanged, updated_frontmatter)
        """
        updated = frontmatter.copy()
        has_changes = False

        from dx_vault_atlas.shared.logger import logger

        logger.debug(
            f"[Doctor Debug] Fixer 'check_and_fix_enums' start | type={updated.get('type')}"
        )

        has_changes |= self._fix_type(updated)
        has_changes |= self._fix_status(updated)
        has_changes |= self._fix_area(updated)
        has_changes |= self._fix_aliases_tags(updated)
        has_changes |= self._fix_task_project_defaults(updated)

        if has_changes:
            logger.debug(
                f"[Doctor Debug] Fixer 'check_and_fix_enums' applied changes | updated={updated}"
            )
            return False, updated
        return True, frontmatter

    def check_and_fix_defaults(
        self,
        frontmatter: dict[str, Any],
    ) -> tuple[bool, dict[str, Any]]:
        """Fill missing fields with safe Pydantic defaults.

        Safe fields: status, version, tags.
        """
        updated = frontmatter.copy()
        has_changes = False
        safe_fields = {"status", "version", "tags"}

        from dx_vault_atlas.shared.logger import logger

        logger.debug(
            f"[Doctor Debug] Fixer 'check_and_fix_defaults' start | safe_fields={safe_fields}"
        )

        note_type = updated.get("type")
        if not note_type or not isinstance(note_type, str):
            return True, frontmatter

        model_cls = MODEL_MAP.get(note_type)
        if not model_cls:
            return True, frontmatter

        for name in safe_fields:
            if name in updated:
                continue
            val = self._resolve_field_default(model_cls, name)
            if val is not _SENTINEL:
                logger.debug(f"[Doctor Debug] Fixer injecting default {name}={val}")
                updated[name] = val
                has_changes = True

        if has_changes:
            logger.debug(
                f"[Doctor Debug] Fixer 'check_and_fix_defaults' applied changes | updated={updated}"
            )
            return False, updated
        return True, frontmatter

    def check_and_fix_extraneous(
        self,
        frontmatter: dict[str, Any],
    ) -> tuple[bool, dict[str, Any]]:
        """Remove fields that are not supported by the note's Pydantic model

        if the model forbids extra fields.
        """
        updated = frontmatter.copy()

        from dx_vault_atlas.shared.logger import logger

        logger.debug(f"[Doctor Debug] Fixer 'check_and_fix_extraneous' start")

        note_type = updated.get("type")
        if not note_type or not isinstance(note_type, str):
            return True, frontmatter

        model_cls = MODEL_MAP.get(note_type)
        if not model_cls:
            return True, frontmatter

        # Only remove extras if the model explicitly forbids them
        if getattr(model_cls, "model_config", {}).get("extra") == "forbid":
            from dx_vault_atlas.shared.pydantic_utils import strip_unknown_fields

            logger.debug(
                f"[DEBUG TRACE] fixer.check_and_fix_extraneous | Stripping unknowns for {model_cls.__name__} | 'source' in updated: {'source' in updated}"
            )
            clean_data = strip_unknown_fields(model_cls, updated)
            if clean_data != updated:
                logger.debug(
                    f"[Doctor Debug] Fixer removed extraneous fields | original={list(updated.keys())} -> new={list(clean_data.keys())} | 'source' in clean_data: {'source' in clean_data}"
                )
                return False, clean_data
        else:
            logger.debug(
                f"[Doctor Debug] Fixer 'check_and_fix_extraneous' skipped | model_config.extra={getattr(model_cls, 'model_config', {}).get('extra')}"
            )

        return True, frontmatter

    @staticmethod
    def _resolve_field_default(
        model_cls: type,
        field_name: str,
    ) -> object:
        """Return the safe default for *field_name*, or _SENTINEL."""
        if field_name not in model_cls.model_fields:
            return _SENTINEL
        info = model_cls.model_fields[field_name]
        if info.default is not None and info.default is not PydanticUndefined:
            val = info.default
            return val.value if hasattr(val, "value") else val
        if info.default_factory is not None:
            return info.default_factory()
        return _SENTINEL

    def fix(
        self,
        file_path: Path,
        current: dict[str, Any],
        body: str,
    ) -> tuple[bool, dict[str, Any], str]:
        """Orchestrate all fixes for a note file in memory.

        Returns:
            (has_changes, fixed_frontmatter, body)
        """
        logger.debug(
            f"[DEBUG TRACE] fixer.fix Start | 'source' in current: {'source' in current}"
        )
        total_changes = False

        unchanged, current = self.check_and_fix_dates(
            file_path,
            current,
        )
        if not unchanged:
            total_changes = True

        unchanged, current = self.check_and_fix_enums(current)
        if not unchanged:
            total_changes = True

        unchanged, current = self.check_and_fix_defaults(current)
        if not unchanged:
            total_changes = True

        unchanged, current = self.check_and_fix_extraneous(current)
        if not unchanged:
            total_changes = True

        logger.debug(
            f"[DEBUG TRACE] fixer.fix End | total_changes={total_changes} | 'source' in current: {'source' in current}"
        )
        return total_changes, current, body

    # -- private: date helpers ----------------------------------------------

    def _fix_created(
        self,
        file_path: Path,
        original: dict[str, Any],
        updated: dict[str, Any],
        has_changes: bool,
    ) -> bool:
        """Resolve the *created* field from filename or frontmatter."""
        true_created = self.date_resolver.resolve_created(
            file_path,
            original,
        )
        current_created = original.get("created")

        if true_created:
            if not current_created or current_created != true_created:
                updated["created"] = true_created
                return True
            return has_changes

        if current_created and isinstance(current_created, datetime):
            now_utc = datetime.now(UTC)
            if _strip_tz(current_created) > _strip_tz(now_utc):
                updated["created"] = None
                return True
        elif current_created is None and "created" not in original:
            updated["created"] = None
            return True

        return has_changes

    def _fix_updated(
        self,
        updated: dict[str, Any],
        has_changes: bool,
    ) -> bool:
        """Ensure *updated* ≥ *created*."""
        c_val = updated.get("created")

        if "updated" not in updated:
            updated["updated"] = c_val if c_val else None
            has_changes = True

        u_val = updated.get("updated")
        if (
            c_val
            and u_val
            and isinstance(c_val, datetime)
            and isinstance(u_val, datetime)
            and _strip_tz(u_val) < _strip_tz(c_val)
        ):
            updated["updated"] = c_val
            has_changes = True

        return has_changes

    # -- private: enum helpers ----------------------------------------------

    @staticmethod
    def _fix_type(updated: dict[str, Any]) -> bool:
        """Normalise note type or default to 'note'."""
        known = set(MODEL_MAP.keys()) | {"note"}

        if "type" in updated and isinstance(updated["type"], str):
            val = updated["type"].strip().lower()
            if val in known and val != updated["type"]:
                updated["type"] = val
                return True

        if "type" not in updated or not updated["type"]:
            updated["type"] = "note"
            return True

        return False

    @staticmethod
    def _fix_status(updated: dict[str, Any]) -> bool:
        """Coerce status lists/strings to their canonical enum value."""
        if "status" not in updated:
            return False

        changed = False
        current = updated["status"]

        if isinstance(current, list):
            if not current:
                del updated["status"]
                return True
            current = current[0]
            updated["status"] = current
            changed = True

        if isinstance(current, str):
            canonical = _match_status_enum(current)
            if canonical is None:
                del updated["status"]
                return True
            if current != canonical:
                updated["status"] = canonical
                changed = True

        return changed

    @staticmethod
    def _fix_area(updated: dict[str, Any]) -> bool:
        """Fix area casing to match the enum."""
        if "area" not in updated:
            return False
        if not isinstance(updated["area"], str):
            return False

        current = updated["area"]
        norm = _normalize_key(current)
        for member in NoteArea:
            if _normalize_key(member.value) == norm:
                if current != member.value:
                    updated["area"] = member.value
                    return True
                break
        return False

    @staticmethod
    def _fix_aliases_tags(updated: dict[str, Any]) -> bool:
        """Coerce aliases to list and tags to empty list."""
        changed = False

        if "aliases" in updated:
            aliases = updated["aliases"]
            if isinstance(aliases, str):
                updated["aliases"] = [aliases]
                changed = True
            elif aliases is None:
                updated["aliases"] = []
                changed = True

        if "tags" not in updated or updated["tags"] is None:
            updated["tags"] = []
            changed = True

        return changed

    @staticmethod
    def _fix_task_project_defaults(
        updated: dict[str, Any],
    ) -> bool:
        """Ensure task/project notes have status and priority."""
        note_type = updated.get("type", "note")
        if note_type not in ("task", "project"):
            return False

        changed = False
        if "status" not in updated or not updated["status"]:
            from dx_vault_atlas.shared.logger import logger

            logger.debug(
                f"[Doctor Debug] Task/Project default injecting status='to_do'"
            )
            updated["status"] = "to_do"
            changed = True
        if "priority" not in updated:
            from dx_vault_atlas.shared.logger import logger

            logger.debug(f"[Doctor Debug] Task/Project default injecting priority=1")
            updated["priority"] = 1
            changed = True
        return changed
