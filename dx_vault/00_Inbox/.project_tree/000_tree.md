---
created: null
updated: null
type: note
tags: []
source: me
version: '1.0'
---
# Project MOC Tree

\\n.
├── [[.env.example]]
├── [[.gitignore]]
├── [[.gitmodules]]
├── [[LICENSE]]
├── [[README.md]]
├── [[Test Auto Fix.md]]
├── [[debug_date.py]]
├── [[integration_test.py]]
├── [[output.txt]]
├── [[pyproject.toml]]
├── [[repro_bug.py]]
├── [[repro_bug2.py]]
├── scripts/
│   ├── [[create_test_notes_manually.py]]
│   ├── [[fix_test_notes.py]]
│   ├── [[reproduce_cli_flow.py]]
│   ├── [[reproduce_ref_info.py]]
│   ├── [[reproduce_version_issue.py]]
│   ├── [[verify_debug.py]]
│   ├── [[verify_doctor_autofill.py]]
│   └── [[verify_doctor_debug.py]]
├── src/
│   ├── dx_vault_atlas/
│   │   ├── [[__init__.py]]
│   │   ├── [[cli.py]]
│   │   ├── services/
│   │   │   ├── [[__init__.py]]
│   │   │   ├── note_creator/
│   │   │   │   ├── [[__init__.py]]
│   │   │   │   ├── [[app.py]]
│   │   │   │   ├── core/
│   │   │   │   │   ├── [[__init__.py]]
│   │   │   │   │   ├── [[factory.py]]
│   │   │   │   │   ├── [[processor.py]]
│   │   │   │   │   └── [[writer.py]]
│   │   │   │   ├── [[defaults.py]]
│   │   │   │   ├── models/
│   │   │   │   │   ├── [[__init__.py]]
│   │   │   │   │   ├── [[enums.py]]
│   │   │   │   │   └── [[note.py]]
│   │   │   │   ├── services/
│   │   │   │   │   ├── [[__init__.py]]
│   │   │   │   │   ├── [[console.py]]
│   │   │   │   │   └── [[templating.py]]
│   │   │   │   ├── templates/
│   │   │   │   │   ├── [[__init__.py]]
│   │   │   │   │   ├── [[info.md]]
│   │   │   │   │   ├── [[moc.md]]
│   │   │   │   │   ├── [[project.md]]
│   │   │   │   │   ├── [[ref.md]]
│   │   │   │   │   └── [[task.md]]
│   │   │   │   ├── tui/
│   │   │   │   │   └── [[wizard_steps.py]]
│   │   │   │   ├── [[tui.py]]
│   │   │   │   ├── [[tui_steps.py]]
│   │   │   │   └── utils/
│   │   │   │       ├── [[__init__.py]]
│   │   │   │       └── [[title_normalizer.py]]
│   │   │   ├── note_doctor/
│   │   │   │   ├── [[__init__.py]]
│   │   │   │   ├── [[app.py]]
│   │   │   │   ├── core/
│   │   │   │   │   ├── [[__init__.py]]
│   │   │   │   │   ├── [[date_resolver.py]]
│   │   │   │   │   ├── [[fixer.py]]
│   │   │   │   │   └── [[patcher.py]]
│   │   │   │   ├── [[main.py]]
│   │   │   │   ├── models/
│   │   │   │   ├── [[tui.py]]
│   │   │   │   └── [[validator.py]]
│   │   │   └── note_migrator/
│   │   │       ├── [[__init__.py]]
│   │   │       ├── [[app.py]]
│   │   │       ├── core/
│   │   │       │   ├── [[__init__.py]]
│   │   │       │   ├── [[errors.py]]
│   │   │       │   ├── [[heuristics.py]]
│   │   │       │   ├── [[migrator.py]]
│   │   │       │   ├── [[schema_upgrader.py]]
│   │   │       │   └── [[transformation_service.py]]
│   │   │       ├── [[main.py]]
│   │   │       ├── models/
│   │   │       │   ├── [[__init__.py]]
│   │   │       │   ├── [[frontmatter.py]]
│   │   │       │   └── [[migration.py]]
│   │   │       ├── services/
│   │   │       │   ├── [[__init__.py]]
│   │   │       │   ├── [[editor_buffer.py]]
│   │   │       │   └── [[yaml_parser.py]]
│   │   │       └── [[validator.py]]
│   │   └── shared/
│   │       ├── [[__init__.py]]
│   │       ├── [[config.py]]
│   │       ├── [[console.py]]
│   │       ├── core/
│   │       │   ├── [[bootstrap.py]]
│   │       │   ├── [[scanner.py]]
│   │       │   └── [[system_editor.py]]
│   │       ├── [[logger.py]]
│   │       ├── [[paths.py]]
│   │       ├── [[pydantic_utils.py]]
│   │       ├── tui/
│   │       │   ├── [[__init__.py]]
│   │       │   ├── [[app.py]]
│   │       │   ├── [[config_editor.py]]
│   │       │   ├── [[config_wizard.py]]
│   │       │   ├── [[result_app.py]]
│   │       │   ├── [[theme.py]]
│   │       │   ├── [[widgets.py]]
│   │       │   ├── [[wizard.py]]
│   │       │   └── [[wizard_app.py]]
│   │       └── [[ui.py]]
│   └── [[test_strip.py]]
├── test_vault/
│   ├── [[000_Home.md]]
│   └── 00_Inbox/
│       └── [[20260218024306_mejores_practicas_para_agentes_en_google_antigravity.md]]
├── tests/
│   ├── [[__init__.py]]
│   ├── [[check_full_doctor.py]]
│   ├── [[check_old.py]]
│   ├── [[check_old2.py]]
│   ├── [[check_patcher_source.py]]
│   ├── [[check_refnote.py]]
│   ├── [[check_trace.py]]
│   ├── [[conftest.py]]
│   ├── doctor_scenarios/
│   │   ├── [[01_valid_note.md]]
│   │   ├── [[02_missing_dates_filename_20250101120000.md]]
│   │   ├── [[03_missing_dates_no_filename.md]]
│   │   ├── [[04_future_creation_date.md]]
│   │   ├── [[05_bad_status_casing.md]]
│   │   ├── [[06_bad_status_default.md]]
│   │   ├── [[07_priority_string.md]]
│   │   ├── [[08_priority_int_valid.md]]
│   │   ├── [[09_missing_required_no_default.md]]
│   │   ├── [[10_missing_optional_has_default.md]]
│   │   ├── [[11_list_status.md]]
│   │   ├── [[12_null_tags.md]]
│   │   ├── [[13_alias_consistency_ok.md]]
│   │   ├── [[14_alias_consistency_fail.md]]
│   │   ├── [[15_string_alias.md]]
│   │   ├── [[16_updated_before_created_20250102120000.md]]
│   │   ├── [[17_extra_fields.md]]
│   │   ├── [[18_unknown_enum_source.md]]
│   │   ├── [[19_malformed_frontmatter.md]]
│   │   └── [[20_complex_mixed.md]]
│   ├── migration_scenarios/
│   │   ├── [[01_perfect_note.md]]
│   │   ├── [[02_missing_type_explicit.md]]
│   │   ├── [[03_missing_dates.md]]
│   │   ├── [[04_old_version.md]]
│   │   ├── [[05_extra_fields.md]]
│   │   ├── [[06_missing_required.md]]
│   │   ├── [[07_malformed_frontmatter.md]]
│   │   ├── [[08_empty_file.md]]
│   │   ├── [[09_date_string_format.md]]
│   │   └── [[10_conflict_content.md]]
│   ├── [[repro_source_bug.py]]
│   ├── [[reproduce_doctor.py]]
│   ├── [[reproduce_migration.py]]
│   ├── temp_doctor_repro/
│   │   └── [[valid_task.md]]
│   ├── [[test_doctor_extraneous.py]]
│   ├── [[test_note_creator_main.py]]
│   ├── [[test_note_creator_tui.py]]
│   ├── [[test_processor.py]]
│   ├── [[test_title_normalizer.py]]
│   ├── [[test_tui_widgets.py]]
│   ├── [[test_tui_wizard.py]]
│   ├── [[test_validator.py]]
│   ├── [[test_wizard_app.py]]
│   └── [[verify_source_fix.py]]
├── [[uv.lock]]
└── [[verify_defaults.py]]
\\n