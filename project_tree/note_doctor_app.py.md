### `app.py` (Note Doctor)

- **Ubicación Original:** `src/dx_vault_atlas/services/note_doctor/app.py`
- **Propósito Exhaustivo:** Es el orquestador principal (God Object) del subsistema `Note Doctor`. Escanea masivamente la bóveda de Obsidian (`Vault`), valida de forma estricta los esquemas del Frontmatter (usando Pydantic models implícitos), intenta auto-corregir problemas menores automáticamente (`NoteFixer`), aplica mapeos de sanitización, y finalmente coordina un bucle interactivo de solicitud al usuario (CLI o TUI) para parchar (`Patcher`) las notas que continúan inválidas, todo mientras informa estadísticas por consola.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** 
      - Objeto `GlobalConfig` con el `vault_path`.
      - Archivos provenientes de `VaultScanner.scan()`.
      - Parámetros bandera booleanos de CLI (`fix_date`, `debug_mode`).
      - Input de usuario recuperado por `DoctorTUI.gather_fixes()`.
    - **Process:**
        ```mermaid
        graph TD
            A[Inicio: run] --> B[Escanear Bóveda]
            B --> C{¿Modo fix_date?}
            C -- Sí --> D[Ejecutar _run_date_fix_mode y Fin]
            C -- No --> E[Ejecutar _run_full_check_mode]
            E --> F[Iterar sobre notas: _classify_note]
            F --> G[1. validator.validate]
            G --> H{¿Error Grave YAML?}
            H -- Sí --> I[Retornar Invalid]
            H -- No --> J[2. fixer.fix : Auto-reparar]
            J --> K[3. Aplicar field / value mappings]
            K --> L{¿Hubo Cambios Auto?}
            L -- Sí --> M[Re-validar y Escribir]
            L -- No --> N[Etiquetar Valid / Warning / Version]
            M --> O[Agrupar Resultados]
            N --> O
            O --> P[Mostrar Resumen Consola]
            P --> Q[Bucle Múltiple: _process_invalid_results]
            Q --> R{¿El Usuario Brinda Fixes?}
            R -- Sí --> S[patcher.apply_fixes y Guardar]
            R -- No/Skip --> T[Saltar a la siguiente]
            S --> Q
            T --> Q
        ```
    - **Output:**
      - Escritura destructiva (modificación in situ) de los archivos Markdown vía `yaml_parser.serialize_frontmatter`.
      - Salida en consola interactiva (`rich`) mostrando notas escaneadas, válidas, warnings e invalidas.

- **Desglose Interno:**
    - `DoctorApp`:
      - `run()`: Entrypoint de alto nivel.
      - `_run_date_fix_mode()`: Ejecuta una vía rápida para únicamente arreglar las fechas (created/updated) según el parseador `fixer`.
      - `_run_full_check_mode()`: Iterador maestro. Cuenta las sanas e insanas.
      - `_classify_note()`: El corazón analítico. Intenta la validación primaria, luego la auto-reparación, el mapeo diccionario, revalidación y clasiificación final.
      - `_apply_field_mappings()` / `_apply_value_mappings()`: Interceptan llaves de YAML para mutar keys legacy (ej. `categoría` -> `area`).
      - `_process_invalid_results()`: Maneja el bucle de "segunda unida", pidiendo intervención humana archivo por archivo.
      - Opciones `_handle_rename()`, `_gather_fixes_cli()`: Soporte al TUI.

- **Dependencias:**
    - **Internas:** 
      - `[[fixer.py]]`, `[[patcher.py]]`, `[[tui.py]]`, `[[validator.py]]` (Todos de Note Doctor).
      - `[[yaml_parser.py]]` (Curiosamente cruza dependencias con `Note Migrator`).
      - `[[title_normalizer.py]]` (Para `_handle_rename`).
      - `[[scanner.py]]`, `[[console.py (shared)]]`.
    - **Externas:** `re`, `pathlib`, `typing`.

> [!WARNING] Deuda Técnica:
> Este archivo representa un "God Object". Emplea más de 670 líneas de código encapsulando flujos lógicos enormes y ramificaciones pesadas (`_classify_note` es especialmente denso), mezclando además inyecciones de CLI rudimentario con delegaciones al TUI moderno.

> [!BUG] Riesgo Potencial (¡CRÍTICO!):
> **Inyección de Conflicto Git no resuelto en código vivo.** En las líneas 181-191 se evidencia la presencia de los marcadores de conflicto clásicos de Git (`<<<<<<< HEAD ... ======= ... >>>>>>>`). Si el intérprete aterriza en este if under `debug_mode=True`, el archivo provocará un volcado por `SyntaxError` global y la aplicación fallará espectacularmente sin compilar.
