"""Note Doctor application orchestrator."""

import re
from pathlib import Path
from typing import Any

from dx_vault_atlas.services.note_creator.models.enums import (
    NoteArea,
    NoteSource,
    Priority,
)
from dx_vault_atlas.services.note_creator.utils.title_normalizer import (
    TitleNormalizer,
)
from dx_vault_atlas.services.note_doctor.core.fixer import NoteFixer
from dx_vault_atlas.services.note_doctor.core.patcher import (
    FrontmatterPatcher,
)
from dx_vault_atlas.services.note_doctor.tui import DoctorTUI
from dx_vault_atlas.services.note_doctor.validator import (
    MODEL_MAP,
    NoteDoctorValidator,
    ValidationResult,
)
from dx_vault_atlas.services.note_migrator.services.yaml_parser import (
    YamlParserService,
)
from dx_vault_atlas.shared import console as ui
from dx_vault_atlas.shared.config import GlobalConfig
from dx_vault_atlas.shared.core.scanner import VaultScanner
from dx_vault_atlas.shared.logger import logger

# Field → selectable options (used in CLI debug mode)
_ENUM_OPTIONS: dict[str, list[Any]] = {
    "type": list(MODEL_MAP.keys()),
    "source": [x.value for x in NoteSource],
    "area": [x.value for x in NoteArea],
    "priority": [x.value for x in Priority],
}

# Fields handled separately in CLI gather flow
_SKIP_FIELDS = {"title", "aliases", "dates", "version", "status", "tags"}

# Maximum fix attempts before skipping a note
_MAX_FIX_ATTEMPTS = 2


