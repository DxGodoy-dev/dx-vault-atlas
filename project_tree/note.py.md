### `note.py`

- **Ubicación Original:** `src/dx_vault_atlas/services/note_creator/models/note.py`
- **Propósito Exhaustivo:** Constituye el corazón de la integridad de datos del `Note Creator`. Define los modelos `Pydantic` que representan estructuralmente todos los tipos de notas posibles en el ecosistema de Obsidian. Al heredar de `BaseModel`, garantiza que toda la data inyectada desde el wizard TUI pase por una férrea validación de tipos, coerción automática y aplicación de valores por defecto antes de ser enviada al renderizador Jinja2.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** 
      - Cargas de datos en formato de argumentos por palabra clave (`**kwargs`) provenientes del `NoteFactory`.
      - Extracción de literales globales (ej: `SCHEMA_VERSION` desde `[[defaults.py]]`).
    - **Process:**
        ```mermaid
        classDiagram
            class BaseNote {
                +version: str
                +title: str
                +aliases: list[str]
                +tags: list[str]
                +created: datetime
                +updated: datetime
                +note_type: str
                +ensure_list()
                +coerce_version()
            }
            BaseNote <|-- MocNote
            BaseNote <|-- RefNote
            BaseNote <|-- RankedNote
            
            class RankedNote {
                +source: NoteSource | str
                +priority: Priority
            }
            RankedNote <|-- StatusNote
            
            class StatusNote {
                +status: NoteStatus
            }
            StatusNote <|-- InfoNote
            StatusNote <|-- WorkflowNote
            
            class WorkflowNote {
                +area: NoteArea
            }
            WorkflowNote <|-- ProjectNote
            WorkflowNote <|-- TaskNote
            
            class ProjectNote {
                +start_date: datetime
                +end_date: datetime
                +outcome: int
            }
            class TaskNote {
                +deadline: datetime
            }
        ```
        - Configura `model_config = {"extra": "forbid"}` para asegurar que atributos ajenos o mal escritos insertando basura en el Frontmatter sean rechazados radicalmente.
        - Ejecuta decoradores `@field_validator` de fase *"before"* para forzar que los `tags` siempre sean listas aunque llegue un String solitario, y blindar el número de versión (forzando Type Casting a `.to_str()`).
    - **Output:**
        - Instancias puras, validadas y tipadas exportadas para alimentar el motor dict de renderizado de plantillas. No posee efectos secundarios.

- **Desglose Interno:**
    - `BaseNote`: La plantilla raigal de toda nota Obsidian (creación, edición, título, tags).
    - `MocNote`, `RefNote`: Extendidas con campos atómicos como referenciadores `up` y `level`.
    - `RankedNote`: Intermediario lógico que inyecta parámetros de ponderación (source y priority).
    - `StatusNote`: Heredero que añade el campo Enum de estado (`status`).
    - `InfoNote`: Hereda de Status pero sobreescribe la variable forzando a `NoteStatus.TO_READ`.
    - `WorkflowNote`: Base dual para Entidades Accionables añadiendo el área de afectación (`NoteArea`).
    - `ProjectNote` / `TaskNote`: Nodos hojas especializados que agregan las fechas exactas paramétricas (deadline, start_date).

- **Dependencias:**
    - **Internas:** 
      - `[[defaults.py]]` (`SCHEMA_VERSION`)
      - `[[enums.py]]` (Todos los Enums).
    - **Externas:** `datetime.datetime`, `pydantic.BaseModel`, `pydantic.Field`, `pydantic.field_validator`.

> [!INFO] Nota de Arquitectura:
> La definición piramidal de herencia (`BaseNote -> RankedNote -> StatusNote -> WorkflowNote`) evita de forma inmaculada el código duplicado o espagueti que sucedería si cada uno de los 6 tipos de nota declararan todos sus 12 campos reiterativamente. Representa una ejecución estelar de herencia paramétrica.
