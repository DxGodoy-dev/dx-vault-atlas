### `main.py` (Note Doctor)

- **Ubicación Original:** `src/dx_vault_atlas/services/note_doctor/main.py`
- **Propósito Exhaustivo:** Sirve como el punto de entrada directo (Entrypoint) para invocar al servicio *Note Doctor* desde la línea de comandos principal (`CLI`). Aisla el manejo de errores fatal a nivel de sistema antes de iniciar la lógica de orquestación.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** Parámetros nulos. Se basa en que las banderas y argumentos ya fueron resueltos por el paquete invocador como `Typer` o la CLI.
    - **Process:**
      - Obtiene la configuración global (`get_settings()`).
      - Fabrica la app orquestadora llamando a `create_app(settings)` (cuyo patrón reside en `[[note_doctor_app.py.md]]`).
      - Invoca `.run()`.
      - Envuelve todo en un gran bloque `try/except`:
        1. Captura interrupciones de teclado (Ctrl+C) con `sys.exit(0)` (Finalización silenciosa limpia).
        2. Captura Excepciones base y las dirige a la bitácora `logger.exception()` para rastreo saliendo con código de error `sys.exit(1)`.
    - **Output:** 
      - Ejecución del proceso.
      - Salida (Exit Codes) a nivel OS.

- **Desglose Interno:**
    - Modulo base `main()` principal.
    - Guardamotores estándar `if __name__ == "__main__":`.

- **Dependencias:**
    - **Internas:** 
      - `[[note_doctor_app.py.md]]` (`create_app`)
      - `[[config.py]]` (`get_settings`)
      - `[[logger.py]]` (`logger`)
    - **Externas:** `sys`.

> [!INFO] Nota de Arquitectura:
> Abstraer `main.py` del núcleo funcional (`app.py`) facilita el empaquetamiento posterior si se decide usar un formato `.exe` (PyInstaller) o comandos en `pyproject.toml` al mantener un pipeline secuencial de instanciación con `sys.exit`.
