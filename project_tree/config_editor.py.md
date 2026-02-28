### `config_editor.py` (Shared TUI)

- **Ubicación Original:** `src/dx_vault_atlas/shared/tui/config_editor.py`
- **Propósito Exhaustivo:** Implementa la interfaz interactiva "Día Dos" a base de texto CLI estándar (`rich`). Permite al usuario revisar, descartar y auditar la configuración activa del sistema desde consola (`dxva config`). A través de él, se pueden mutar dicts complejos como mapeos de traducciones para el Note Migrator (`field_mappings`).

- **Modelo IPO (Input, Process, Output):**
    - **Input:** Caracteres numéricos o Strings respondidos al `IntPrompt.ask`.
    - **Process:**
      - `_ensure_config()`: Valida si ya hay configuración. Si accidentalmente un usuario borró el JSON, fuerza la re-ejecución del Módulo Setup (`config_wizard.py`).
      - Bucle infinito `while True:` que dibuja el menú de opciones.
      - Rutea lógica modularizada hacia inyecciones en memoria en el objeto `GlobalConfig`: `_edit_paths()`, `_edit_mappings()`, etc.
      - Altera temporalmente el diccionario interno hasta que el usuario pulsa 5 (`Save`), invocando `ConfigManager.save()` destructivo. 0 descarta.
    - **Output:** Formateo de Terminal `rich` con reglas horizontales y actualizaciones guardadas subyacentes en el disco XDG.

- **Desglose Interno:**
    - `ConfigEditor`
      - `run()`
      - Múltiples loops `_edit_*` especializados. Validadores acoplados como `Prompt.ask` con invocación a `validate_directory`.

- **Dependencias:**
    - **Internas:** 
      - `[[shared_console.py.md|console.py]]`
      - `[[config.py]]`
      - `[[config_wizard.py]]`
    - **Externas:** `rich.prompt.IntPrompt`.

> [!INFO] Nota de Arquitectura:
> Este archivo hace un uso intensivo de Modulación de Consola en memoria. Al inyectar todas las respuestas temporalmente a la instancia `GlobalConfig` y sólo guardarlas tras un commit explícito (Guardar y Salir), asegura atomicidad transaccional: una escritura equivocada iterando opciones jamás corrompe la bóveda hasta que el usuario decida consolidar los cambios.
