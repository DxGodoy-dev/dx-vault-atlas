import sys
from pathlib import Path
from typing import Callable, Any, Final

from note_creator.core.logger import logger
from note_creator.models.enums import NoteSource, Priority, NoteTemplate, NoteArea
from note_creator.models.note import (
    BaseNote,
    MocNote,
    RankedNote,
    TaskNote,
    ProjectNote,
)
from note_creator.services.console import ConsoleInterface

# Mapeo de modelos para instanciación final
MODEL_MAP = {
    NoteTemplate.PROJECT: ProjectNote,
    NoteTemplate.TASK: TaskNote,
    NoteTemplate.INFO: RankedNote,
    NoteTemplate.MOC: MocNote,
}

DEFAULT_TAGS: Final[list[str]] = []

class NoteBuilderService:
    """Servicio para la construcción interactiva de notas."""

    @staticmethod
    def _get_base_info(title: str, template: NoteTemplate) -> dict[str, Any]:
        return {
            "title": f'"{title}"',
            "aliases": [title],
            "tags": DEFAULT_TAGS,
            "type": Path(template.value).stem,
        }

    @staticmethod
    def _get_workflow_info() -> dict[str, Any]:
        return {
            "source": ConsoleInterface.choose_enum("Source", NoteSource),
            "priority": ConsoleInterface.choose_enum("Priority", Priority),
        }

    @staticmethod
    def _get_context_info() -> dict[str, Any]:
        return {"area": ConsoleInterface.choose_enum("Area (Work/Personal)", NoteArea)}

    # Mapa de pasos según el requerimiento:
    # MOC: Nada | INFO: Workflow | TASK/PROJECT: Workflow + Context
    _STEPS_MAP: dict[NoteTemplate, list[Callable[[], dict[str, Any]]]] = {
        NoteTemplate.MOC: [],
        NoteTemplate.INFO: [_get_workflow_info],
        NoteTemplate.TASK: [_get_workflow_info, _get_context_info],
        NoteTemplate.PROJECT: [_get_workflow_info, _get_context_info],
    }

    @classmethod
    def run_wizard(cls, raw_title: str) -> BaseNote:
        """
        Punto de entrada principal. 
        Pide el template y construye la nota completa.
        """
        # 1. Pedir el template primero (como solicitaste)
        template = ConsoleInterface.choose_enum("Template", NoteTemplate, default_index=0)
        
        # 2. Iniciar composición de datos
        note_data = cls._get_base_info(raw_title, template)
        
        # 3. Ejecutar pasos dinámicos
        steps = cls._STEPS_MAP.get(template, [])
        for step_func in steps:
            note_data.update(step_func())

        # 4. Retornar instancia validada
        note_class = MODEL_MAP.get(template, BaseNote)
        return note_class(**note_data)