class DoctorApp:
    """Orchestrates the note doctor workflow.

    Responsibilities:
    - Scan vault
    - Validate notes (using Validator)
    - Coordinate fixes (using NoteFixer)
    - Prompt user (using DoctorTUI)
    - Read/Write files (via YamlParser)
    """

    def __init__(self, settings: GlobalConfig) -> None:
        """Initialise DoctorApp with dependencies."""
        self.settings = settings
        self.scanner = VaultScanner()
        self.validator = NoteDoctorValidator()
        self.yaml_parser = YamlParserService()
        self.fixer = NoteFixer()
        self.patcher = FrontmatterPatcher()
        self.tui = DoctorTUI()

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

        ui.show_header(f"Note Doctor {mode_str}")
        ui.console.print(f"[bold]Vault path:[/bold] {self.settings.vault_path}")

        notes = list(self.scanner.scan(self.settings.vault_path))
        ui.console.print(f"\n[bold]Scanning {len(notes)} notes...[/bold]")
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
        ui.console.print(f"\n[green]✓ Fixed dates in {fixed} notes.[/green]")

    def _fix_date_for_note(
        self,
        note_path: Path,
        *,
        save: bool = False,
    ) -> bool:
        """Check and optionally fix dates for a single note."""
        try:
            content = note_path.read_text(encoding="utf-8")
            parsed = self.yaml_parser.parse(content)
        except Exception as e:
            logger.error(f"Error reading {note_path.name}: {e}")
            return False

        date_ok, new_fm = self.fixer.check_and_fix_dates(
            note_path,
            parsed.frontmatter,
        )

        if not date_ok and save:
            try:
                self._write_note(note_path, new_fm, parsed.body)
                ui.console.print(f"[green]Fixed dates for {note_path.name}[/green]")
                return True
            except Exception as e:
                logger.error(f"Error writing {note_path.name}: {e}")
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
            else:
                # outcome is a ValidationResult
                invalid_results.append(outcome)

        self._report_results(
            valid_count,
            warn_count,
            version_count,
            len(invalid_results),
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
            ValidationResult – still invalid after auto-fix
        """
        if debug_mode:
            logger.debug(f"Validating: {note_path.name}")

        result = self.validator.validate(note_path)

        if result.error:
            # File unreadable or gross YAML error - can't auto-fix
            return result

        if debug_mode and not result.is_valid:
            logger.debug(
                f"Invalid | {note_path.name}"
                f" | missing={result.missing_fields}"
                f" | invalid={result.invalid_fields}"
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

        if result.is_valid and not has_changes:
            return self._tag_valid(result, note_path)

        if has_changes:
            if debug_mode:
                logger.debug(f"Auto-fixing | {note_path.name}")

            # Re-validate in memory before writing to disk
            fixed_result = self.validator.validate_content(note_path, fm_final, body)

            if fixed_result.is_valid:
                self._write_note(note_path, fm_final, body)
                return self._tag_valid(fixed_result, note_path)
            result = fixed_result

        if self._is_only_version_issue(result):
            return "version"

        return result

    # -- config-driven mappings ---------------------------------------------

    def _apply_field_mappings(
        self,
        frontmatter: dict[str, Any],
    ) -> bool:
        """Rename frontmatter keys based on ``field_mappings`` config.

        Returns ``True`` if any key was renamed.
        """
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
        """Replace frontmatter values based on ``value_mappings`` config.

        Returns ``True`` if any value was replaced.
        """
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
    ) -> str:
        """Print warnings (if any) and return the tag string."""
        if result.warnings:
            ui.console.print(
                f"[yellow]⚠️  {note_path.name}: {', '.join(result.warnings)}[/yellow]"
            )
            return "warning"
        return "valid"

    @staticmethod
    def _is_only_version_issue(result: ValidationResult) -> bool:
        """Check if the only issue is the version field."""
        issues = set(result.missing_fields) | set(
            result.invalid_fields,
        )
        issues.discard("dates")
        return issues == {"version"}

    # -- reporting ----------------------------------------------------------

    @staticmethod
    def _report_results(
        valid: int,
        warnings: int,
        version_outdated: int,
        invalid: int,
    ) -> None:
        """Print summary report."""
        ui.console.print(f"\n[green]✓[/green] {valid} notes healthy")

        if warnings > 0:
            ui.console.print(
                f"[yellow]⚠️[/yellow] {warnings} notes have"
                " warnings (e.g. unknown source)"
            )
        if version_outdated > 0:
            ui.console.print(
                f"[yellow]![/yellow] {version_outdated} notes"
                " have outdated versions (run 'dxva migrate')"
            )
        if invalid > 0:
            ui.console.print(f"[red]![/red] {invalid} notes need manual attention")
        elif warnings > 0:
            ui.console.print("\n[bold]Doctor finished (with warnings).[/bold]")
        else:
            ui.console.print("\n[bold]Doctor finished.[/bold]")

    # -- interactive repair -------------------------------------------------

    def _process_invalid_results(
        self,
        results: list[ValidationResult],
        debug_mode: bool,
    ) -> None:
        """Process invalid results interactively."""
        if not results:
            return

        ui.console.print()
        for i, result in enumerate(results, 1):
            action = self._process_note(
                result,
                i,
                len(results),
                debug_mode,
            )
            if action == "__quit__":
                return

        ui.console.print("\n[bold]Doctor finished.[/bold]")

    def _process_note(
        self,
        result: ValidationResult,
        index: int,
        total: int,
        debug_mode: bool,
    ) -> str | None:
        """Process a single invalid note interactively.

        Returns ``"__quit__"`` or ``None``.
        """
        file_path = result.file_path
        ui.console.print(f"\n[cyan]━━━ [{index}/{total}] {file_path.name} ━━━[/cyan]")

        # Handle filename mismatch before the fix loop
        if "integrity_filename" in result.invalid_fields:
            rename_out = self._handle_rename(result)
            if rename_out is not None:
                file_path, result = rename_out
                if result.is_valid:
                    ui.console.print(
                        f"[green]Note {file_path.name} is now valid.[/green]"
                    )
                    return None

        frontmatter = dict(result.frontmatter)
        for _attempt in range(_MAX_FIX_ATTEMPTS):
            self._print_issues(
                result.missing_fields,
                result.invalid_fields,
            )

            if debug_mode:
                logger.debug(f"CLI prompt | {file_path.name}")
                fixes = self._gather_fixes_cli(result)
            else:
                fixes = self.tui.gather_fixes(result)

            if not fixes:
                ui.console.print("[yellow]Skipped or no fixes provided.[/yellow]")
                return None
            if fixes.get("__quit__"):
                ui.console.print("[red]Exiting...[/red]")
                return "__quit__"
            if fixes.get("__skip__"):
                ui.console.print("[yellow]Skipping note...[/yellow]")
                return None

            frontmatter = self.patcher.apply_fixes(
                frontmatter,
                fixes,
            )
            self._write_note(file_path, frontmatter, result.body)
            ui.console.print(f"[green]Fixed {file_path.name}[/green]")

            result = self.validator.validate(file_path)
            if result.is_valid:
                ui.console.print(f"[green]Note {file_path.name} is now valid.[/green]")
                return None

            frontmatter = dict(result.frontmatter)
            ui.console.print("[yellow]Note still has issues. Continuing...[/yellow]")

        ui.console.print(
            f"[red]Could not fully fix {file_path.name} "
            f"after {_MAX_FIX_ATTEMPTS} attempts. Skipping.[/red]"
        )
        return None

    # -- helpers (printing / writing) ---------------------------------------

    def _handle_rename(
        self,
        result: ValidationResult,
    ) -> tuple[Path, ValidationResult] | None:
        """Offer to rename file to match title.

        Returns:
            ``(new_path, new_result)`` on success, or ``None``.
        """
        title = result.frontmatter.get("title", "")
        if not title:
            return None

        stem = result.file_path.stem
        from dx_vault_atlas.services.note_doctor.core.date_resolver import DateResolver

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

        ui.console.print(
            f"[yellow]Filename mismatch:[/yellow] {result.file_path.name} → {new_name}"
        )
        if not ui.confirm("Rename file?", default=True):
            return None

        result.file_path.rename(new_path)
        ui.console.print(f"[green]Renamed → {new_name}[/green]")
        new_result = self.validator.validate(new_path)
        return new_path, new_result

    @staticmethod
    def _print_issues(
        missing: list[str],
        invalid: list[str],
    ) -> None:
        """Print missing and invalid fields."""
        if missing:
            ui.console.print(f"[yellow]Missing:[/yellow] {', '.join(missing)}")
        real = [x for x in invalid if x != "dates"]
        if real:
            ui.console.print(f"[red]Invalid:[/red] {', '.join(real)}")

    def _write_note(
        self,
        file_path: Path,
        frontmatter: dict[str, Any],
        body: str,
    ) -> None:
        """Write updated note to disk."""
        yaml_content = self.yaml_parser.serialize_frontmatter(
            frontmatter,
        )
        file_path.write_text(
            yaml_content + body,
            encoding="utf-8",
        )

    # -- helpers (CLI gather) -----------------------------------------------

    def _gather_fixes_cli(
        self,
        result: ValidationResult,
    ) -> dict[str, Any]:
        """Gather fixes via CLI input (debug mode)."""
        fixes: dict[str, Any] = {}

        self._handle_title_fix(result, fixes)
        self._handle_field_fixes(result, fixes)

        return fixes

    @staticmethod
    def _handle_title_fix(
        result: ValidationResult,
        fixes: dict[str, Any],
    ) -> None:
        """Handle title/aliases repair in CLI mode."""
        if "title" in result.missing_fields:
            if ui.confirm(
                f"Missing title for {result.file_path.name}. Fix?",
                default=True,
            ):
                title = ui.query("Enter title")
                fixes["title"] = title
                fixes["aliases"] = [title]
            return

        needs_aliases = (
            "aliases" in result.missing_fields or "aliases" in result.invalid_fields
        )
        if needs_aliases:
            existing = result.frontmatter.get("title", "").strip(
                '"',
            )
            if existing:
                fixes["aliases"] = [existing]

    def _handle_field_fixes(
        self,
        result: ValidationResult,
        fixes: dict[str, Any],
    ) -> None:
        """Handle non-title field repairs in CLI mode."""
        issues = (
            set(result.missing_fields) | set(result.invalid_fields)
        ) - _SKIP_FIELDS

        for field in issues:
            if not ui.confirm(
                f"Issue with '{field}'. Fix?",
                default=True,
            ):
                continue

            if field in _ENUM_OPTIONS:
                val = self._gather_enum_selection(
                    field,
                    _ENUM_OPTIONS[field],
                )
                if val is not None:
                    fixes[field] = val
            else:
                fixes[field] = ui.query(
                    f"Enter value for {field}",
                )

    @staticmethod
    def _gather_enum_selection(
        field: str,
        options: list[str | int],
    ) -> str | int:
        """Present a numbered menu for enum selection."""
        ui.console.print(f"Select {field}:")
        for idx, opt in enumerate(options, 1):
            ui.console.print(f"{idx}. {opt}")

        while True:
            sel = ui.query(f"Choose (1-{len(options)})")
            try:
                idx = int(sel)
                if 1 <= idx <= len(options):
                    return options[idx - 1]
                ui.console.print(
                    f"[red]Invalid selection. Choose 1-{len(options)}[/red]"
                )
            except ValueError:
                ui.console.print("[red]Please enter a number.[/red]")


def create_app(settings: GlobalConfig) -> DoctorApp:
    """Create DoctorApp instance."""
    return DoctorApp(settings)
