### `validator.py` (Note Doctor)

- **Ubicación Original:** `src/dx_vault_atlas/services/note_doctor/validator.py`
- **Propósito Exhaustivo:** Constituye el "Motor Diagnóstico" del Note Doctor. Lee archivos físicos en disco y los somete a una batería estricta de validaciones cruzándolos contra los modelos teóricos de Pydantic definidos en Note Creator. Su propósito no es arreglar problemas, sino levantar un inventario estructurado (`ValidationResult`) de todos los campos faltantes, tipos de datos anómalos, incongruencias estructurales y versiones obsoletas de YAML.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** La ruta física del archivo (`Path`) o su contenido crudo (Frontmatter Data + Body Content).
    - **Process:**
        ```mermaid
        graph TD
            A[validate] --> B[Parsear Archivo con YamlParser]
            B --> C{¿Error de Lectura?}
            C -- Sí --> D[Devolver ValidationError Temprano]
            C -- No --> E[validate_content: _check_required]
            E --> F[_check_integrity: Títulos, Nombres de Archivo, Alias]
            F --> G[_check_enums: Area, Priority, Source]
            G --> H[_check_version: Comparar SCHEMA_VERSION]
            H --> I[_run_pydantic]
            I --> J[Filtrar campos desconocidos para evitar Crash Pydantic]
            J --> K[Instanciar Modelo Falso en Memoria]
            K --> |Éxito| L[Agrupar en Result Object]
            K --> |Fallo| M[Capturar pydantic.ValidationError y Parsear Keys]
            M --> L
            L --> N[Retornar ValidationResult Dto]
        ```
    - **Output:**
      - Objeto estandarizado `ValidationResult` que empaqueta:
        - `is_valid` (bool)
        - `missing_fields` (list)
        - `invalid_fields` (list)
        - `warnings` (list)
        - `error` (str opcional, en caso de fatalidad).

- **Desglose Interno:**
    - `ValidationResult`: Clase portadora de datos (Data Transfer Object) de la salida.
    - `NoteDoctorValidator`: Modulo base de ejecución.
      - `_read_and_parse()`: Captura OSError y yaml-errors.
      - `_check_integrity()`: Verifica colisiones semánticas: compara el `stem` original del `.md` sanitizado contra el YAML "title", y comprueba que el "title" exista dentro del vector "aliases".
      - `_check_enums()`: Valida manualmente y envuelve `ValueError` para dar warnings en lugar de crashes (ej. "unknown_source: IA").
      - `_check_version()`: Usa `packaging.version` para evaluar semántica Mayor.Menor.
      - `_run_pydantic()`: Ejecución final para atrapar tipos erróneos profundos (e.g., fecha inválida, string en lugar de booleano).

- **Dependencias:**
    - **Internas:** 
      - `[[defaults.py]]` (`SCHEMA_VERSION`)
      - `[[enums.py]]`
      - `[[note.py]]` (Pydantic Models)
      - `[[title_normalizer.py]]` (Para chequear integridad de filename)
      - `[[yaml_parser.py]]` (Parseo sintáctico previo)
      - `[[pydantic_utils.py]]` (`strip_unknown_fields`)
    - **Externas:** `packaging.version.parse`, `pydantic.ValidationError`, `re`.

> [!INFO] Nota de Arquitectura:
> **Pydantic Stripping:** La llamada a `strip_unknown_fields` antes de instanciar un validador Pydantic es una táctica defensiva crítica. Si un usuario inyecta manualmente un campo extra en YAML (ej: `myVar: true`), pasar ese dict a Pydantic en modo "extra: forbid" provocaría el fallo por sobrecarga antes de lograr auditar los campos requeridos. Aquí el validador esquiva los campos foráneos para testear primero lo central.
