### `app.py` (Note Migrator)

- **Ubicación Original:** `src/dx_vault_atlas/services/note_migrator/app.py`
- **Propósito Exhaustivo:** Orquestador principal del motor de migración masiva. A diferencia del `Note Doctor` (cuyo objetivo es "Sanar" errores individuales en notas según sus modelos Pydantic), el `Note Migrator` está diseñado para "Evolucionar" arquitectónicamente una Bóveda entera de Obsidian desde un esquema de base de datos antiguo hacia uno moderno (ej. v1.0 a v2.0). Ejecuta transformaciones masivas por lotes.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** 
      - Dependencias globales (`settings`, Escáner).
      - Banderas `rename_only` (que salta inyecciones o borrados limitándose a renombrar llaves YAML) y `debug_mode`.
    - **Process:**
        ```mermaid
        graph TD
            A[Inicio: run] --> B{¿Usuario confirma Backup?}
            B -- No --> C[Abortar Ejecución Segura]
            B -- Sí --> D[Escanear Bóveda VaultScanner]
            D --> E[Iterar Archivos: _migrate_note_if_needed]
            E --> F[Parsear YAML]
            F --> G{¿Tiene Frontmatter?}
            G -- No --> H[Saltar]
            G -- Sí --> I[TransformationService.transform]
            I --> J{¿Hubo cambios?}
            J -- Sí --> K[_write_note y Contar +1 Modificada]
            J -- No --> L[Contar +1 Saltada]
            K --> M[Siguiente Nota]
            L --> M
            M --> N[Imprimir Resumen Final]
        ```
    - **Output:**
      - Escritura física en bloque de miles de archivos (`file_path.write_text`).
      - Estadísticas enriquecidas de migración en terminal `rich`.

- **Desglose Interno:**
    - `class MigratorApp`: Contenedor de estado para inyección de dependencias.
    - `run()`: Solicita confirmación explícita de seguridad antes de actuar (protección de datos) y orquesta el bucle de conteo (migrated, error, skipped).
    - `_migrate_note_if_needed()`: Filtra rápidamente archivos ilegibles, que no sean Markdown o que carezcan de metadatos YAML al inicio para evitar gastar ciclos de procesamiento en assets (como imágenes incrustadas o PDFs).
    - `_write_note()`: Envoltorio para la capa de serialización destructiva.

- **Dependencias:**
    - **Internas:** 
      - `[[transformation_service.py]]`.
      - `[[yaml_parser.py]]`.
      - `[[scanner.py]]`, `[[config.py]]`, `[[console.py (shared)]]`.
    - **Externas:** `pathlib.Path`.

> [!WARNING] Deuda Técnica:
> El `YamlParserService` se está importando repetidamente tanto en `note_doctor` como en `note_migrator` desde la carpeta profunda de `note_migrator/services/`. Esta utilidad de parseo y serialización YAML es lo suficientemente agnóstica como para pertenecer a `shared/`, lo que indica un problema de límite de dominios ("Domain Boundary Violation").

> [!INFO] Nota de Arquitectura:
> **Hard-Break Inclusivo:** La solicitud interactiva estricta `ui.confirm("\n[?] Have you backed up your vault?")` previene la corrupción catastrófica de bases de conocimiento completas ante errores no previstos en las reglas de transformación masiva.
