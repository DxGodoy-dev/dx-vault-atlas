### `moc.md`

- **Ubicación Original:** `src/dx_vault_atlas/services/note_creator/templates/moc.md`
- **Propósito Exhaustivo:** Plantilla Jinja destinada a la generación de archivos MOC (Map of Content). Funciona como el andamiaje principal para inyectar metadatos en notas estructurales superiores dentro de la jerarquía de Obsidian.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** Variables renderizadas mediante `[[templating.py]]` usando el modelo `MocNote`. Admite parámetros estándar más `level` y `up` vacíos por defecto.
    - **Process:** Ausencia de lógica. Interpretado pasivamente por el renderizador.
    - **Output:** Texto en formato YAML + Markdown compatible.

- **Desglose Interno:**
    - Bloque YAML: Contiene llaves exclusivas de la rúbrica MOC como `level` (para dictaminar cardinalidad de importancia organizacional) y `up: "[[ ]]"` (enlace WikiLink preparado para conectar manualmente al MOC padre superior).

- **Dependencias:**
    - **Internas:** Usado por `[[templating.py]]`. Su gemelo lógico en código es el modelo Pydantic `MocNote`.
    - **Externas:** N/A.

> [!INFO] Nota de Arquitectura:
> A diferencia de `info.md`, los MOC por diseño en este sistema ignoran propiedades transitorias (ej. no tienen `status`, `priority` o `source`) pues su nivel de abstracción es únicamente navegacional.
