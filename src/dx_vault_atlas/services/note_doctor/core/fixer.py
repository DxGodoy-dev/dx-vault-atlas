"""Note Fixing Domain Service."""

from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol

from pydantic_core import PydanticUndefined

from dx_vault_atlas.core.registry import NoteModelRegistry
from dx_vault_atlas.shared.models.enums import (
    NoteArea,
    NoteStatus,
)
from dx_vault_atlas.shared.models.defaults import SCHEMA_VERSION
from dx_vault_atlas.shared.utils.date_resolver import (
    DateResolver,
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
# Rules (Strategy Pattern)
# ---------------------------------------------------------------------------


class FixRuleProtocol(Protocol):
    """Protocol for note fixing rules."""

    def apply(
        self,
        file_path: Path,
        original: dict[str, Any],
        updated: dict[str, Any],
    ) -> bool:
        """Apply the rule to the frontmatter.

        Args:
            file_path: Path to the note file.
            original: The original frontmatter.
            updated: The frontmatter being updated.

        Returns:
            True if changes were made, False otherwise.
        """
        ...


class IntegrityAliasesFixRule:
    """Auto-fixes integrity_aliases if the aliases list is empty."""

    def apply(
        self,
        file_path: Path,
        original: dict[str, Any],
        updated: dict[str, Any],
    ) -> bool:
        logger.debug("[Doctor Debug] Fixer 'IntegrityAliasesFixRule' start")
        title = updated.get("title")
        if not title or not isinstance(title, str):
            return False

        aliases_field = updated.get("aliases")

        # If it's missing, or empty list, or string, we can auto-fix it
        if "aliases" not in updated:
            updated["aliases"] = [title]
            return True

        if isinstance(aliases_field, list) and not aliases_field:
            updated["aliases"] = [title]
            return True

        # EnumFixRule already handles converting string to list, but just in case
        if isinstance(aliases_field, str):
            if title != aliases_field:
                updated["aliases"] = [aliases_field, title]
                return True
            updated["aliases"] = [title]
            return True

        # If it's a list with items but missing the title, we let tui/cli handle the prompt.
        return False


class DateFixRule:
    """Fixes created and updated dates."""

    def __init__(self, date_resolver: DateResolver) -> None:
        self.date_resolver = date_resolver

    def apply(
        self,
        file_path: Path,
        original: dict[str, Any],
        updated: dict[str, Any],
    ) -> bool:
        has_changes = False

        logger.debug(
            f"[Doctor Debug] Fixer 'DateFixRule' start | frontmatter={updated}"
        )

        has_changes = self._fix_created(file_path, original, updated, has_changes)
        has_changes = self._fix_updated(updated, has_changes)

        if has_changes:
            logger.debug(
                f"[Doctor Debug] Fixer 'DateFixRule' applied changes | updated={updated}"
            )
        return has_changes

    def _fix_created(
        self,
        file_path: Path,
        original: dict[str, Any],
        updated: dict[str, Any],
        has_changes: bool,
    ) -> bool:
        true_created = self.date_resolver.resolve_created(file_path, original)
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

    def _fix_updated(self, updated: dict[str, Any], has_changes: bool) -> bool:
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


class EnumFixRule:
    """Fixes enum values (type, status, area, aliases, tags, task/project)."""

    def apply(
        self,
        file_path: Path,
        original: dict[str, Any],
        updated: dict[str, Any],
    ) -> bool:
        has_changes = False

        logger.debug(
            f"[Doctor Debug] Fixer 'EnumFixRule' start | type={updated.get('type')}"
        )

        has_changes |= self._fix_type(updated)
        has_changes |= self._fix_status(updated)
        has_changes |= self._fix_area(updated)
        has_changes |= self._fix_aliases_tags(updated)
        has_changes |= self._fix_task_project_defaults(updated)

        if has_changes:
            logger.debug(
                f"[Doctor Debug] Fixer 'EnumFixRule' applied changes | updated={updated}"
            )
        return has_changes

    @staticmethod
    def _fix_type(updated: dict[str, Any]) -> bool:
        known = set(NoteModelRegistry.get_all().keys()) | {"note"}

        if "type" in updated and isinstance(updated["type"], str):
            val = updated["type"].strip().lower()
            if val.endswith(".md"):
                val = val[:-3]
            if val in known and val != updated["type"]:
                updated["type"] = val
                return True

        if "type" not in updated or not updated["type"]:
            updated["type"] = "note"
            return True

        return False

    @staticmethod
    def _fix_status(updated: dict[str, Any]) -> bool:
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
    def _fix_task_project_defaults(updated: dict[str, Any]) -> bool:
        note_type = updated.get("type", "note")
        if note_type not in ("task", "project"):
            return False

        changed = False
        if "status" not in updated or not updated["status"]:
            logger.debug("[Doctor Debug] Task/Project default injecting status='to_do'")
            updated["status"] = "to_do"
            changed = True
        if "priority" not in updated:
            logger.debug("[Doctor Debug] Task/Project default injecting priority=1")
            updated["priority"] = 1
            changed = True
        return changed


class DefaultsFixRule:
    """Fills missing fields with safe Pydantic defaults."""

    def apply(
        self,
        file_path: Path,
        original: dict[str, Any],
        updated: dict[str, Any],
    ) -> bool:
        has_changes = False
        safe_fields = {"status", "version", "tags"}

        logger.debug(
            f"[Doctor Debug] Fixer 'DefaultsFixRule' start | safe_fields={safe_fields}"
        )

        note_type = updated.get("type")
        if not note_type or not isinstance(note_type, str):
            return False

        model_cls = NoteModelRegistry.get_model(note_type)
        if not model_cls:
            return False

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
                f"[Doctor Debug] Fixer 'DefaultsFixRule' applied changes | updated={updated}"
            )
        return has_changes

    @staticmethod
    def _resolve_field_default(model_cls: type, field_name: str) -> object:
        if field_name not in model_cls.model_fields:
            return _SENTINEL
        info = model_cls.model_fields[field_name]
        if info.default is not None and info.default is not PydanticUndefined:
            val = info.default
            return val.value if hasattr(val, "value") else val
        if info.default_factory is not None:
            return info.default_factory()
        return _SENTINEL


