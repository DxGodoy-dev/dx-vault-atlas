### `templating.py`

- **Ubicación Original:** `src/dx_vault_atlas/services/note_creator/services/templating.py`
- **Propósito Exhaustivo:** Encapsula y abstrae el motor de plantillas `Jinja2`. Se encarga de procesar los archivos base de Markdown ubicados en la carpeta `templates/` inyectando los datos vivos (variables tipadas provenientes del modelo Pydantic) para generar el archivo semi-final sin el cuerpo del usuario. Permite el uso de sintaxis dinámica como condicionales y ciclos dentro de los archivos `.md`.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** 
      - En Inicialización: La constante global `TEMPLATES_DIR` que apunta al directorio físico.
      - En `render`: El nombre de la plantilla (`str`) y una instancia Pydantic poblada (`BaseNote`).
    - **Process:**
        ```mermaid
        graph TD
            A[Inicializar TemplatingService] --> B[Cargar Environment Jinja2 desde FileSystemLoader]
            B --> C[Registrar filtro custom: format_date]
            C --> D[Espera Llamada Render]
            D --> E[Extraer Diccionario Serializado 'model_dump' del Pydantic Model]
            E --> F{¿Existe la Plantilla?}
            F -- Sí --> G[Inyectar Variables e Interpretar Jinja]
            F -- No --> H[Lanzar FileNotFoundError]
            G --> I[Retornar String Renderizado]
        ```
        1. Configura `Environment` limpiando espacios en blanco por defecto en los bloques de renderizado para no afectar YAML (`trim_blocks=True`).
        2. Inyecta el filtro `format_date` que castea strings ISO de vuelta a `datetime` y los formatea amigablemente.
        3. En `render()`, usa `model_dump(mode="json", by_alias=True)` lo cual permite garantizar que los objetos anidados o fechas vengan serializados y utilizando los nombres alias definidos en Pydantic (como `type` en lugar de `note_type`).
        4. Reemplaza las llaves `{{ variable }}` en el archivo físico.

    - **Output:**
        - Un mega-string (`str`) de texto renderizado que equivale a la cabeza y frontmatter de la nueva nota en Obsidian.

- **Desglose Interno:**
    - `class TemplatingService`: Contenedor de estado de Jinja2.
    - `__init__()`: Inicializa y acopla el entorno Jinja en memoria la primera vez.
    - `_format_date_filter()`: Función auxiliar de Jinja2. Evita que crasheen plantillas cuando fechas vienen vacías o mal formateadas.
    - `render(template_name, note_data)`: Motor principal de acoplamiento Datos-Vista.

- **Dependencias:**
    - **Internas:** 
      - `[[note.py]]` (`BaseNote`)
      - `[[paths.py]]` (`TEMPLATES_DIR`)
    - **Externas:** `datetime`, `jinja2.Environment`, `jinja2.FileSystemLoader`, `jinja2.TemplateNotFound`, `jinja2.select_autoescape`.

> [!INFO] Nota de Arquitectura:
> La inyección de dependencias `by_alias=True` en `model_dump` es crítica porque YAML prefiere keys limpios como `type`, pero al ser palabra reservada en Python, el Pydantic model internamente lo llama `note_type`. Este puente permite interoperabilidad sin escribir mapeos a mano.
