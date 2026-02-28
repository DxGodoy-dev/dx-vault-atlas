### `config_wizard.py` (Shared TUI)

- **Ubicación Original:** `src/dx_vault_atlas/shared/tui/config_wizard.py`
- **Propósito Exhaustivo:** Funciona como el menú ineludible de Configuración de Primera Vez (First-Run Experience). Emplea `Rich` para realizar tres preguntas existenciales forzosas (`vault_path`, `vault_inbox`, `editor_cmd`) sin las cuales ninguna otra capa de la aplicación puede operar de manera segura.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** Rutas en texto y selecciones literales.
    - **Process:**
      - Despliega paneles estilizados de bienvenida.
      - Aísla la verificación de directorios en un Prompt Cíclico `_prompt_directory`: hasta que el host OS no verifique que la ruta proveída es un directorio vivo y existente, el usuario se queda atascado imposibilitando guardar variables locas o dañadas.
      - Propone la carpeta `Obsidian/Vault` y la subcarpeta `/Inbox` en la home del usuario dinámicamente como default.
    - **Output:** Un DTO limpio `GlobalConfig` instanciado o `None` si la captura fue interrumpida.

- **Desglose Interno:**
    - `run_setup_wizard()`: Orquestador visual lineal "Step 1/3, 2/3, 3/3".
    - Excepciones toleradas: Atrapa el cancelamiento por teclado.

- **Dependencias:**
    - **Internas:** 
      - `[[config.py]]` (`GlobalConfig`)
      - `[[paths.py]]` (`validate_directory`)
    - **Externas:** `rich.console`, `rich.panel`, `rich.prompt`, `pathlib.Path`.

> [!INFO] Nota de Arquitectura:
> Aislar el `run_setup_wizard` de `config_editor` es una gran elección, ya que el Wizard es un procedimiento lineal dependiente de fallos (tiene que acabar sí o sí secuencialmente), mientas que el Editor es un modelo interactivo radial de exploración infinita.
