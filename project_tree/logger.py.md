### `logger.py` (Shared)

- **Ubicación Original:** `src/dx_vault_atlas/shared/logger.py`
- **Propósito Exhaustivo:** Implementa el sistema central de observabilidad y auditoría asincrónica (Logging). Refuerza una política de "Cero Print" (donde las operaciones internas no bloquean salidas de consola de usuario) redirigiendo el flujo de información de depuración humana hacia un sistema de bitácoras físicas de archivo rotatorio y bajo un formato estructurado.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** 
      - Cadenas textuales provenientes del uso del singleton `logger.info()`, `.debug()`, `.error()`, integrados en casi todo el ecosistema (Migrator, Doctor, Creator).
    - **Process:**
      - Determina de manera agnóstica la carpeta de sistema (`platformdirs.user_log_dir`) para depositar logs sin contaminar el repositorio actual.
      - **Idempotencia:** Bloquea inyecciones dobles de Handlers revisando `logger.hasHandlers()`.
      - Instala rotación automática de archivos (`RotatingFileHandler`) para evitar el consumo infinito de disco duro (límite de 5 MB, con hasta 3 copias de seguridad `app.log.1`, `app.log.2`).
      - Si fallan los permisos OS (`OSError`), en lugar de colapsar la aplicación entera, se degrada elegantemente: imprime un aviso en rojo a consola y engulle silenciosamente el error instalando un `logging.NullHandler()`.
      - Provee un activador explícito `enable_debug_logging()` invocado desde CLI cuando se corre el programa en modo diagnóstico (`dxva --debug`).
    - **Output:** Archivo físico `app.log` con formato estructurado (Tab-Separated-Like) para facilitar la lectura `grep`.

- **Desglose Interno:**
    - `setup_logger` (Funcion configuradora).
    - `enable_debug_logging` (Abre el grifo de los logs a la pantalla del usuario).
    - Variable Global Instanciada `logger` (Punto único de uso, Singleton pattern).

- **Dependencias:**
    - **Internas:** `[[paths.py]]`.
    - **Externas:** Módulo estándar de CPython `logging`, `sys`, `pathlib.Path`, `platformdirs`.

> [!INFO] Nota de Arquitectura:
> **Resistencia IO ("Fail-Safe"):** Es vital la implementación del constructor envoltorio de `OSError`. Debido a que esta herramienta se distribuye como un CLI empaquetado y puede heredar permisos estrictos dependientes del usuario del SO en Windows/Linux, un fallo de creación de un Log File jamás debe ocasionar un Kernel Panic que aborte la creación de Notas que sí es la función principal. Así, la observabilidad se vuelve "Best Effort".
