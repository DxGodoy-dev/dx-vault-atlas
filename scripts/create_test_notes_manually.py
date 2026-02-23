import sys
from pathlib import Path
from datetime import datetime

# Adjust path to import src
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT / "src"))

from dx_vault_atlas.services.note_creator.core.processor import NoteProcessor
from dx_vault_atlas.services.note_creator.services.templating import TemplatingService
from dx_vault_atlas.services.note_creator.models.note import (
    MocNote,
    InfoNote,
    TaskNote,
    ProjectNote,
)
from dx_vault_atlas.services.note_creator.models.enums import (
    NoteSource,
    Priority,
    NoteArea,
    NoteStatus,
)


def create_notes():
    templating = TemplatingService()
    processor = NoteProcessor(templating)

    inbox = PROJECT_ROOT / "dx_vault" / "dx_vault" / "dx_vault" / "00_Inbox"
    inbox.mkdir(parents=True, exist_ok=True)

    print(f"Creating notes in {inbox}...")

    # 1. MOC
    moc_data = MocNote(
        title='"Test MOC Note"',
        aliases=["Test MOC Note"],
        type="moc",
        tags=[],
    )
    processor.create_note("moc.md", moc_data, inbox / "Test MOC Note.md")
    print("Created Test MOC Note.md")

    # 2. INFO
    info_data = InfoNote(
        title='"Test INFO Note"',
        aliases=["Test INFO Note"],
        type="info",
        source=NoteSource.ME,
        priority=Priority.MEDIUM,
        tags=[],
    )
    processor.create_note("info.md", info_data, inbox / "Test INFO Note.md")
    print("Created Test INFO Note.md")

    # 3. TASK
    task_data = TaskNote(
        title='"Test TASK Note"',
        aliases=["Test TASK Note"],
        type="task",
        source=NoteSource.ME,
        priority=Priority.HIGH,
        area=NoteArea.WORK,
        status=NoteStatus.TO_DO,
        tags=[],
    )
    processor.create_note("task.md", task_data, inbox / "Test TASK Note.md")
    print("Created Test TASK Note.md")

    # 4. PROJECT
    project_data = ProjectNote(
        title='"Test PROJECT Note"',
        aliases=["Test PROJECT Note"],
        type="project",
        source=NoteSource.RESEARCH,
        priority=Priority.CRITICAL,
        area=NoteArea.PERSONAL,
        status=NoteStatus.IN_PROGRESS,  # Project usually created as To Do but let's vary
        tags=[],
    )
    processor.create_note("project.md", project_data, inbox / "Test PROJECT Note.md")
    print("Created Test PROJECT Note.md")


if __name__ == "__main__":
    create_notes()
