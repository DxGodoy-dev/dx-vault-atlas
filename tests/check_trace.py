import os
import shutil
from pathlib import Path

from dx_vault_atlas.shared.config import GlobalConfig
from dx_vault_atlas.services.note_doctor.app import create_app

vault = Path("test_vault")
if vault.exists():
    shutil.rmtree(vault)
inbox = vault / "00_Inbox"
inbox.mkdir(parents=True)

# File WITHOUT source
note1 = inbox / "20260218024306_mejores_practicas_para_agentes_en_google_antigravity.md"
note1.write_text(
    """---
version: '1.0'
title: Mejores Prácticas para Agentes en Google Antigravity
aliases:
- Mejores Prácticas para Agentes en Google Antigravity
tags: []
created: 2026-02-18 02:43:06
updated: 2026-02-18 02:43:06.960640
type: ref
---
# body
""",
    encoding="utf-8",
)

config = GlobalConfig(
    vault_path=vault,
    vault_inbox=inbox,
    field_mappings={"date": "created"},
    value_mappings={"source": {"gemini": "ia"}},
)

app = create_app(config)

# Monkeypatch _classify_note to see the trace
orig_classify = app._classify_note


def trace_classify(note_path, debug_mode):
    print("-------")
    print(f"Tracing {note_path.name}")
    print(f"File content before validate:\n{note_path.read_text(encoding='utf-8')}")
    res = app.validator.validate(note_path)
    print(
        f"Validate Result: is_valid={res.is_valid}, invalid={res.invalid_fields}, frontmatter={res.frontmatter}"
    )
    has_changes, fm_final, body = app.fixer.fix(
        note_path, res.frontmatter.copy(), res.body
    )
    print(f"After fixer.fix: has_changes={has_changes}, fm_final={fm_final}")

    b1 = app._apply_field_mappings(fm_final)
    print(f"After field mappings: b1={b1}, fm_final={fm_final}")

    b2 = app._apply_value_mappings(fm_final)
    print(f"After value mappings: b2={b2}, fm_final={fm_final}")

    return orig_classify(note_path, debug_mode)


app._classify_note = trace_classify
app.run(debug_mode=True)
