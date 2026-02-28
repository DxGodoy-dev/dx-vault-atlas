### `bootstrap.py` (Shared Core)

- **Ubicación Original:** `src/dx_vault_atlas/shared/core/bootstrap.py`
- **Propósito Exhaustivo:** Funciona como la rutina de "Arranque Mínimo" (Bootstrapper). Su único trabajo es interceptar la ejecución de la aplicación un instante antes de que actúen el Note Creator/Migrator/Doctor para garantizar que el aplicativo tenga una configuración XDG viva. Si no la encuentra, detiene la ejecución del sub-módulo y lanza de emergencia el asistente de "Primera Vez" (Setup Wizard) para que el usuario defina su ruta de Bóveda por consola.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** Cero argumentos implícitos. Llama a `get_config_manager().exists()`.
    - **Process:**
      - Evalúa si el archivo JSON persistente existe. Si es así, lo carga e inmediatamente devuelve el control.
      - De no existir, imprime texto de setup e invoca asíncronamente `run_setup_wizard()`.
      - Si el usuario aborta en mitad del asistente, llama a la utilidad privada `_exit_app()` (wrapper para `sys.exit(1)`) cerrando limpiamente sin un rastro en rojo de stack trace.
      - Si el setup triunfa, guarda la nueva configuración llamando al `ConfigManager.save()`.
    - **Output:**
      - Objeto estricto `GlobalConfig`.

- **Desglose Interno:**
    - `_exit_app(code)`: Wrapper utilitario simple.
    - `ensure_config_exists()`: Orquestador del flujo de protección de inicio.

- **Dependencias:**
    - **Internas:** 
      - `[[config.py]]`
      - `[[shared_console.py.md|console.py]]`
      - `[[config_wizard.py]]`
    - **Externas:** `sys`, `typing.NoReturn`.

> [!INFO] Nota de Arquitectura:
> **Onboarding sin Fricción:** Al centralizar la comprobación de la existencia de parámetros en la capa `core` y exponer el `ensure_config_exists()`, los módulos finales (como los Entrypoints `main.py` de Doctor o Creator) no tienen que preocuparse jamás de lidiar con Variables Nulas por usuarios nuevos que se saltaron la configuración.
