"""Note Doctor application orchestrator."""

from pathlib import Path
from typing import Any

from dx_vault_atlas.shared.utils.title_normalizer import (
    TitleNormalizer,
)
from dx_vault_atlas.services.note_doctor.core.cli import DoctorCLI
from dx_vault_atlas.shared.utils.date_resolver import DateResolver
from dx_vault_atlas.services.note_doctor.core.fixer import (
    DateFixRule,
    DefaultsFixRule,
    EnumFixRule,
    ExtraneousFieldsFixRule,
    NoteFixer,
    VersionFixRule,
)
from dx_vault_atlas.shared.core.io import NoteIOService
from dx_vault_atlas.services.note_doctor.core.patcher import (
    FrontmatterPatcher,
)
from dx_vault_atlas.services.note_doctor.tui import DoctorTUI
from dx_vault_atlas.services.note_doctor.validator import (
    NoteDoctorValidator,
    ValidationResult,
)
from dx_vault_atlas.shared.yaml_parser import (
    YamlParserService,
)
from dx_vault_atlas.shared.config import GlobalConfig
from dx_vault_atlas.shared.core.scanner import VaultScanner
from dx_vault_atlas.shared.logger import logger

# Maximum fix attempts before skipping a note
_MAX_FIX_ATTEMPTS = 2


