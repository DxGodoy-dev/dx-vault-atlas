"""CLI service for Note Doctor."""

from typing import Any

from dx_vault_atlas.core.registry import NoteModelRegistry
from dx_vault_atlas.services.note_creator.models.enums import (
    NoteArea,
    Priority,
)
from dx_vault_atlas.services.note_doctor.validator import (
    ValidationResult,
)
from dx_vault_atlas.shared import console as ui

# Field → selectable options (used in CLI debug mode)
_ENUM_OPTIONS: dict[str, list[Any]] = {
    "type": list(NoteModelRegistry.get_all().keys()),
    "area": [e.value for e in NoteArea],
    "priority": [e.value for e in Priority],
}

# Fields handled separately in CLI gather flow
_SKIP_FIELDS = {"title", "aliases", "dates", "version", "status", "tags"}


class DoctorCLI:
    """Service handling all interactive CLI I/O and display."""

    def show_header(self, mode_str: str, vault_path: str) -> None:
        """Show start header."""
        ui.show_header(f"Note Doctor {mode_str}")
        ui.console.print(f"[bold]Vault path:[/bold] {vault_path}")

    def show_scan_count(self, count: int) -> None:
        """Show scanned notes count."""
        ui.console.print(f"\n[bold]Scanning {count} notes...[/bold]")

    def show_date_fix_result(self, fixed_count: int) -> None:
        """Show date fixing success count."""
        ui.console.print(f"\n[green]✓ Fixed dates in {fixed_count} notes.[/green]")

    def show_note_date_fixed(self, filename: str) -> None:
        """Show single note date fix success."""
        ui.console.print(f"[green]Fixed dates for {filename}[/green]")

    def show_note_fixed(self, filename: str) -> None:
        """Show single note fully fixed."""
        ui.console.print(f"[green]Fixed {filename}[/green]")

    def show_note_valid(self, filename: str) -> None:
        """Show single note validated successfully."""
        ui.console.print(f"[green]Note {filename} is now valid.[/green]")

    def show_note_warnings(self, filename: str, warnings: list[str]) -> None:
        """Show note warnings."""
        if warnings:
            ui.console.print(f"[yellow]⚠️  {filename}: {', '.join(warnings)}[/yellow]")

    def report_results(
        self,
        valid: int,
        warnings: int,
        version_outdated: int,
        invalid: int,
    ) -> None:
        """Print summary report."""
        ui.console.print(f"\n[green]✓[/green] {valid} notes healthy")

        if warnings > 0:
            ui.console.print(
                f"[yellow]⚠️[/yellow] {warnings} notes have warnings (e.g. unknown source)"
            )
        if version_outdated > 0:
            ui.console.print(
                f"[yellow]![/yellow] {version_outdated} notes have outdated versions (run 'dxva migrate')"
            )
        if invalid > 0:
            ui.console.print(f"[red]![/red] {invalid} notes need manual attention")
        elif warnings > 0:
            ui.console.print("\n[bold]Doctor finished (with warnings).[/bold]")
        else:
            ui.console.print("\n[bold]Doctor finished.[/bold]")

    def show_doctor_finished(self) -> None:
        """Show completion message."""
        ui.console.print("\n[bold]Doctor finished.[/bold]")

    def show_note_header(self, index: int, total: int, filename: str) -> None:
        """Show header for processing a specific note."""
        ui.console.print(f"\n[cyan]━━━ [{index}/{total}] {filename} ━━━[/cyan]")

    def prompt_rename(self, old_name: str, new_name: str) -> bool:
        """Prompt to rename file."""
        ui.console.print(f"[yellow]Filename mismatch:[/yellow] {old_name} → {new_name}")
        return ui.confirm("Rename file?", default=True)

    def show_renamed(self, new_name: str) -> None:
        """Show renamed confirmation."""
        ui.console.print(f"[green]Renamed → {new_name}[/green]")

    def print_issues(self, missing: list[str], invalid: list[str]) -> None:
        """Print missing and invalid fields."""
        if missing:
            ui.console.print(f"[yellow]Missing:[/yellow] {', '.join(missing)}")
        real = [x for x in invalid if x != "dates"]
        if real:
            ui.console.print(f"[red]Invalid:[/red] {', '.join(real)}")

    def show_skip_or_no_fixes(self) -> None:
        """Show skip message."""
        ui.console.print("[yellow]Skipped or no fixes provided.[/yellow]")

    def show_exiting(self) -> None:
        """Show exiting message."""
        ui.console.print("[red]Exiting...[/red]")

    def show_skipping_note(self) -> None:
        """Show skipping note message."""
        ui.console.print("[yellow]Skipping note...[/yellow]")

    def show_fix_failed(self) -> None:
        """Show fix failed message."""
        ui.console.print("[yellow]Note still has issues. Continuing...[/yellow]")

    def show_max_attempts_reached(self, filename: str, max_attempts: int) -> None:
        """Show max fix attempts reached."""
        ui.console.print(
            f"[red]Could not fully fix {filename} "
            f"after {max_attempts} attempts. Skipping.[/red]"
        )

    # -- Interactive Gathering ----------------------------------------------

    def gather_fixes(self, result: ValidationResult) -> dict[str, Any]:
        """Gather fixes via CLI input (debug mode)."""
        fixes: dict[str, Any] = {}

        self._handle_title_fix(result, fixes)
        self._handle_field_fixes(result, fixes)

        return fixes

    def _handle_title_fix(
        self,
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
            existing = result.frontmatter.get("title", "").strip('"')

            if "integrity_aliases" in result.invalid_fields:
                ui.console.print(
                    f"[yellow]Title '{existing}' is missing from aliases.[/yellow]"
                )
                options = [
                    "Add title to aliases",
                    "Keep current aliases",
                    "Replace aliases with title only",
                ]
                sel = self._gather_enum_selection("Integrity Aliases Action", options)
                if sel == "Add title to aliases":
                    fixes["integrity_aliases"] = "ADD"
                elif sel == "Replace aliases with title only":
                    fixes["integrity_aliases"] = "REPLACE"
                else:
                    fixes["integrity_aliases"] = "KEEP"
            elif existing:
                fixes["aliases"] = [existing]

    def _handle_field_fixes(
        self,
        result: ValidationResult,
        fixes: dict[str, Any],
    ) -> None:
        """Handle non-title field repairs in CLI mode."""
        extraneous = self._get_extraneous_fields(result.frontmatter)
        issues = (
            (set(result.missing_fields) | set(result.invalid_fields))
            - _SKIP_FIELDS
            - extraneous
        )

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

    def _gather_enum_selection(
        self,
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

    @staticmethod
    def _get_extraneous_fields(frontmatter: dict[str, Any]) -> set[str]:
        """Return field names present in frontmatter but forbidden by the model."""
        note_type = frontmatter.get("type")
        if not note_type or not isinstance(note_type, str):
            return set()
        model_cls = NoteModelRegistry.get_model(note_type)
        if not model_cls:
            return set()
        if getattr(model_cls, "model_config", {}).get("extra") != "forbid":
            return set()
        from dx_vault_atlas.shared.pydantic_utils import strip_unknown_fields

        clean = strip_unknown_fields(model_cls, frontmatter)
        return set(frontmatter.keys()) - set(clean.keys())
