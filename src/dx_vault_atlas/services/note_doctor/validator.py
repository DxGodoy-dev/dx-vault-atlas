"""Validator for Note Doctor Service."""

import re
from pathlib import Path
from typing import Any

from packaging.version import parse as parse_version
from pydantic import ValidationError

from dx_vault_atlas.services.note_creator.defaults import SCHEMA_VERSION
from dx_vault_atlas.services.note_creator.models.enums import (
    NoteArea,
    NoteSource,
    Priority,
)
from dx_vault_atlas.services.note_creator.models.note import (
    BaseNote,
    InfoNote,
    MocNote,
    ProjectNote,
    RefNote,
    TaskNote,
)
from dx_vault_atlas.services.note_creator.utils.title_normalizer import (
    TitleNormalizer,
)
from dx_vault_atlas.services.note_migrator.services.yaml_parser import (
    YamlParseError,
    YamlParserService,
)
from dx_vault_atlas.shared.logger import logger
from dx_vault_atlas.shared.pydantic_utils import strip_unknown_fields

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MODEL_MAP: dict[str, type[BaseNote]] = {
    "project": ProjectNote,
    "task": TaskNote,
    "info": InfoNote,
    "moc": MocNote,
    "ref": RefNote,
}

_TARGET_VERSION = parse_version(SCHEMA_VERSION)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _normalize(text: str) -> str:
    """Sanitize text for comparison, stripping accents and timestamps."""
    text = TitleNormalizer.sanitize(text)
    return re.sub(r"^\d{12,14}_", "", text)


def _format_pydantic_errors(exc: ValidationError) -> str:
    """Format Pydantic errors as a concise, human-readable string."""
    parts = []
    for err in exc.errors():
        field = ".".join(str(loc) for loc in err["loc"]) or "unknown"
        parts.append(f"{field} → {err['msg']}")
    return "; ".join(parts)


# ---------------------------------------------------------------------------
# Data class
# ---------------------------------------------------------------------------


class ValidationResult:
    """Result of a single note validation."""

    def __init__(
        self,
        file_path: Path,
        is_valid: bool,
        frontmatter: dict[str, Any] | None = None,
        body: str = "",
        missing_fields: list[str] | None = None,
        invalid_fields: list[str] | None = None,
        warnings: list[str] | None = None,
        error: str | None = None,
    ) -> None:
        """Initialise with validation outcome details."""
        self.file_path = file_path
        self.is_valid = is_valid
        self.frontmatter = frontmatter or {}
        self.body = body
        self.missing_fields = missing_fields or []
        self.invalid_fields = invalid_fields or []
        self.warnings = warnings or []
        self.error = error


# ---------------------------------------------------------------------------
# Validator
# ---------------------------------------------------------------------------


