"""Template rendering service using Jinja2."""

from datetime import datetime

from jinja2 import Environment, FileSystemLoader, TemplateNotFound, select_autoescape

from dx_vault_atlas.services.note_creator.models.note import BaseNote
from dx_vault_atlas.shared.paths import TEMPLATES_DIR


class TemplatingService:
    """Service for rendering note templates with Jinja2."""

    def __init__(self) -> None:
        """Initialize Jinja2 environment with templates directory."""
        self.env = Environment(
            loader=FileSystemLoader(str(TEMPLATES_DIR)),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        # self.env.filters["format_date"] = self._format_date_filter

    def _format_date_filter(self, value: str, fmt: str = "%Y-%m-%d") -> str:
        """Convert Pydantic ISO string to formatted date.

        Args:
            value: ISO date string from Pydantic.
            fmt: Output date format.

        Returns:
            Formatted date string.
        """
        if not value:
            return ""
        try:
            dt = datetime.fromisoformat(value)
            return dt.strftime(fmt)
        except (ValueError, TypeError):
            return value

    def render(self, template_name: str, note_data: BaseNote) -> str:
        """Render a template with note data.

        Args:
            template_name: Template file name.
            note_data: Validated note data.

        Returns:
            Rendered template content.

        Raises:
            FileNotFoundError: If template doesn't exist.
        """
        try:
            template = self.env.get_template(template_name)
            data = note_data.model_dump(mode="json", by_alias=True)
            return template.render(**data)
        except TemplateNotFound as e:
            msg = f"Template '{template_name}' not found in {TEMPLATES_DIR}"
            raise FileNotFoundError(msg) from e
