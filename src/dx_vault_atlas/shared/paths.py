"""Internal package paths.

Templates remain in note_creator/templates/ as they are service-specific.
This module provides a reference to that location.
"""

from pathlib import Path

# Package root: src/dx_vault_atlas/shared/paths.py -> parent.parent = dx_vault_atlas
PACKAGE_ROOT = Path(__file__).resolve().parent.parent

# Templates location (inside note_creator service)
TEMPLATES_DIR = PACKAGE_ROOT / "services" / "note_creator" / "templates"

APP_NAME = "dx-vault-atlas"


def validate_directory(path_str: str | Path) -> Path:
    """Validate that a path exists and is a directory.

    Args:
        path_str: User-provided path string or Path object.

    Returns:
        Resolved Path if valid.

    Raises:
        ValueError: If path does not exist or is not a directory.
    """
    path = Path(path_str).expanduser().resolve()
    if not path.exists():
        raise ValueError(f"Path does not exist: {path}")
    if not path.is_dir():
        raise ValueError(f"Path is not a directory: {path}")
    return path


def ensure_templates_exist() -> None:
    """Verify templates directory exists.

    Raises:
        FileNotFoundError: If templates directory is missing.
    """
    if not TEMPLATES_DIR.exists():
        msg = f"Templates directory not found: {TEMPLATES_DIR}"
        raise FileNotFoundError(msg)
