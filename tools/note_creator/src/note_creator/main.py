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
from note_creator.models.note import (
    BaseNote,
    TaskNote,
    ProjectNote,
)
from note_creator.models.enums import NoteSource, Priority, NoteTemplate, NoteArea
from note_creator.utils.title_normalizer import TitleNormalizer
from note_creator.utils.paths import ProjectPaths

_E = TypeVar("_E", bound=Enum)

# Directiva Maestra: Uso de Final para constantes
DEFAULT_TAGS: Final[list[str]] = []

def _choose_enum(label: str, enum_cls: type[_E], default_index: int = 0) -> _E:
    """Shows a numbered menu for the enum and returns the selected member."""
    members = list(enum_cls)
    for i, m in enumerate(members):
        display = m.value if isinstance(m.value, str) else f"{m.name} ({m.value})"
        print(f"  {i + 1}. {display}")
    
    prompt = f"\n{label} [1-{len(members)}] (default {default_index + 1}): "
    raw = input(prompt).strip() or str(default_index + 1)
    
    try:
        idx = int(raw)
        if 1 <= idx <= len(members):
            return members[idx - 1]
    except ValueError:
        pass
    return members[default_index]

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
    source: NoteSource = _choose_enum("Source", NoteSource, default_index=0)
    priority: Priority = _choose_enum("Priority", Priority, default_index=1)
    template: NoteTemplate = _choose_enum("Template", NoteTemplate, default_index=0)

    model_map: dict[NoteTemplate, type[BaseNote]] = {
        NoteTemplate.PROJECT: ProjectNote,
        NoteTemplate.TASK: TaskNote,
        NoteTemplate.INFO: BaseNote,
        NoteTemplate.MOC: BaseNote,
    }
    
    NoteClass = model_map.get(template, BaseNote)
    
    # Inicializamos kwargs para la instancia
    note_kwargs = {
        "title": raw_title,
        "aliases": f"[{raw_title}]",
        "source": source,
        "priority": priority,
        "tags": DEFAULT_TAGS,
        "type": Path(template.value).stem,
    }

    # LÓGICA DINÁMICA: ¿La clase requiere 'area'?
    # Inspeccionamos los campos del modelo de Pydantic
    if "area" in NoteClass.model_fields:
        area = _choose_enum("Area (Work/Personal)", NoteArea, default_index=0)
        note_kwargs["area"] = area

    note_data = NoteClass(**note_kwargs)
    output_path = ProjectPaths.NOTES / f"{safe_title}.md"

    # Los servicios lanzan excepciones, main las captura
    template_service = TemplatingService()
    processor = NoteProcessor(template_service)

    logger.info(f"Processing note: {safe_title}")
    processor.create_note(template.value, note_data, output_path)
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