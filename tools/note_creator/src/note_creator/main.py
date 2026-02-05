import sys
from datetime import datetime
from enum import Enum
from typing import TypeVar, Final
from pathlib import Path

# Nota: Eliminamos el prefijo src. porque src es la raíz del paquete instalable
from note_creator.core.logger import logger
from note_creator.core.processor import NoteProcessor
from note_creator.services.templating import TemplatingService
from note_creator.services.console import ConsoleInterface
from note_creator.services.note_creator import NoteBuilderService
from note_creator.models.note import (
    BaseNote,
    MocNote,
    RankedNote,
    TaskNote,
    ProjectNote,
)
from note_creator.models.enums import NoteSource, Priority, NoteTemplate, NoteArea
from note_creator.utils.title_normalizer import TitleNormalizer
from note_creator.utils.paths import ProjectPaths

def run_automation() -> None:
    """Main execution logic with Guard Clauses and Pydantic validation."""
    logger.info("Starting Obsidian Automation Suite")
    
    # Aseguramos directorios antes de iniciar
    ProjectPaths.ensure_dirs()

    raw_title = ConsoleInterface.query("Enter the note title: ").strip()

    # Guard Clause: Validación temprana
    if not raw_title:
        logger.warning("Operation cancelled: title cannot be empty.")
        return

    safe_title = TitleNormalizer.normalize(raw_title)

    print("\n--- Note Configuration ---")
    note_instance = NoteBuilderService.run_wizard(raw_title)
    
    output_path = ProjectPaths.NOTES / f"{safe_title}.md"

    # Los servicios lanzan excepciones, main las captura
    template_service = TemplatingService()
    processor = NoteProcessor(template_service)

    logger.info(f"Processing note: {safe_title}")
    processor.create_note(
        template_name=f"{note_instance.note_type}.md", 
        note_data=note_instance, 
        output_path=output_path
    )
    logger.info(f"Success: Note created at {output_path}")

def main() -> None:
    """Entry point for the console script defined in pyproject.toml."""
    try:
        run_automation()
    except KeyboardInterrupt:
        logger.warning("Process interrupted by user (Ctrl+C).")
        sys.exit(0)
    except Exception:
        # Directiva Maestra: Captura y logueo centralizado con traceback al archivo
        logger.exception("FATAL ERROR: Unhandled application error")
        sys.exit(1)

if __name__ == "__main__":
    main()