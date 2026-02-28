### `ref.md`

- **Ubicación Original:** `src/dx_vault_atlas/services/note_creator/templates/ref.md`
- **Propósito Exhaustivo:** Plantilla Jinja minimalista para los nodos tipo Referencia Zettelkasten (`RefNote`). Mantiene un alcance y peso intencionalmente reducido sin cargar la base de datos de campos vacíos o ruidosos.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** Consume la clase Pydantic `RefNote`.
    - **Process:** Ninguno (render directo de campos Core).
    - **Output:** Salida Markdown textual.

- **Desglose Interno:**
    - Bloque Minimalista: Únicamente mapea variables nativas estándar (version, title, aliases, tags, created, updated, type).
    - Omite todo campo extendido.

- **Dependencias:**
    - **Internas:** `[[note.py]]` (`RefNote`).
    - **Externas:** N/A.
