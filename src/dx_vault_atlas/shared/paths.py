"""Internal package paths.

Templates remain in note_creator/templates/ as they are service-specific.
This module provides a reference to that location.
"""

from pathlib import Path

# Package root: src/dx_vault_atlas/shared/paths.py -> parent.parent = dx_vault_atlas
PACKAGE_ROOT = Path(__file__).resolve().parent.parent

# Templates location (inside note_creator service)
TEMPLATES_DIR = PACKAGE_ROOT / "services" / "note_creator" / "templates"


def ensure_templates_exist() -> None:
    """Verify templates directory exists.

    Raises:
        FileNotFoundError: If templates directory is missing.
    """
    if not TEMPLATES_DIR.exists():
        msg = f"Templates directory not found: {TEMPLATES_DIR}"
        raise FileNotFoundError(msg)
