### `cli.py` (Root Module)

- **Ubicación Original:** `src/dx_vault_atlas/cli.py`
- **Propósito Exhaustivo:** Es el Enrutador Transaccional Global (Global Router). Funciona como el cerebro de conexión con el exterior, traduciendo los teclazos del usuario en la consola (`dxva [comando]`) hacia la instanciación arquitectónica de los submódulos profundos de la aplicación. Además es responsable de la protección de barrera superior (Main Catch) y de forzar el Bootstrapping preventivo.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** Variables y Banderas `sys.argv` alimentadas a las firmas de método mediante inyecciones de dependencia de `Typer` (ej. `--debug-mode`).
    - **Process:**
      - **Callback Estático:** Registra la función `@app.callback()` que se ejecutará _antes_ que cualquier comando. Ésta despacha `ensure_config_exists()` del `core/bootstrap.py` para obligar al usuario a configurar su Vault si es su primera vez usando el programa.
      - **Lazy Loading:** Las importaciones de librerías pesadas como Textual o Pydantic se encierran dentro del scope local de cada función del comando (`def note_doctor()`). Así, si el usuario solo llama a `dxva config show`, Python no gasta milisegundos importando motores TUI enteros que no usará.
      - **The Main Catch:** Envuelve la invocación base `app()` dentro de un macro `try...except Exception`. Esta es la malla definitiva protectora (Skill 06): Si un error estalla sorpresivamente desde las profundidades del código en Runtime, este buje lo acorrala.
    - **Output:** 
      - Ejecución delegada a los orquestadores (App).
      - En caso de Crash Crítico: Guarda silenciosamente el Traceback real en `logger.critical(exc_info=True)` y luego avienta un bonito e inofensivo Panel Rojo al usuario terminal indicándole dónde abrir su archivo `.log` (`logger.handlers[0].baseFilename`), finalizando el programa con `sys.exit(1)`.

- **Desglose Interno:**
    - Grupo `Typer` Principal (`app`) y Subgrupo (`config_app`).
    - Comandos de Configuración: `show`, `edit`, `reset`.
    - Comandos de Servicios Base: `note`, `migrate`, `doctor`.
    - Entrypoint de Sistema Estricto: `main()`.

- **Dependencias:**
    - **Internas:** Todas las rutas expuestas (`[[note_creator_app.py.md|note_creator.create_app]]`, `[[note_doctor_main.py.md|note_doctor.main]]`, `[[note_migrator_app.py.md|note_migrator.create_app]]`, `[[shared_logger.py.md|logger]]`, `[[config_editor.py.md|ConfigEditor]]`, `[[bootstrap.py.md|ensure_config_exists]]`).
    - **Externas:** `typer`, `rich`, `sys`, `json`.

> [!INFO] Nota de Arquitectura:
> **Resistencia Estética de Typer:** Gracias a que se invoca `install_rich_traceback(show_locals=False)` en la cabecera, si ocurre un colapso antes de llegar a los bucles Asíncronos, la impresión en pantalla del stack de errores en vez de ser texto blanco plano aburrido se dibujará con colores hermosos delineando cada pieza del error.
