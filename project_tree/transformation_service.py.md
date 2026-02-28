### `transformation_service.py`

- **Ubicación Original:** `src/dx_vault_atlas/services/note_migrator/core/transformation_service.py`
- **Propósito Exhaustivo:** Constituye el "Motor de Evolución de Esquema". Su misión exclusiva es asegurar que el esquema de base de datos YAML (las llaves Frontmatter) coincida matemáticamente con la versión estructural más reciente soportada por la aplicación (`SCHEMA_VERSION`). Es un proceso destructivo que extirpa variables obsoletas y construye metadatos rudimentarios para que el subsistema `Note Doctor` pueda repararlos posteriormente.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** 
      - El objeto `frontmatter` crudo cargado desde disco.
      - Parámetros bandera para limitar el proceso (`rename_only`).
    - **Process:**
        ```mermaid
        graph TD
            A[Entrada: transform] --> B{¿rename_only es True?}
            B -- Sí --> C[Retorno Temprano sin Inyecciones]
            B -- No --> D[Parsear versión SemVer del archivo actual]
            D --> E{¿Versión < SCHEMA_VERSION o Nulo?}
            E -- Sí --> F[Activar bandera should_update_version]
            E -- No --> G[Verificar Existencia de Claves Críticas]
            F --> G
            G --> H{¿Falta 'created' o 'updated'?}
            H -- Sí --> I[Inyectar 'created': null]
            H -- No --> J
            I --> J[Actualizar campo 'version' si es necesario]
            J --> K[_enforce_model_schema]
            K --> L[Instanciar Model Pydantic Falso]
            L --> M[Eliminar toda clave YAML que no exista en el Modelo]
            M --> N[Retornar Nuevo Diccionario Limpio e Indicador has_changes]
        ```
    - **Output:**
      - Tupla: `(updated_frontmatter: dict, has_changes: bool)`.

- **Desglose Interno:**
    - `class TransformationService`: Única estructura de control.
        - `transform()`: Evalúa versiones. Nunca adivina o extrae fechas, simplemente inyecta contenedores vacíos (`None`) para evitar fallos de instanciación en fases posteriores.
        - `_enforce_model_schema()`: Llama agresivamente a `strip_unknown_fields` pasándole la maqueta Pydantic correspondiente. Es la guillotina final para campos obsoletos ("legacy metadata").

- **Dependencias:**
    - **Internas:** 
      - `[[defaults.py]]` (`SCHEMA_VERSION`)
      - `[[note_doctor_validator.py.md|validator.py]]` (`MODEL_MAP`)
      - `[[pydantic_utils.py]]` (`strip_unknown_fields`)
    - **Externas:** `packaging.version.parse`.

> [!INFO] Nota de Arquitectura:
> **Chain of Responsibility (Responsabilidad Segregada):** Es vital observar que este servicio se niega a intentar arreglar una fecha si `created` está vacío. Al inyectar un `null`, asegura que todos los archivos migrados puedan ser parseados por Python sin *KeyErrors*, para que luego el servicio `[[date_resolver.py]]` del `Note Doctor` asuma el complejo trabajo de reconstruir el instante temporal desde el nombre de archivo de forma especializada.
