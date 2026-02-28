### `project.md`

- **Ubicación Original:** `src/dx_vault_atlas/services/note_creator/templates/project.md`
- **Propósito Exhaustivo:** Plantilla Jinja base para la creación del tipo de nota más complejo del ecosistema: `ProjectNote`. Acumula la mayor carga de llaves de metadatos (Data DNA) con el fin de rastrear estados de vida de proyectos y su línea temporal para automatizaciones posteriores en Obsidian Dataview.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** Recibe todas las variables asociadas a la herencia `ProjectNote` desde el orquestador Jinja2, incluyendo `priority`, `source`, `area`, `status`.
    - **Process:** Carga de frontmatter estático. Al igual que los demás templates, carece de bucles lógicos Jinja. 
    - **Output:** String exportable.

- **Desglose Interno:**
    - Extiende las propiedades basales incluyendo casilleros de ciclo de vida (`start:`, `completed:`, `deadline:`, `outcome:""`) que inicialmente se depositan en blanco tras la ejecución del script para rellenado dinámico mediante Obsidian en un futuro.

- **Dependencias:**
    - **Internas:** Correspondencia 1:1 con el modelo `ProjectNote` en `[[note.py]]`.
    - **Externas:** N/A.
