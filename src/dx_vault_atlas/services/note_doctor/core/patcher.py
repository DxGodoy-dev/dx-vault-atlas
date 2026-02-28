"""Frontmatter patching service."""

from typing import Any

from dx_vault_atlas.shared.logger import logger


class FrontmatterPatcher:
    """Applies fixes to note frontmatter."""

    # Canonical field order
    ORDERED_FIELDS = [
        "version",
        "type",
        "title",
        "created",
        "updated",
        "aliases",
        "tags",
        # Type specific (Ranked, Workflow, Project, Task, MOC)
        "source",
        "priority",
        "status",
        "area",
        "outcome",
        "start_date",
        "end_date",
        "deadline",
        "level",
        "up",
    ]

    @classmethod
    def apply_fixes(
        cls, frontmatter: dict[str, Any], fixes: dict[str, Any]
    ) -> dict[str, Any]:
        """Apply a dictionary of fixes to the frontmatter.

        Args:
            frontmatter: Original frontmatter dictionary (will be modified).
            fixes: Dictionary of fixes from the wizard/TUI.

        Returns:
            Modified frontmatter dictionary with canonical ordering.
        """
        logger.debug(
            f"[DEBUG TRACE] patcher.apply_fixes Start | fixes={fixes} | 'source' in fm: {'source' in frontmatter}"
        )

        # Iterate over fixes and apply
        for key, value in fixes.items():
            # Map wizard keys to frontmatter keys
            target_key = key
            if key == "template":
                target_key = "type"

            if target_key == "title":
                # Special handling for title
                frontmatter["title"] = value
                # Ensure alias exists
                current_aliases = frontmatter.get("aliases", [])

                # If aliases is not a list (e.g. None or malformed), make it one
                if not isinstance(current_aliases, list):
                    current_aliases = []

                if value not in current_aliases:
                    current_aliases.append(value)

                frontmatter["aliases"] = current_aliases

            elif target_key in ["aliases", "tags"]:
                # Ensure these are lists
                if isinstance(value, str):
                    # concise splitting
                    items = [x.strip() for x in value.split(",") if x.strip()]
                    frontmatter[target_key] = items
                elif isinstance(value, list):
                    frontmatter[target_key] = value
                else:
                    # fallback
                    frontmatter[target_key] = [str(value)]

            else:
                # Handle Enum values (Wizard returns Enum members)
                if hasattr(value, "value"):
                    frontmatter[target_key] = value.value
                else:
                    frontmatter[target_key] = value

        # Reorder fields based on canonical order
        ordered_frontmatter = {}

        # 1. Add known fields in order if they exist
        for field in cls.ORDERED_FIELDS:
            if field in frontmatter:
                ordered_frontmatter[field] = frontmatter[field]

        # 2. Add remaining fields (custom or unknown)
        for key, value in frontmatter.items():
            if key not in ordered_frontmatter:
                ordered_frontmatter[key] = value

        logger.debug(
            f"[DEBUG TRACE] patcher.apply_fixes End | 'source' in ordered_fm: {'source' in ordered_frontmatter}"
        )
        return ordered_frontmatter
