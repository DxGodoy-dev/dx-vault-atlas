"""YAML frontmatter parser for markdown files."""

import re
from dataclasses import dataclass

import yaml

from dx_vault_atlas.shared.utils.title_normalizer import TitleNormalizer


class DoubleQuotedString(str):
    """A string subclass that PyYAML will represent with double quotes."""


def _double_quoted_presenter(
    dumper: yaml.Dumper, data: DoubleQuotedString
) -> yaml.ScalarNode:
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style='"')


yaml.SafeDumper.add_representer(DoubleQuotedString, _double_quoted_presenter)  # type: ignore[arg-type]
yaml.Dumper.add_representer(DoubleQuotedString, _double_quoted_presenter)  # type: ignore[arg-type]


class YamlParseError(Exception):
    """Raised when YAML frontmatter is malformed."""


@dataclass
class ParsedNote:
    """Result of parsing a markdown file.

    Attributes:
        frontmatter: Parsed YAML as dictionary with typed values.
        body: Content after the frontmatter.
        has_yaml: Whether the file had YAML frontmatter.
    """

    frontmatter: dict[str, str | int | list[str] | None]
    body: str
    has_yaml: bool


class YamlParserService:
    """Extracts YAML frontmatter and body from markdown files.

    Expects frontmatter delimited by --- at the start of the file.
    """

    FRONTMATTER_PATTERN = re.compile(
        r"^---\s*\n(.*?)\n---\s*\n?(.*)",
        re.DOTALL,
    )

    def parse(self, content: str) -> ParsedNote:
        """Parse markdown content into frontmatter and body.

        Args:
            content: Raw markdown file content.

        Returns:
            ParsedNote with frontmatter dict, body, and has_yaml flag.

        Raises:
            YamlParseError: If frontmatter exists but is malformed.
        """
        match = self.FRONTMATTER_PATTERN.match(content)

        # Guard: No frontmatter found
        if not match:
            return ParsedNote(
                frontmatter={},
                body=content,
                has_yaml=False,
            )

        yaml_content = match.group(1)
        body = match.group(2)

        try:
            raw_frontmatter = yaml.safe_load(yaml_content)
            # Handle empty YAML block
            if raw_frontmatter is None:
                raw_frontmatter = {}
        except yaml.YAMLError as e:
            msg = f"Invalid YAML frontmatter: {e}"
            raise YamlParseError(msg) from e

        # Ensure we return a dict
        frontmatter: dict[str, str | int | list[str] | None] = (
            raw_frontmatter if isinstance(raw_frontmatter, dict) else {}
        )

        return ParsedNote(
            frontmatter=frontmatter,
            body=body,
            has_yaml=True,
        )

    def serialize_frontmatter(
        self, frontmatter: dict[str, str | int | list[str] | None]
    ) -> str:
        """Convert frontmatter dict back to YAML string.

        Args:
            frontmatter: Dictionary to serialize.

        Returns:
            YAML string with --- delimiters.
        """
        # Create a shallow copy to avoid mutating the original dict in memory
        serialization_dict = frontmatter.copy()

        # Apply strict normalization and double quoting to the title field
        raw_title = serialization_dict.get("title")
        if raw_title is not None and isinstance(raw_title, str):
            normalized_title = TitleNormalizer.normalize_frontmatter_title(raw_title)
            serialization_dict["title"] = DoubleQuotedString(normalized_title)

        yaml_content = yaml.dump(
            serialization_dict,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )
        return f"---\n{yaml_content}---\n"
