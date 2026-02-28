### `yaml_parser.py` (Note Migrator)

- **Ubicación Original:** `src/dx_vault_atlas/services/note_migrator/services/yaml_parser.py`
- **Propósito Exhaustivo:** Constituye la interfaz de lectura y escritura a bajo nivel (I/O) para manipular los atributos físicos de los metadatos de las notas. Extrae asépticamente el bloque de **YAML Frontmatter** incrustado entre los separadores `---` en la cabecera de un archivo Markdown, aislando el contenido del cuerpo (body), para luego poder inyectar versiones parcheadas del diccionario nuevamente a un formato serializado compatible con Obsidian.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** String puro con el contenido completo del archivo Markdown (`content`).
    - **Process:**
      - **En parseo:** Emplea una expresión regular (`FRONTMATTER_PATTERN`) buscando coincidencias exactas del patrón divisor `---`. Si no encuentra metadatos, asume que todo es cuerpo y retorna una tupla vacía y la bandera `has_yaml=False`. Delega la decodificación pesada a `yaml.safe_load`.
      - **En serialización:** Llama a `yaml.dump()` forzando configuración estricta (`sort_keys=False` para respetar el reordenamiento del parcher, y formateo expandido no inline bloqueando el `default_flow_style`).
    - **Output:** 
      - Al leer: El DataClass envoltorio `ParsedNote`.
      - Al escribir: Un String reconstruido (`f"---\n{yaml_content}---\n"`).

- **Desglose Interno:**
    - `class YamlParseError`: Exception Custom para evitar propagar errores genéricos de las dependencias Pypi.
    - `@dataclass ParsedNote`: Clase portadora de datos (DTO). Almacena Diccionario Pydantic, cadena de Cuerpo y Booleano de estado.
    - `class YamlParserService`: Exposición de métodos lógicos. Contiene la Regex pre-compilada.
      - `parse()`
      - `serialize_frontmatter()`

- **Dependencias:**
    - **Internas:** Ninguna (Es un módulo hoja, altamente dependiente él mismo).
    - **Externas:** `re`, `dataclasses.dataclass`, librería de terceros `PyYAML` (`yaml`).

> [!INFO] Nota de Arquitectura:
> **Aislamiento Físico Exitoso:** Al delegar la manipulación Regex a este archivo en lugar de inyectar llamadas a `re` o `yaml` directamente dentro del bucle de validación de Doctor o Migrator, el código garantiza el principio de Single Responsibility (SRP). Si mañana Obsidian cambia su motor de metadatos (por ejemplo a JSON), solo se deberia re-escribir esta pequeña clase sin afectar la lógica analítica de los bots.

> [!WARNING] Deuda Técnica:
> Este archivo es ampliamente invocado por todos los servicios (`Note Doctor`, `Note Migrator` y posiblemente otros). Sin embargo, se encuentra físicamente atrapado dentro del dominio `/services/note_migrator/services/`. Debería refactorizarse moviéndolo a la carpeta raíz `/shared/core/` para no vulnerar el aislamiento de sub-dominios.
