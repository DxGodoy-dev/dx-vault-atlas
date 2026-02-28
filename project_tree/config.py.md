### `config.py` (Shared)

- **Ubicación Original:** `src/dx_vault_atlas/shared/config.py`
- **Propósito Exhaustivo:** Administrador centralizado de la configuración de toda la aplicación. Aisla el manejo de variables de entorno y archivos persistentes del Sistema Operativo usando estándares XDG. Define el modelo estricto de los parámetros críticos del ecosistema como la ruta a la bóveda de Obsidian (`vault_path`) y las reglas de inyección.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** 
      - Variables de entorno (Prefijadas con `DX_`, ej: `DX_VAULT_PATH`).
      - Archivo persistente en disco `~/.config/dx-vault-atlas/config.json`.
    - **Process:**
      - Utiliza `pydantic-settings` para fusionar las fuentes (Dando prioridad a las Variables de Entorno sobre el JSON).
      - Ejecuta validaciones defensivas usando `validate_directory` de `paths.py` para asegurar que el `vault_path` no solo sea un string, sino un directorio que exista orgánicamente en el disco.
      - Evita Lectura/Escritura reiterada en disco guardando la carga en RAM mediante el singleton estático `@lru_cache()`.
      - Proporciona a toda la aplicación una vía homogeneizada mediante getter `get_settings()`.
    - **Output:** Objeto Instanciado `GlobalConfig` que garantiza que sus atributos están 100% disponibles y sanitizados.

- **Desglose Interno:**
    - `class GlobalConfig(BaseSettings)`: El "Data Schema" estricto. (Define `vault_path`, `vault_inbox`, `editor`, `field_mappings`).
    - `class ConfigManager`: El "I/O Controller". Maneja la persistencia XDG (`user_config_dir`) llamando a `.load()` (parsea JSON) o `.save()` (vuelca estado local a JSON y limpia caché).
    - Excepciones: `ConfigNotFoundError`.
    - Funciones Helper Singleton: `get_config_manager`, `get_settings`.

- **Dependencias:**
    - **Internas:** 
      - `[[logger.py]]`
      - `[[paths.py]]` (Para validar directorios físicos).
    - **Externas:** `pydantic_settings`, `pydantic`, `platformdirs` (Resuelve Cross-Platform Paths), `functools.lru_cache`, `json`.

> [!INFO] Nota de Arquitectura:
> **XDG Compliance:** Al utilizar `platformdirs.user_config_dir()`, este archivo jamás contamina el directorio Home (`~`) del usuario con carpetas visibles, un patrón sucio común en CLI scripts, sino que respeta los lugares correctos del sistema (`%APPDATA%` en Windows, `~/.config/` en Linux y `~/Library/Application Support/` en MacOS).
