### `fixer.py` (Note Doctor)

- **Ubicación Original:** `src/dx_vault_atlas/services/note_doctor/core/fixer.py`
- **Propósito Exhaustivo:** Repositorio central de la Inteligencia de Auto-Sanación de la Bóveda. El `NoteFixer` aborda los problemas técnicos detectados por el Validator e intenta resolverlos silenciosamente (Auto-fix) mediante mutación del YAML sin necesidad de intervención manual. Cubre tareas como rescatar fechas desde los nombres de archivo, extirpar campos basura que rompen esquemas Pydantic, y asegurar que propiedades tipo List de YAML mal declaradas se aplanen a String.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** 
      - En su método pivote `fix`: Recibe la ruta `file_path`, el diccionario de YAML crudo (`current`) y el texto del resto de la nota (`body`).
    - **Process:**
        ```mermaid
        graph TD
            A[Entrada: fix] --> B[check_and_fix_dates]
            B --> C[check_and_fix_enums]
            C --> D[check_and_fix_defaults]
            D --> E[check_and_fix_extraneous]
            
            subgraph check_and_fix_dates
                B1[Llamar DateResolver para Creado] --> B2[Remover Timezone, Descartar Futuro]
                B2 --> B3[Fijar 'Updated' igual o mayor que Creado]
            end
            
            subgraph check_and_fix_enums
                C1[Normalizar Status: de Array a String si es necesario] --> C2[Normalizar Area y Type]
                C2 --> C3[Asegurar Task/Project con default To_do y P1]
            end
            
            subgraph check_and_fix_defaults
                D1[Listar Campos model_fields seguros] --> D2{¿Tienen valor default en Pydantic?}
                D2 -- Sí --> D3[Inyectar valor Default]
            end
            
            subgraph check_and_fix_extraneous
                E1{¿Pydantic tiene extra: forbid?}
                E1 -- Sí --> E2[Eliminar Claves YAML no documentadas]
            end
            
            E --> F[Retornar bool de si hubo cambios y Data Fixeada]
        ```
    - **Output:**
      - Devuelve una tupla: `(total_changes: bool, current: dict, body: str)`. Esto alerta a `[[note_doctor_app.py.md]]` si es necesario volver a guardar el archivo físico en el disco duro o si no se hizo nada.

- **Desglose Interno:**
    - Helpers top-level: `_strip_tz` (para comparar tiempos UTC puros sin fallos), `_normalize_key` (aplana texto quitando mayúsculas y espacios).
    - `class NoteFixer`: Expone 5 funciones cardinales públicas (incluyendo la orquestadora `fix`).
      - Constante centinela `_SENTINEL = object()`: Truco avanzado en Python usado para diferenciar explícitamente entre un valor por defecto que es literalmente `None` y la "carencia abstracta" de valor por defecto.
      - Métodos Privados Enum: `_fix_status`, `_fix_area`, `_fix_aliases_tags` aplican conversiones de coerción permisivas (ej. si el status es `['to_do']` debido a un bug de YAML List, se reescribe como `"to_do"`).

- **Dependencias:**
    - **Internas:** 
      - `[[date_resolver.py]]`
      - `[[enums.py]]` y `[[note.py]]`
      - `[[yaml_parser.py]]`
      - `[[validator.py]]` (Exponiendo `MODEL_MAP`)
    - **Externas:** `datetime.datetime`, `pydantic_core.PydanticUndefined`.

> [!INFO] Nota de Arquitectura:
> **Resistencia de Tipos a Nivel Fixer:** Cuando se extrae el default dinámicamente de un modelo Pydantic usando el introspector `model_cls.model_fields[field_name]`, en lugar de hardcodearlos, el `NoteFixer` se auto-acopla mágicamente y nunca necesitará actualizarse aunque los defaults teóricos cambien masivamente en `NoteCreator`.

> [!BUG] Riesgo Potencial (¡CRÍTICO!):
> **Conflictos de Fusión expuestos.** Al igual que en `app.py`, en las líneas 206-210 del método `check_and_fix_extraneous()` coexisten de manera destructiva separadores de Merge Conflict introducidos y jamás devueltos (`<<<<<<< HEAD`, `=======`, `>>>>>>>`). Esto imposibilita la ejecución natural provocando cuelgues sintácticos en Python.
