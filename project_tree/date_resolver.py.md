### `date_resolver.py`

- **Ubicación Original:** `src/dx_vault_atlas/services/note_doctor/core/date_resolver.py`
- **Propósito Exhaustivo:** Constituye la herramienta de rescate temporal del `Note Doctor`. Cuando una nota ha perdido, corrompido o jamás tuvo sus propiedades de `created` o `updated` en el YAML, esta clase extrae e interpreta la estampa de tiempo Zettelkasten incrustada en el propio nombre físico del archivo (su prefijo numérico). Garantiza recuperar el instante original de creación evitando depender de la inestable metadata del Sistema Operativo (`mtime`/`ctime`).

- **Modelo IPO (Input, Process, Output):**
    - **Input:** 
      - En el Extractor: Un string correspondiente al `stem` (nombre sin extensión) del archivo (ej: `"20250101153022_mi_viaje"`).
    - **Process:**
      - Revisa que los primeros 8 caracteres sean dígitos.
      - Intenta recortar los primeros 14 (`YYYYMMDDHHMMSS`) o 12 dígitos (`YYYYMMDDHHMM`).
      - Si encuentra un bloque, lo parsea contra `datetime.strptime()` infiriendo el formato correcto.
      - Evita bucles lógicos condicionales iterativos en favor de regresión descendente simple, por ello omite `mermaid`.
      - Cruza agresivamente el tiempo extraído contra el `datetime.now()` del sistema. Si de alguna manera el nombre del archivo dicta un punto en el **futuro**, descalifica la fecha retornando `None`.
    - **Output:**
      - Objeto nativo `datetime` válido y seguro, o de lo contrario `None` (obligando a la falla para que el TUI asuma manualidad).

- **Desglose Interno:**
    - `class DateResolver`: 
      - `@staticmethod extract_timestamp_from_stem()`: Rebanador de strings estricto.
      - `@staticmethod resolve_created()`: Emplea el extractor, moldea a datetime y valida contra viajes en el tiempo (fechas futuras).
      - `@staticmethod resolve_updated()`: Retorna `None` intencional. Esto es un "Stub" arquitectónico porque según las reglas estrictas de la aplicación, está prohibido inventar fechas modificadas si no existe un rastro de texto claro que la ampare, por lo que delega a las capas superiores la invención de un fallback lógico (ej: `updated = created`).

- **Dependencias:**
    - **Internas:** Ninguna.
    - **Externas:** `datetime`, `pathlib.Path`.

> [!INFO] Nota de Arquitectura:
> **Strict Non-Metadata Rule (Regla de Independencia de Metadatos OS):** Al deshabilitar conscientemente el rescate mediante los atributos `st_ctime/st_mtime` del disco duro nativo usando Python `os.stat`, el desarrollador asegura la inmutabilidad de la Bóveda Obsidian a través de sincronizaciones cloud (como Google Drive u OneDrive) que frecuentemente "destruyen" y sobreescriben fechas de metadatos de archivos cuando se descargan en ordenadores frescos. El nombre del archivo siempre sobrevive.
