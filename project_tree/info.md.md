### `info.md`

- **Ubicación Original:** `src/dx_vault_atlas/services/note_creator/templates/info.md`
- **Propósito Exhaustivo:** Este archivo es un "Asset" / Plantilla Jinja puro. Sirve como el esqueleto crudo para formatear las "Notas de Información" (`InfoNote`) depositadas en Obsidian. Determina exactamente el orden vertical de las declaraciones YAML Frontmatter.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** Variables renderizadas mediante Inyección Jinja2 (`{{ variable }}`) facilitadas por la instancia Pydantic `InfoNote`. 
        - `version`
        - `title`
        - `aliases`
        - `tags`
        - `created`, `updated`
        - `type`
        - `source`, `priority`, `status`
    - **Process:** No contiene lógica condicional. Es un recurso pasivo interpretado por `[[templating.py]]`.
    - **Output:** Cadena de texto YAML válida y separadores de frontmatter Markdown `---` con el formato literal correcto.

- **Desglose Interno:**
    - Bloque de Cabecera (Líneas 1-12): Define el Metadata del Engine de Dataview en Obsidian.
    - Bloque de Cuerpo: Vacío intencionalmente, a la espera de un `append` dinámico por el NoteProcessor.

- **Dependencias:**
    - **Internas:** Consumido directamente por `[[templating.py]]` y mapeado en `[[enums.py]]` como `NoteTemplate.INFO`.
    - **Externas:** N/A.

> [!INFO] Nota de Arquitectura:
> La sintaxis obligatoria de listas para vectores como `aliases` y `tags` se delegó a la serialización interna de Pydantic (`.model_dump()`), por lo que aquí basta con inyectar el token directo `{{ tags }}` en lugar de recorrerlos con un For-Loop de Jinja `{% for %}`, manteniendo la plantilla notablemente limpia.