class NoteDoctorValidator:
    """Validates notes using Pydantic models and enum checks."""

    def __init__(self) -> None:
        """Initialise the validator with a YAML parser."""
        self.yaml_parser = YamlParserService()

    # -- public API ---------------------------------------------------------

    def validate(self, file_path: Path) -> ValidationResult:
        """Validate a note file against schema and business rules."""
        result = self._read_and_parse(file_path)
        if isinstance(result, ValidationResult):
            return result
        frontmatter, body = result
        return self.validate_content(file_path, frontmatter, body)

    def validate_content(
        self, file_path: Path, frontmatter: dict[str, Any], body: str
    ) -> ValidationResult:
        """Validate a note in-memory against schema and business rules."""
        logger.debug(
            f"[DEBUG TRACE] validator.validate_content Start | path={file_path.name} | 'source' in frontmatter: {'source' in frontmatter}"
        )
        note_type = frontmatter.get("type")
        if not note_type or not isinstance(note_type, str):
            return ValidationResult(
                file_path,
                False,
                frontmatter,
                body,
                missing_fields=["type"],
            )

        missing = self._check_required(note_type, frontmatter)
        invalid = self._check_integrity(file_path, frontmatter)
        warnings: list[str] = []

        self._check_enums(frontmatter, invalid, warnings)
        self._check_version(frontmatter, invalid)

        model_cls = MODEL_MAP.get(note_type)
        if model_cls:
            self._run_pydantic(
                model_cls,
                file_path,
                frontmatter,
                invalid,
                missing,
            )

        if missing or invalid:
            logger.debug(
                f"Validation failed | {file_path.name}"
                f" | missing={missing} | invalid={invalid}"
            )
            return ValidationResult(
                file_path,
                False,
                frontmatter,
                body,
                missing,
                invalid,
                warnings,
            )

        logger.debug(
            f"Validation passed | {file_path.name}"
            + (f" | warnings={warnings}" if warnings else "")
        )
        return ValidationResult(
            file_path,
            True,
            frontmatter,
            body,
            warnings=warnings,
        )

    # -- private helpers (read / parse) -------------------------------------

    def _read_and_parse(
        self,
        file_path: Path,
    ) -> ValidationResult | tuple[dict[str, Any], str]:
        """Read and parse a note, returning early on errors."""
        try:
            content = file_path.read_text(encoding="utf-8")
        except OSError as e:
            return ValidationResult(
                file_path,
                False,
                error=f"Read error: {e}",
            )

        try:
            parsed = self.yaml_parser.parse(content)
        except YamlParseError as e:
            return ValidationResult(
                file_path,
                False,
                error=f"YAML error: {e}",
            )

        return parsed.frontmatter, parsed.body

    # -- private helpers (field checks) -------------------------------------

    def _check_required(
        self,
        note_type: str,
        frontmatter: dict[str, Any],
    ) -> list[str]:
        """Return list of missing required fields based on Pydantic models."""
        model_cls = MODEL_MAP.get(note_type)
        if not model_cls:
            return []

        missing = []
        for name, field_info in model_cls.model_fields.items():
            if field_info.is_required():
                key = field_info.alias if field_info.alias else name
                if key not in frontmatter:
                    missing.append(key)
        return missing

    def _check_integrity(
        self,
        file_path: Path,
        frontmatter: dict[str, Any],
    ) -> list[str]:
        """Check title-vs-filename and title-in-aliases consistency."""
        invalid: list[str] = []
        title = frontmatter.get("title")
        aliases = frontmatter.get("aliases")

        if title and isinstance(title, str):
            norm_title = _normalize(title)
            norm_fname = _normalize(file_path.stem)
            if norm_title != norm_fname:
                invalid.append("integrity_filename")

        if (
            title
            and aliases
            and isinstance(aliases, (list, tuple))
            and title not in aliases
        ):
            invalid.append("integrity_aliases")

        return invalid

    # -- private helpers (enum + version checks) ----------------------------

    def _check_enums(
        self,
        frontmatter: dict[str, Any],
        invalid: list[str],
        warnings: list[str],
    ) -> None:
        """Validate priority, source and area enum values in-place."""
        self._check_priority(frontmatter, invalid)
        self._check_source(frontmatter, warnings)
        self._check_area(frontmatter, invalid)

    def _check_priority(
        self,
        frontmatter: dict[str, Any],
        invalid: list[str],
    ) -> None:
        """Flag invalid priority values."""
        val = frontmatter.get("priority")
        if val is None:
            return
        try:
            Priority(val)
        except ValueError:
            invalid.append("priority")

    def _check_source(
        self,
        frontmatter: dict[str, Any],
        warnings: list[str],
    ) -> None:
        """Warn on non-enum source values (lenient)."""
        val = frontmatter.get("source")
        if not val:
            return
        try:
            NoteSource(val)
        except ValueError:
            if isinstance(val, str) and val.strip():
                warnings.append(f"unknown_source: {val}")

    def _check_area(
        self,
        frontmatter: dict[str, Any],
        invalid: list[str],
    ) -> None:
        """Flag invalid area values."""
        val = frontmatter.get("area")
        if not val:
            return
        try:
            NoteArea(val)
        except ValueError:
            invalid.append("area")

    def _check_version(
        self,
        frontmatter: dict[str, Any],
        invalid: list[str],
    ) -> None:
        """Flag outdated schema versions."""
        raw = str(frontmatter.get("version", ""))
        if not raw:
            return
        current = parse_version(raw)
        if current < _TARGET_VERSION and "version" not in invalid:
            invalid.append("version")

    # -- private helpers (pydantic) -----------------------------------------

    def _run_pydantic(
        self,
        model_cls: type[BaseNote],
        file_path: Path,
        frontmatter: dict[str, Any],
        invalid: list[str],
        missing: list[str],
    ) -> None:
        """Run Pydantic model validation, appending new issues."""
        try:
            # Only pass fields the model knows about
            filtered = strip_unknown_fields(model_cls, frontmatter)
            logger.debug(
                f"[DEBUG TRACE] validator._run_pydantic | class={model_cls.__name__} | 'source' in filtered: {'source' in filtered} | 'source' in fm: {'source' in frontmatter}"
            )
            model_cls(**filtered)
        except ValidationError as e:
            logger.debug(
                f"Pydantic errors | {file_path.name}: {_format_pydantic_errors(e)}"
            )
            for error in e.errors():
                logger.debug(
                    f"[DEBUG TRACE] validator._run_pydantic Error item | type={error['type']} | loc={error['loc']}"
                )
                # Skip "extra_forbidden" errors — extraneous fields are
                # handled by the fixer's check_and_fix_extraneous step.
                if error["type"] == "extra_forbidden":
                    continue
                loc = error["loc"]
                field = str(loc[0]) if loc else "unknown"
                if field not in invalid and field not in missing:
                    invalid.append(field)
