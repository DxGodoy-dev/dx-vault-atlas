### `main.py` (Note Migrator)

- **Ubicación Original:** `src/dx_vault_atlas/services/note_migrator/main.py`
- **Propósito Exhaustivo:** Funciona como el punto de inicio desnudo y disparador (Entrypoint) para las llamadas a consola (`dxva migrate`). Centraliza la instanciación de dependencias (Variables de Entorno Globales) y encapsula el ciclo de vida de la ejecución mitigando cierres ruidosos (Crashes) por control+C, delegando el peso arquitectónico a `app.py`.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** Variables nulas, invocado desde un wrapper CLI (Typer) o script directo.
    - **Process:** Envuelve de forma segura el método `create_app(settings).run()` en un bloque `try/except`. Finaliza la ejecución ante `KeyboardInterrupt` o dirige excepciones serias al bitácora global de Python (`logger`).
    - **Output:** Códigos de control del flujo del SO (`sys.exit()`).

- **Desglose Interno:**
    - Método principal aislado `main()`.
    - Guarda estándar de ejecución `if __name__ == "__main__":`.

- **Dependencias:**
    - **Internas:** 
      - `[[note_migrator_app.py.md]]` (`create_app`)
      - `[[config.py]]` (`get_settings`)
      - `[[logger.py]]` (`logger`)
    - **Externas:** `sys`.

> [!INFO] Nota de Arquitectura:
> **Modularidad Exclusiva:** El hecho de aislar `.run()` detrás de fábricas de dependencias como `.create_app()` hace que el `Note Migrator` sea completamente "Testeable" mediante *Unit Tests*, ya que se puede instanciar el inyector con Paths ficticios o configuraciones Mock en vez de correr el ciclo de comando directo, previniendo daños a la data real durante el Testing.
