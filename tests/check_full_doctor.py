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

note2 = vault / "000_Home.md"
note2.write_text(
    """---
version: '1.0'
title: 000_Home
aliases: []
tags: []
created: 2026-02-18 02:43:06
updated: 2026-02-18 02:43:06.960640
type: moc
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
app.run(debug_mode=True)
