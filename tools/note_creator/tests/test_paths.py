"""Tests for ProjectPaths."""
from pathlib import Path

from note_creator.utils.paths import ProjectPaths


def test_templates_dir_exists():
    """TEMPLATES path exists and points to src/templates."""
    assert ProjectPaths.TEMPLATES.exists(), "TEMPLATES directory should exist"
    assert "templates" in ProjectPaths.TEMPLATES.name
    assert "src" in str(ProjectPaths.TEMPLATES)


def test_templates_contains_info_md():
    """info.md template file exists under TEMPLATES."""
    info_md = ProjectPaths.TEMPLATES / "info.md"
    assert info_md.exists(), "info.md should exist in templates"
    assert info_md.suffix == ".md"


def test_ensure_dirs_creates_logs_and_templates():
    """ensure_dirs creates LOGS and TEMPLATES without error."""
    ProjectPaths.ensure_dirs()
    assert ProjectPaths.LOGS.exists()
    assert ProjectPaths.TEMPLATES.exists()
