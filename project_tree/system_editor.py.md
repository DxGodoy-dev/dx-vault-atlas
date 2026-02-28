### `system_editor.py` (Shared Core)

- **Ubicación Original:** `src/dx_vault_atlas/shared/core/system_editor.py`
- **Propósito Exhaustivo:** El puente interactivo hacia el Sistema Operativo subyacente del usuario final. Tras haber creado el andamiaje del metadato (YAML), el hilo de Python no permite al usuario teclear en la terminal cómodamente sus artículos; por lo que el `SystemEditor` despacha asíncronamente un entorno gráfico (como VS Code, Vim o Notepad) con el archivo abierto, congelando la actividad interna de la App hasta que el externo se cierra informando finalización exitosa.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** La ruta física del `.md` inyectada (`file_path`) y una variable alfabética de preferencia del comando del editor a usar (`editor_cmd` proveniente de la _settings_).
    - **Process:**
      - Determina al host analizando `os.name == "nt"` (Windows) para designar editores default (`vim` en Unix, `notepad` en Win).
      - Aplica jerarquía de carga de configuración (`Or`): Input explícito -> Env Var `DXVA_EDITOR` -> OS Env Var `$EDITOR` -> Default.
      - Divide la cadena lexicamente (ej: si el usuario pone `'code --wait'`, `shlex.split` lo convierte en `['code', '--wait']`).
      - Spawnea a hilo separado vía OS usando `subprocess.check_call()`. Al usar `check_call`, la aplicación se duerme a la espera y no continúa.
      - En caso de Fallo Crítico (ej. el Editor declarado no exista), usa `os.startfile()` silencioso el cual delega a la aplicación default asignada por Windows Explorer.
    - **Output:** 
      - Pantalla Gráfica OS de terceros.
      - Retorno Oculto sin Datos extra, habilitando que la App original cierre. Lanza RuntimeError si ambos fallan.

- **Desglose Interno:**
    - Variable flag `IS_WINDOWS`.
    - `class SystemEditor` y su utilidad `@staticmethod open_file()`.

- **Dependencias:**
    - **Internas:** Ninguna.
    - **Externas:** `os`, `shlex`, `subprocess`, `pathlib.Path`.

> [!BUG] Riesgo Potencial:
> El comando `shlex.split(cmd_str, posix=not IS_WINDOWS)` está diseñado para funcionar bien extrayendo sentencias complejas. Sin embargo, en Windows muchos usuarios tienen comandos con espacios puros ej. `C:\Program Files\editor`. Si no está debidamente envuelto en comillas por el usuario en su settings `.json`, esto rebanará el Path causando un `FileNotFoundError` inmediato escalando al Dropback de `os.startfile`.
