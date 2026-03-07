"""Template rendering service using Jinja2."""

from datetime import datetime

from jinja2 import Environment, FileSystemLoader, TemplateNotFound, select_autoescape

from dx_vault_atlas.shared.models.note import BaseNote
from dx_vault_atlas.shared.paths import TEMPLATES_DIR


class TemplatingService:
    """Service for rendering note templates with Jinja2."""

    def __init__(self) -> None:
        """Initialize Jinja2 environment with templates directory."""
        from dx_vault_atlas.shared.yaml_parser import YamlParserService

        self.env = Environment(
            loader=FileSystemLoader(str(TEMPLATES_DIR)),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.yaml_parser = YamlParserService()

    def render(self, template_name: str, note_data: BaseNote) -> str:
        """Render a template with note data.

        Args:
            template_name: Template file name.
            note_data: Validated note data.

        Returns:
            Rendered template content including YAML frontmatter.

        Raises:
            FileNotFoundError: If template doesn't exist.
        """
        # Serialize YAML frontmatter using parser service
        # Pydantic's model_dump easily provides a dictionary for PyYAML
        data_dict = note_data.model_dump(mode="json", by_alias=True, exclude_none=True)

        # Ensure default link formats for Obsidian (from old templates)
        if "up" not in data_dict:
            data_dict["up"] = "[[ ]]"

        yaml_block = self.yaml_parser.serialize_frontmatter(data_dict)

        # Render Jinja body
        try:
            template = self.env.get_template(template_name)
            body = template.render(**data_dict)
            return f"{yaml_block}\n{body}"
        except TemplateNotFound as e:
            msg = f"Template '{template_name}' not found in {TEMPLATES_DIR}"
            raise FileNotFoundError(msg) from e
