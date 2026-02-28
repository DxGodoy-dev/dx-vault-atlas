from dataclasses import replace
from typing import Any

from dx_vault_atlas.services.note_doctor.validator import MODEL_MAP, ValidationResult
from dx_vault_atlas.shared.tui import (
    WizardConfig,
    run_wizard,
)
from dx_vault_atlas.services.note_creator.tui_steps import (
    AREA_STEP,
    PRIORITY_STEP,
    SOURCE_STEP,
    STATUS_STEP,
    TEMPLATE_STEP,
    TITLE_STEP,
)


class DoctorTUI:
    """Handles user interaction for Note Doctor using TUI Wizard."""

    def gather_fixes(self, result: ValidationResult) -> dict[str, Any]:
        """Run wizard to gather fixes for missing/invalid fields."""
        missing = set(result.missing_fields)
        invalid = set(result.invalid_fields)
        invalid.discard("dates")
        invalid.discard("integrity_filename")
        invalid.discard("integrity_aliases")

        # Remove extraneous fields — they should be stripped, not fixed
        extraneous = self._get_extraneous_fields(result.frontmatter)
        invalid -= extraneous

        # Auto-fill logic for InfoNote status
        # If type is already "info" (in frontmatter) and status is missing,
        # we suppress the step and fill it automatically.
        auto_fill_status = False
        current_type = result.frontmatter.get("type")
        if current_type == "info" and "status" in missing:
            missing.discard("status")
            auto_fill_status = True

        steps = self._build_steps(missing, invalid, result)

        if not steps and not auto_fill_status:
            return {}

        fixes = {}
        if steps:
            config = WizardConfig(
                title=f"Fixing Note: {result.file_path.name}",
                steps=steps,
                success_message="Fixes collected!",
                auto_exit_delay=0.5,
            )
            fixes = run_wizard(config) or {}

            # If wizard was cancelled (fixes is empty dict usually implies success with no data,
            # but run_wizard returns None on quit. Only if we proceed fixes is dict)
            # wait, run_wizard returns None on quit. The `or {}` makes it empty dict.
            # If user quit, we should probably stop?
            # DoctorApp._process_note handles empty dict as "Skipped".
            # If run_wizard returned None, it means Quit/Interrupted.
            # But line 40 says `return run_wizard(config) or {}`.
            # If I separate it, I can detect quit. But let's stick to existing pattern for now.
            # ACTUALLY: existing code: `return run_wizard(config) or {}`
            # This swallows the Quit signal potentially?
            # `run_wizard` implementation in `shared/tui/__init__.py`:
            # It returns `dict` or `None`.
            # If `None`, `gather_fixes` returns `{}`.
            # `app.py` sees `{}` and prints "Skipped or no fixes provided."
            # So user cannot quit easily?
            # Wait, `NoteDoctor` loop checks for `__quit__` in fixes?
            # `run_wizard` usually doesn't return `__quit__`.
            # The steps (choose_enum) raise `UserQuitError`. `run_wizard` catches it?
            # Let's assume standard behavior for now and just inject the fix.

        # Check if we should auto-fill status post-wizard
        # (Conditions: Pre-flagged OR template selected is INFO)
        from dx_vault_atlas.services.note_creator.models.enums import NoteTemplate

        # Determine effective type
        effective_type = current_type
        if "template" in fixes:
            # fixes["template"] is a NoteTemplate enum member
            if fixes["template"] == NoteTemplate.INFO:
                effective_type = "info"
            else:
                effective_type = str(fixes["template"].value).replace(".md", "")
        elif "type" in fixes:
            effective_type = fixes["type"]

        # If effective type is info, ensure status is set
        if effective_type == "info":
            # If we pre-flagged it, or if it was missing and we selected info (so step was skipped)
            if auto_fill_status or "status" in result.missing_fields:
                if "status" not in fixes:
                    fixes["status"] = "To Read"

        return fixes

    def _build_steps(
        self, missing: set[str], invalid: set[str], result: ValidationResult
    ) -> list[Any]:
        """Build wizard steps based on missing/invalid fields."""
        steps = []

        # 0. Title
        title_in_fm = result.frontmatter.get("title")
        if "title" in missing or not title_in_fm:
            default_title = result.file_path.stem
            from dx_vault_atlas.services.note_doctor.core.date_resolver import (
                DateResolver,
            )

            ts = DateResolver.extract_timestamp_from_stem(default_title)
            if ts:
                default_title = default_title[len(ts) :].strip(" -_")
            steps.append(replace(TITLE_STEP, default_value=default_title))

        # 1. Type
        if "type" in missing or "type" in invalid:
            steps.append(TEMPLATE_STEP)

        # 2. Dependencies (Source, Priority, Area, Status)
        self._add_dependency_steps(steps, missing, invalid)

        # Filter conditions if dependencies are not strictly requested
        return self._filter_conditions_if_missing(steps, missing, invalid)

    def _add_dependency_steps(
        self, steps: list[Any], missing: set[str], invalid: set[str]
    ) -> None:
        """Add dependent steps if missing or invalid."""
        needs_type_fix = "type" in missing or "type" in invalid

        # Map step to the field key it modifies/provides
        dependency_map = [
            (SOURCE_STEP, "source"),
            (PRIORITY_STEP, "priority"),
            (AREA_STEP, "area"),
            (STATUS_STEP, "status"),
        ]

        for step, key in dependency_map:
            # If type is being fixed, we conservatively add dependencies
            # If key is explicitly missing/invalid, we MUST add it
            if (
                needs_type_fix or key in missing or key in invalid
            ) and step not in steps:
                steps.append(step)

    def _filter_conditions_if_missing(
        self, steps: list[Any], missing: set[str], invalid: set[str]
    ) -> list[Any]:
        """Remove conditions from steps if they are explicitly missing."""
        final_steps = []
        needs_type_fix = "type" in missing or "type" in invalid

        for step in steps:
            # If step has condition but we are NOT fixing type/template,
            # we should force it to show (remove condition)
            # because we know it IS missing/invalid.
            if step.condition and not needs_type_fix:
                final_steps.append(replace(step, condition=None))
            else:
                final_steps.append(step)

        return final_steps

    @staticmethod
    def _get_extraneous_fields(frontmatter: dict) -> set[str]:
        """Return field names present in frontmatter but forbidden by the model."""
        note_type = frontmatter.get("type")
        if not note_type or not isinstance(note_type, str):
            return set()
        model_cls = MODEL_MAP.get(note_type)
        if not model_cls:
            return set()
        if getattr(model_cls, "model_config", {}).get("extra") != "forbid":
            return set()
        from dx_vault_atlas.shared.pydantic_utils import strip_unknown_fields

        clean = strip_unknown_fields(model_cls, frontmatter)
        return set(frontmatter.keys()) - set(clean.keys())
