from dx_vault_atlas.shared.logger import logger


class TypeHeuristics:
    """Detects NoteType from strict 'type' field in YAML.

    Previously used model introspection, now simplified to only accept explicit type.
    """

    @classmethod
    def detect_type(cls, frontmatter: dict[str, object]) -> str | None:
        """Extracts the note type from frontmatter 'type' field.

        Args:
            frontmatter: The parsed YAML frontmatter dictionary.

        Returns:
            The detected type string if explicitly defined, else None.
        """
        # Guard: Check if type is explicitly defined
        existing_type = frontmatter.get("type")
        if existing_type and isinstance(existing_type, str):
            logger.debug(f"Type explicitly defined in frontmatter: {existing_type}")
            return existing_type

        logger.debug("No 'type' field found in frontmatter.")
        return None
