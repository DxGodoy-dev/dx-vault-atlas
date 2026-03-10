import logging
import sys
from pathlib import Path

import pytest

# Ensure src is in pythonpath
sys.path.append(str(Path(__file__).parent.parent / "src"))

from dx_vault_atlas.services.note_migrator.core.heuristics import TypeHeuristics
from dx_vault_atlas.services.note_migrator.core.migrator import NoteMigrator
from dx_vault_atlas.services.note_migrator.core.schema_upgrader import SchemaUpgrader
from dx_vault_atlas.services.note_migrator.core.transformation_service import (
    TransformationService,
)
from dx_vault_atlas.shared.core.io import (
    LocalFileRepository,
)
from dx_vault_atlas.shared.yaml_parser import YamlParserService
from dx_vault_atlas.shared.config import GlobalConfig

# Import note models to populate the NoteModelRegistry
import dx_vault_atlas.shared.models.note  # noqa: F401

logger = logging.getLogger(__name__)

SCENARIOS_DIR = Path(__file__).parent / "migration_scenarios"

MOCK_INPUTS = {
    "02_missing_type_explicit.md": {"type": "info", "source": "Other", "priority": "1"},
    "05_extra_fields.md": {
        "source": "Other",
        "priority": 1,
        "area": "Personal",
        "status": "active",
    },
    "06_missing_required.md": {"area": "Personal"},
    "08_empty_file.md": {
        "title": "Empty Note",
        "type": "info",
        "priority": 1,
        "status": "active",
        "source": "Other",
        "aliases": [],
    },
}


class MockEditorBuffer:
    def __init__(self, scenario_name: str, editor: str = "vim") -> None:
        self.scenario_name = scenario_name

    def prompt_user(
        self, original_content: str, frontmatter: dict, missing_fields: list[str]
    ) -> dict:
        # Validation for 08_empty_file explicit requirement (Title before Type)
        if self.scenario_name == "08_empty_file.md":
            if "title" in missing_fields and "type" in missing_fields:
                if missing_fields.index("title") > missing_fields.index("type"):
                    raise AssertionError(
                        "FAIL: 'title' should be asked before 'type' for empty files."
                    )

        if self.scenario_name in MOCK_INPUTS:
            updates = MOCK_INPUTS[self.scenario_name]
            return {**frontmatter, **updates}

        return frontmatter


def get_scenarios() -> list[Path]:
    return sorted(list(SCENARIOS_DIR.glob("*.md")))


@pytest.fixture
def migrator_setup(tmp_path: Path):
    vault_p = tmp_path / "vault"
    vault_inbox_p = vault_p / "Inbox"
    vault_inbox_p.mkdir(parents=True, exist_ok=True)
    mock_settings = GlobalConfig(vault_path=vault_p, vault_inbox=vault_inbox_p)

    yaml_parser = YamlParserService()
    heuristics = TypeHeuristics()
    schema_upgrader = SchemaUpgrader()
    transformer = TransformationService(mock_settings)
    file_repo = LocalFileRepository()

    def _create_migrator(scenario_name: str) -> NoteMigrator:
        editor_service = MockEditorBuffer(scenario_name)
        return NoteMigrator(
            yaml_parser=yaml_parser,
            editor_service=editor_service,
            heuristics=heuristics,
            schema_upgrader=schema_upgrader,
            transformation_service=transformer,
            file_repository=file_repo,
        )

    return _create_migrator


@pytest.mark.parametrize("scenario_path", get_scenarios(), ids=lambda p: p.stem)
def test_migration_scenario(
    scenario_path: Path, migrator_setup, tmp_path: Path
) -> None:
    scenario_name = scenario_path.name
    temp_file = tmp_path / f"temp_{scenario_name}"
    temp_file.write_text(scenario_path.read_text(encoding="utf-8"), encoding="utf-8")

    migrator = migrator_setup(scenario_name)

    if "07_malformed" in scenario_name:
        with pytest.raises(Exception) as exc:
            migrator.migrate(temp_file)
        assert "FrontmatterParseError" in type(exc.value).__name__
        return

    migrator.migrate(temp_file)
    final_content = temp_file.read_text(encoding="utf-8")

    if "01_perfect_note" in scenario_name:
        assert "version: 1.0.0" in final_content
    elif "02_missing_type" in scenario_name:
        assert "type: info" in final_content
    elif "03_missing_dates" in scenario_name:
        assert "created" in final_content
        assert "updated" in final_content
    elif "04_old_version" in scenario_name:
        assert "version: 1.0" in final_content or "version: '1.0'" in final_content
    elif "05_extra_fields" in scenario_name:
        assert "extra_field" not in final_content
    elif "06_missing_required" in scenario_name:
        assert "area: Personal" in final_content
    elif "08_empty_file" in scenario_name:
        assert 'title: "Empty Note"' in final_content
    elif "09_date_string" in scenario_name:
        assert "October 27, 2023" in final_content
    elif "10_conflict" in scenario_name:
        assert "<<< HEAD" in final_content
