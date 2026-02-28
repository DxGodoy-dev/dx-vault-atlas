### `enums.py`

- **Ubicación Original:** `src/dx_vault_atlas/services/note_creator/models/enums.py`
- **Propósito Exhaustivo:** Actúa como el diccionario estricto del dominio (`Domain Language`) especificando todas las categorías válidas de metadatos (Frontmatter YAML) dentro de la creación de Notas del sistema. Facilita el autocompletado en el IDE y evita los típicos *Magic Strings* esparcidos por la aplicación.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** N/A (Definición de Tipos).
    - **Process:**
      - Agrupa valores en clases nativas `IntEnum` y `StrEnum`. No existe flujo lógico para aplicar diagramas Mermaid.
    - **Output:**
      - Las enumeraciones tipadas y cerradas para controlar qué strings y números pueden ingresar a la creación de Pydantic Models y formularios TUI.

- **Desglose Interno:**
    - `Priority (IntEnum)`: Grados numéricos de urgencia `{1: LOW, 2: MEDIUM, ..., 5: URGENT}`. Al ser `IntEnum` permite comparar numéricamente si `P1 > P2` desde el exterior.
    - `NoteStatus (StrEnum)`: Los estados de progreso ("to_do", "in_progress", etc).
    - `NoteSource (StrEnum)`: Orígenes documentales de la nota (ej. YouTube, IA, me).
    - `NoteTemplate (StrEnum)`: Archivos literales de plantillas con extensión (`"info.md"`, `"task.md"`, etc).
    - `NoteArea (StrEnum)`: Clasificación a alto nivel (Personal vs Work).

- **Dependencias:**
    - **Internas:** Ninguna.
    - **Externas:** `enum.IntEnum`, `enum.StrEnum` de la librería estándar de Python.

> [!INFO] Nota de Arquitectura:
> La decisión de que `Priority` sea un `IntEnum` fue acertada, ya que en sistemas de Markdown Dataview la comparación cuantitativa de prioridades es un patrón dominante. Mantiene la extensibilidad abierta si se necesita un nivel superior a URGENT en el futuro.
