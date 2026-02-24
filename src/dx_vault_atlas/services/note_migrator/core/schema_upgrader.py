"""Schema upgrader service."""

from packaging.version import parse as parse_version

from dx_vault_atlas.services.note_creator.defaults import SCHEMA_VERSION
from dx_vault_atlas.services.note_migrator.validator import MODEL_MAP
from dx_vault_atlas.shared.logger import logger


class SchemaUpgrader:
    """Service to upgrade note schema to current version."""

    def upgrade(self, frontmatter: dict) -> dict:
        """Upgrade frontmatter to current schema version and clean fields.

        Args:
            frontmatter: Original frontmatter dictionary.

        Returns:
            Updated and cleaned frontmatter dictionary.
        """
        # 1. Check and update version
        current_version_str = str(frontmatter.get("version") or "")
        current_version = (
            parse_version(current_version_str) if current_version_str else None
        )
        target_version = parse_version(SCHEMA_VERSION)

        should_update = not current_version or current_version < target_version

        if should_update:
            frontmatter["version"] = SCHEMA_VERSION
            logger.info(f"Upgraded schema version to {SCHEMA_VERSION}")

        # 2. Clean fields based on model
        note_type = frontmatter.get("type")
        if (
            note_type
            and isinstance(note_type, str)
            and (model_cls := MODEL_MAP.get(note_type))
        ):
            # Only keep fields that are part of the model + 'type'
            # We DONT use Pydantic validation/dump because it might coerce types
            # or fail on 'invalid' data that we want to preserve for Doctor to fix.
            allowed_fields = set(model_cls.model_fields.keys())
            # Add aliases if any
            for field in model_cls.model_fields.values():
                if field.alias:
                    allowed_fields.add(field.alias)

            allowed_fields.add("type")

            cleaned_data = {k: v for k, v in frontmatter.items() if k in allowed_fields}
            return cleaned_data

        return frontmatter
