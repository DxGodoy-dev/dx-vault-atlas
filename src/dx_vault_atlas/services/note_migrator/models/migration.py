"""Data models for migration results and session tracking."""

from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, Field


class MigrationStatus(StrEnum):
    """Status of a single note migration."""

    SUCCESS = "success"
    SKIPPED = "skipped"
    FAILED = "failed"


class MigrationResult(BaseModel):
    """Result DTO for a single note migration.

    Attributes:
        file_path: Path to the note file.
        status: Final migration status.
        detected_type: Note type detected by heuristics or user input.
        error_message: Error details if status is FAILED.
    """

    file_path: Path
    status: MigrationStatus
    detected_type: str | None = None
    error_message: str | None = None


class MigrationSession(BaseModel):
    """Tracks overall migration progress across all notes.

    Attributes:
        results: List of individual migration results.
    """

    results: list[MigrationResult] = Field(default_factory=list)

    @property
    def successful(self) -> list[MigrationResult]:
        """Return all successful migrations."""
        return [r for r in self.results if r.status == MigrationStatus.SUCCESS]

    @property
    def skipped(self) -> list[MigrationResult]:
        """Return all skipped migrations."""
        return [r for r in self.results if r.status == MigrationStatus.SKIPPED]

    @property
    def failed(self) -> list[MigrationResult]:
        """Return all failed migrations."""
        return [r for r in self.results if r.status == MigrationStatus.FAILED]

    @property
    def summary(self) -> str:
        """Generate human-readable summary of migration results."""
        s, k, f = 0, 0, 0
        for r in self.results:
            if r.status == MigrationStatus.SUCCESS:
                s += 1
            elif r.status == MigrationStatus.SKIPPED:
                k += 1
            elif r.status == MigrationStatus.FAILED:
                f += 1
        return f"✓ {s} success | ⊘ {k} skipped | ✗ {f} failed"

    def update_result(self, file_path: Path, new_result: MigrationResult) -> None:
        """Update an existing result by file path (for retry flow)."""
        for i, result in enumerate(self.results):
            if result.file_path == file_path:
                self.results[i] = new_result
                return
        self.results.append(new_result)
