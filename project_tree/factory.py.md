### `factory.py`

- **Ubicación Original:** `src/dx_vault_atlas/services/note_creator/core/factory.py`
- **Propósito Exhaustivo:** Implementa el patrón de diseño "Factory" para tomar los datos crudos (diccionarios) producidos por la interfaz de usuario (TUI) y convertirlos en objetos fuertemente tipados (instancias de Pydantic Models como `TaskNote`, `InfoNote`, etc.). Se asegura de que la estructura de la nota cumple con el esquema establecido antes de pasar al motor de renderizado.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** 
      - Un diccionario crudo `data: dict[str, Any]` que viene de `[[tui.py]]`.
      - Importa enumeraciones (`NoteTemplate`) y modelos Pydantic base (`BaseNote`, `MocNote`, etc.) desde `[[enums.py]]` y `[[note.py]]`.
    - **Process:**
        ```mermaid
        graph TD
            A[Recibir Data Dict] --> B[Extraer Title y limpiar comillas]
            B --> C{¿Template es Enum o String?}
            C -- Enum --> D[Mapear directamente]
            C -- String --> E[Intentar Cargar como Enum]
            E --> |Fallo| F[Asignar None al Enum]
            D --> G[Extraer type_str quitando extensión .md]
            E --> |Éxito| G
            F --> G
            G --> H[Construir Dictionary Pydantic kwags]
            H --> I[Inyectar Source, Priority, Area, Status si existen]
            I --> J[Buscar clase en MODEL_MAP]
            J --> K[Instanciar Clase y Retornar]
        ```
        1. Extrae y formatea el título (escapando comillas para YAML `\"`).
        2. Intenta parsear la variable de template, resolviendo el problema de recibir strings crudos vs objetos Enum predecibles.
        3. Obtiene el nombre del tipo raíz usando `Path(...).stem` (ej. "task.md" -> "task").
        4. Crea el diccionario de argumentos principales (`title`, `aliases`, `tags`, `type`).
        5. Condicionalmente inyecta `source`, `priority`, `area`, `status` solo si vienen provistos.
        6. Busca la clase constructora correcta listada en `MODEL_MAP` o hace fallback a `BaseNote`.
        7. Inicializa el modelo y lo devuelve.

    - **Output:**
        - Una instancia validada de un Pydantic Model hijo de `BaseNote`.

- **Desglose Interno:**
    - `MODEL_MAP: dict`: Diccionario de enrutamiento que mapea la enumeración elegida con la clase del modelo Pydantic correcta.
    - `class NoteFactory`:
        - `@staticmethod create_note(data)`: Metodo maestro que implementa la lógica procedimental arriba descrita.

- **Dependencias:**
    - **Internas:** 
      - `[[defaults.py]]` (`DEFAULT_TAGS`)
      - `[[enums.py]]` (`NoteTemplate`)
      - `[[note.py]]` (`BaseNote` y todos su modelos herederos)
    - **Externas:** `pathlib.Path`, `typing.Any`

> [!INFO] Nota de Arquitectura:
> Se utiliza el Patrón Factory para separar el mapeo de los datos obtenidos en la terminal de las reglas estrictas de inicialización de los modelos.

> [!WARNING] Deuda Técnica:
> El bloque condicional de las líneas 44-65 posee alta complejidad ciclomática artificial forzada por no confiar en si la TUI retorna un objeto Enum o un simple String por error. Este código es propenso a errores silenciosos (`template_enum = None # type: ignore`) que lanzarán el fallback `BaseNote` ignorando propiedades específicas.