class DoctorApp:
    """Orchestrates the note doctor workflow.

    Responsibilities:
    - Scan vault
    - Validate notes (using Validator)
    - Coordinate fixes (using NoteFixer)
    - Prompt user (via CLI / TUI)
    - Read/Write files (via IO Service)
    """

    def __init__(
        self,
        settings: GlobalConfig,
        cli: DoctorCLI,
        io_service: NoteIOService,
        model_map: dict[str, Any],
    ) -> None:
        """Initialise DoctorApp with dependencies."""
        self.settings = settings
        self.cli = cli
        self.io = io_service
        self.scanner = VaultScanner()
        self.yaml_parser = YamlParserService()
        self.date_resolver = DateResolver()
        self.validator = NoteDoctorValidator(yaml_parser=self.yaml_parser)

        # Instantiate fix rules
        self.date_rule = DateFixRule(self.date_resolver)
        self.enum_rule = EnumFixRule()
        self.defaults_rule = DefaultsFixRule()
        self.extraneous_rule = ExtraneousFieldsFixRule()
        self.version_rule = VersionFixRule()

        from dx_vault_atlas.services.note_doctor.core.fixer import (
            IntegrityAliasesFixRule,
        )

        self.integrity_aliases_rule = IntegrityAliasesFixRule()

        self.fixer = NoteFixer(
            rules=[
                self.date_rule,
                self.enum_rule,
                self.defaults_rule,
                self.extraneous_rule,
                self.version_rule,
                self.integrity_aliases_rule,
            ]
        )
        self.patcher = FrontmatterPatcher()
        self.tui = DoctorTUI(model_map=model_map)

    # -- public API ---------------------------------------------------------

    def run(
        self,
        fix_date: bool = False,
        debug_mode: bool = False,
    ) -> None:
        """Execute the doctor workflow."""
        mode_str = "(date fix only)" if fix_date else "(full check)"
        if debug_mode:
            logger.debug(f"Doctor start | mode={mode_str}")

        self.cli.show_header(mode_str, str(self.settings.vault_path))

        notes = list(self.scanner.scan(self.settings.vault_path))
        self.cli.show_scan_count(len(notes))
        if debug_mode:
            logger.debug(f"Found {len(notes)} notes in scan")

        if fix_date:
            self._run_date_fix_mode(notes)
        else:
            self._run_full_check_mode(notes, debug_mode)

    # -- date-only mode -----------------------------------------------------

    def _run_date_fix_mode(self, notes: list[Path]) -> None:
        """Run only date fixing logic."""
        fixed = sum(1 for n in notes if self._fix_date_for_note(n, save=True))
        self.cli.show_date_fix_result(fixed)

    def _fix_date_for_note(
        self,
        note_path: Path,
        *,
        save: bool = False,
    ) -> bool:
        """Check and optionally fix dates for a single note."""
        parsed = self.io.read_note(note_path)
        if not parsed:
            return False

        new_fm = parsed.frontmatter.copy()
        has_changes = self.date_rule.apply(
            note_path,
            parsed.frontmatter,
            new_fm,
        )
        date_ok = not has_changes

        if not date_ok and save:
            if self.io.write_note(note_path, new_fm, parsed.body):
                self.cli.show_note_date_fixed(note_path.name)
                return True
            return False

        return not date_ok

    # -- full-check mode ----------------------------------------------------

    def _run_full_check_mode(
        self,
        notes: list[Path],
        debug_mode: bool,
    ) -> None:
        """Run full validation and repair logic."""
        invalid_results: list[ValidationResult] = []
        valid_count = 0
        warn_count = 0
        version_count = 0
        fixed_count = 0

        for note_path in notes:
            outcome = self._classify_note(
                note_path,
                debug_mode,
            )
            if outcome == "valid":
                valid_count += 1
            elif outcome == "warning":
                warn_count += 1
            elif outcome == "version":
                version_count += 1
            elif outcome == "fixed":
                fixed_count += 1
            else:
                # outcome is a ValidationResult
                invalid_results.append(outcome)

        self.cli.report_results(
            valid_count,
            warn_count,
            version_count,
            len(invalid_results),
            fixed_count,
        )
        self._process_invalid_results(invalid_results, debug_mode)

    def _classify_note(
        self,
        note_path: Path,
        debug_mode: bool,
    ) -> str | ValidationResult:
        """Validate, auto-fix, and classify a single note.

        Returns:
            "valid"   – healthy with no warnings
            "warning" – healthy but has warnings
            "version" – only version is outdated
            "fixed"   – was auto-fixed and is now healthy
            ValidationResult – still invalid after auto-fix
        """
        if debug_mode:
            logger.debug(
                "[Doctor Debug] --------------------------------------------------"
            )
            logger.debug(f"[Doctor Debug] Validating: {note_path.name}")
            logger.debug("[DEBUG TRACE] app._classify_note Start")

        result = self.validator.validate(note_path)

        if debug_mode and not result.error:
            logger.debug("[DEBUG TRACE] app._classify_note After Validator")

        if result.error:
            # File unreadable or gross YAML error - can't auto-fix
            return result

        if debug_mode and not result.is_valid:
            logger.debug(
                f"[Doctor Debug] Invalid | {note_path.name}"
                f" | missing={result.missing_fields}"
                f" | invalid={result.invalid_fields}"
            )

        if debug_mode:
            print(
                f"!!! DOCTOR DEBUG: _classify_note | type before fixer={result.frontmatter.get('type')} | path={note_path.name}"
            )
        has_changes, fm_final, body = self.fixer.fix(
            note_path,
            result.frontmatter.copy(),
            result.body,
        )

        # Apply config-driven mappings
        if self._apply_field_mappings(fm_final):
            has_changes = True
        if self._apply_value_mappings(fm_final):
            has_changes = True

        # Strip extraneous fields that config mappings may have introduced
        original_fm_final = fm_final.copy()
        rule_made_changes = self.extraneous_rule.apply(
            note_path,
            original_fm_final,
            fm_final,
        )
        unchanged = not rule_made_changes
        if not unchanged:
            has_changes = True

        if debug_mode:
            print(
                f"!!! DOCTOR DEBUG: _classify_note | type after mappings={fm_final.get('type')} | has_changes={has_changes}"
            )
            logger.debug(
                f"[DEBUG TRACE] app._classify_note After Mappings | has_changes={has_changes}"
            )

        if result.is_valid and not has_changes:
            if debug_mode:
                logger.debug(
                    f"[Doctor Debug] Note valid and unchanged | {note_path.name}"
                )
            return self._tag_valid(result, note_path)

        if has_changes:
            if debug_mode:
                logger.debug(
                    f"[Doctor Debug] Auto-fixing | {note_path.name} | has_changes=True"
                )
                logger.debug(f"[Doctor Debug] Frontmatter AFTER fix: {fm_final}")

            # Re-validate in memory before writing to disk
            fixed_result = self.validator.validate_content(note_path, fm_final, body)

            if fixed_result.is_valid:
                if debug_mode:
                    logger.debug(
                        "[Doctor Debug] Re-validation passed. Writing auto-fixed note."
                    )
                self.io.write_note(note_path, fm_final, body)
                self.cli.show_note_fixed(note_path.name)
                return self._tag_valid(fixed_result, note_path, was_fixed=True)

            if debug_mode:
                logger.debug(
                    f"[Doctor Debug] Re-validation failed. Still invalid | "
                    f"missing={fixed_result.missing_fields} | invalid={fixed_result.invalid_fields}"
                )
            result = fixed_result

        if self._is_only_version_issue(result):
            return "version"

        return result

    # -- config-driven mappings ---------------------------------------------

    def _apply_field_mappings(
        self,
        frontmatter: dict[str, Any],
    ) -> bool:
        """Rename frontmatter keys based on ``field_mappings`` config."""
        changed = False
        for old_key, new_key in self.settings.field_mappings.items():
            if old_key in frontmatter:
                if new_key not in frontmatter:
                    frontmatter[new_key] = frontmatter[old_key]
                del frontmatter[old_key]
                changed = True
        return changed

    def _apply_value_mappings(
        self,
        frontmatter: dict[str, Any],
    ) -> bool:
        """Replace frontmatter values based on ``value_mappings`` config."""
        changed = False
        for field, replacements in self.settings.value_mappings.items():
            if field in frontmatter and isinstance(
                frontmatter[field],
                str,
            ):
                old_val = frontmatter[field]
                if old_val in replacements:
                    frontmatter[field] = replacements[old_val]
                    changed = True
        return changed

    def _tag_valid(
        self,
        result: ValidationResult,
        note_path: Path,
        was_fixed: bool = False,
    ) -> str:
        """Print warnings (if any) and return the tag string."""
        self.cli.show_note_warnings(note_path.name, result.warnings)
        if result.warnings:
            return "warning"
        if was_fixed:
            return "fixed"
        return "valid"

    @staticmethod
    def _is_only_version_issue(result: ValidationResult) -> bool:
        """Check if the only issue is the version field."""
        issues = set(result.missing_fields) | set(
            result.invalid_fields,
        )
        issues.discard("dates")
        return issues == {"version"}

    # -- interactive repair -------------------------------------------------

    def _process_invalid_results(
        self,
        results: list[ValidationResult],
        debug_mode: bool,
    ) -> None:
        """Process invalid results interactively."""
        if not results:
            return

        for i, result in enumerate(results, 1):
            action = self._process_note(
                result,
                i,
                len(results),
                debug_mode,
            )
            if action == "__quit__":
                return

        self.cli.show_doctor_finished()

    def _process_note(
        self,
        result: ValidationResult,
        index: int,
        total: int,
        debug_mode: bool,
    ) -> str | None:
        """Process a single invalid note interactively."""
        file_path = result.file_path
        self.cli.show_note_header(index, total, file_path.name)

        # Handle filename mismatch before the fix loop
        if "integrity_filename" in result.invalid_fields:
            rename_out = self._handle_rename(result)
            if rename_out is not None:
                file_path, result = rename_out
                if result.is_valid:
                    self.cli.show_note_valid(file_path.name)
                    return None

        frontmatter = dict(result.frontmatter)
        for _attempt in range(_MAX_FIX_ATTEMPTS):
            self.cli.print_issues(
                result.missing_fields,
                result.invalid_fields,
            )

            if debug_mode:
                logger.debug(f"CLI prompt | {file_path.name}")
                logger.debug("[DEBUG TRACE] app._process_note Before Fix Gather")
                fixes = self.cli.gather_fixes(result)
            else:
                fixes = self.tui.gather_fixes(result)

            if debug_mode:
                logger.debug(
                    f"[DEBUG TRACE] app._process_note Fixes Gathered = {fixes}"
                )

            if not fixes:
                self.cli.show_skip_or_no_fixes()
                return None
            if fixes.get("__quit__"):
                self.cli.show_exiting()
                return "__quit__"
            if fixes.get("__skip__"):
                self.cli.show_skipping_note()
                return None

            frontmatter = self.patcher.apply_fixes(
                frontmatter,
                fixes,
            )
            if debug_mode:
                logger.debug("[DEBUG TRACE] app._process_note After Patcher")

            # Strip fields not allowed by the note's Pydantic model
            original_for_rules = frontmatter.copy()
            self.extraneous_rule.apply(
                file_path,
                original_for_rules,
                frontmatter,
            )
            if debug_mode:
                logger.debug(
                    "[DEBUG TRACE] app._process_note After check_and_fix_extraneous"
                )

            self.io.write_note(file_path, frontmatter, result.body)
            self.cli.show_note_fixed(file_path.name)

            result = self.validator.validate(file_path)
            if result.is_valid:
                if debug_mode:
                    logger.debug("[Doctor Debug] TUI fix successful. Note is valid.")
                self.cli.show_note_valid(file_path.name)
                return None

            frontmatter = dict(result.frontmatter)
            if debug_mode:
                logger.debug(
                    f"[Doctor Debug] TUI fix still failed! | "
                    f"missing={result.missing_fields} | invalid={result.invalid_fields}"
                )
            self.cli.show_fix_failed()

        self.cli.show_max_attempts_reached(file_path.name, _MAX_FIX_ATTEMPTS)
        return None

    # -- helpers ------------------------------------------------------------

    def _handle_rename(
        self,
        result: ValidationResult,
    ) -> tuple[Path, ValidationResult] | None:
        """Offer to rename file to match title."""
        title = result.frontmatter.get("title", "")
        if not title:
            return None

        stem = result.file_path.stem

        created = result.frontmatter.get("created")
        from datetime import datetime
        if created and isinstance(created, datetime):
            prefix = created.strftime("%Y%m%d%H%M%S") + "_"
        else:
            ts_match = DateResolver.extract_timestamp_from_stem(stem)

            # Determine prefix and clean stem
            if ts_match:
                # Check if there is a separator directly after the timestamp
                separator_len = 0
                if len(stem) > len(ts_match) and stem[len(ts_match)] in ("_", "-"):
                    separator_len = 1
                prefix = stem[: len(ts_match) + separator_len]
            else:
                prefix = ""

        norm_title = TitleNormalizer.sanitize(title)
        new_name = f"{prefix}{norm_title}{result.file_path.suffix}"
        new_path = result.file_path.parent / new_name

        if new_path == result.file_path:
            return None

        if not self.cli.prompt_rename(result.file_path.name, new_name):
            return None

        success = self.io.rename_note(result.file_path, new_path)
        if success:
            self.cli.show_renamed(new_name)
            new_result = self.validator.validate(new_path)
            return new_path, new_result
        return None


def create_app(settings: GlobalConfig) -> DoctorApp:
    """Create DoctorApp instance."""
    # Ensure models are registered
    import dx_vault_atlas.shared.models.note  # noqa: F401
    from dx_vault_atlas.core.registry import NoteModelRegistry

    yaml_parser = YamlParserService()
    io_service = NoteIOService(yaml_parser)
    cli = DoctorCLI()

    return DoctorApp(
        settings=settings,
        cli=cli,
        io_service=io_service,
        model_map=NoteModelRegistry.get_all(),
    )