class ExtraneousFieldsFixRule:
    """Removes fields not supported by the note's Pydantic model if it forbids extras."""

    def apply(
        self,
        file_path: Path,
        original: dict[str, Any],
        updated: dict[str, Any],
    ) -> bool:
        logger.debug("[Doctor Debug] Fixer 'ExtraneousFieldsFixRule' start")

        note_type = updated.get("type")
        if not note_type or not isinstance(note_type, str):
            return False

        model_cls = NoteModelRegistry.get_model(note_type)
        if not model_cls:
            return False

        if getattr(model_cls, "model_config", {}).get("extra") == "forbid":
            from dx_vault_atlas.shared.pydantic_utils import strip_unknown_fields

            logger.debug(
                f"[DEBUG TRACE] fixer.ExtraneousFieldsFixRule | Stripping unknowns for {model_cls.__name__}"
            )

            clean_data = strip_unknown_fields(model_cls, updated)

            # Since this is a reference dict, we have to clear and update to preserve the original dict reference
            if clean_data != updated:
                logger.debug(
                    f"[Doctor Debug] Fixer removed extraneous fields | original={list(updated.keys())} -> new={list(clean_data.keys())}"
                )
                updated.clear()
                updated.update(clean_data)
                return True
        else:
            logger.debug(
                f"[Doctor Debug] Fixer 'ExtraneousFieldsFixRule' skipped | model_config.extra={getattr(model_cls, 'model_config', {}).get('extra')}"
            )

        return False


class VersionFixRule:
    """Normalizes the version field to the target SCHEMA_VERSION string."""

    def apply(
        self,
        file_path: Path,
        original: dict[str, Any],
        updated: dict[str, Any],
    ) -> bool:
        logger.debug("[Doctor Debug] Fixer 'VersionFixRule' start")
        if "version" not in updated:
            return False

        current = updated["version"]
        target = str(SCHEMA_VERSION)

        if current != target or not isinstance(current, str):
            updated["version"] = target
            logger.debug(f"[Doctor Debug] Fixer normalized version: {current!r} -> {target!r}")
            return True

        return False


# ---------------------------------------------------------------------------
# Fixer
# ---------------------------------------------------------------------------


class NoteFixer:
    """Applies fixes to note frontmatter based on rules."""

    def __init__(self, rules: list[FixRuleProtocol]) -> None:
        """Initialise the fixer with a list of rules."""
        self.rules = rules

    # -- public API ---------------------------------------------------------

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
        logger.debug("[DEBUG TRACE] fixer.fix Start")
        total_changes = False
        original = current.copy()

        for rule in self.rules:
            if rule.apply(file_path, original, current):
                total_changes = True

        logger.debug(f"[DEBUG TRACE] fixer.fix End | total_changes={total_changes}")
        return total_changes, current, body
