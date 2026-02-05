from jinja2 import Environment, FileSystemLoader, select_autoescape, TemplateNotFound
from note_creator.models.note import BaseNote
from note_creator.utils.paths import ProjectPaths
from datetime import datetime

class TemplatingService:
    def __init__(self) -> None:
        self.env = Environment(
            loader=FileSystemLoader(str(ProjectPaths.TEMPLATES)),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True
        )
        self.env.filters["format_date"] = self._format_date_filter

    def _format_date_filter(self, value: str, fmt: str = "%Y-%m-%d") -> str:
        """Convierte un string ISO de Pydantic de vuelta a objeto fecha y lo formatea."""
        if not value:
            return ""
        try:
            # Pydantic mode="json" entrega ISO strings
            dt = datetime.fromisoformat(value)
            return dt.strftime(fmt)
        except (ValueError, TypeError):
            return value

    def render(self, template_name: str, note_data: BaseNote) -> str:
        """Renders a template using Pydantic's JSON-compatible dict."""
        try:
            template = self.env.get_template(template_name)
            
            # Directiva Maestra: mode="json" serializa Enums y Datetimes automáticamente
            data = note_data.model_dump(mode="json", by_alias=True)
            
            return template.render(**data)
        except TemplateNotFound:
            raise FileNotFoundError(
                f"La plantilla '{template_name}' no existe en {ProjectPaths.TEMPLATES}."
            )