from pathlib import Path
from note_creator.models.note import BaseNote
from note_creator.services.templating import TemplatingService
from note_creator.core.editor import TextEditor

class NoteProcessor:
    def __init__(self, templating_service: TemplatingService) -> None:
        self.templating = templating_service

    def create_note(self, template_name: str, note_data: BaseNote, output_path: Path) -> None:
        """Renderiza la nota y la abre en el editor."""
        # El note_data aquí ya viene validado como ProjectNote o TaskNote desde main.py
        content = self.templating.render(template_name, note_data)
        self._write_to_disk(content, output_path)
        TextEditor.open_file(str(output_path))

    def _write_to_disk(self, content: str, path: Path) -> None:
        if path.exists():
            raise FileExistsError(f"La nota ya existe en: {path}")
        path.write_text(content, encoding="utf-8")