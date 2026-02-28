### `tui.py`

- **Ubicación Original:** `src/dx_vault_atlas/services/note_creator/tui.py`
- **Propósito Exhaustivo:** Este archivo se especializa en proveer el punto de entrada configurado de la interfaz gráfica de terminal (TUI) para recolectar los atributos necesarios en la creación de una nota. Básicamente empaqueta la lógica del "Wizard" interactivo importando los pasos requeridos y delegando en un orquestador TUI (`run_wizard`).

- **Modelo IPO (Input, Process, Output):**
    - **Input:** 
      - Parámetro: `settings` (`GlobalConfig`) proveniente del estado global del programa.
      - Importa la lista `NOTE_CREATOR_STEPS` que define todos los pasos formales de captura y sus interfaces.
    - **Process:**
        ```mermaid
        graph TD
            A[Entrada: run_tui] --> B[Crear Instancia WizardConfig]
            B --> C[Asignar NOTE_CREATOR_STEPS como steps]
            C --> D[Deshabilitar callback en on_complete]
            D --> E[Llamar al motor Textual run_wizard]
            E --> F[Fin y Retorno de Datos]
        ```
        1. Inicializa una instancia de `WizardConfig` configurada con un `title` visual, la constante global de pasos, un retardo minúsculo de salida y `on_complete = None` indicando que no debe ejecutar funciones extra de enruteo tras culminar exitosamente el wizard de captura.
        2. Ejecuta el core TUI compartiendo el config (`run_wizard(config)`).

    - **Output:**
        - Una tabla de diccionario (`dict[str, Any]`) donde las claves son las variables introducidas en la interfaz y el valor sus strings, booleans, enums elegidos. Puede devolver `None` de forma semántica si el usuario abortó prematuramente o de alguna manera saltó el wizard.

- **Desglose Interno:**
    - `run_tui(settings: GlobalConfig)`: Única función de nivel superior. Recibe las configuraciones globales, pero realmente las usa muy poco dado que la lógica delegada `run_wizard` es completamente desconectada en este punto.

- **Dependencias:**
    - **Internas:** 
      - `[[tui_steps.py]]` (`NOTE_CREATOR_STEPS`)
      - `[[config.py]]` (`GlobalConfig`)
      - `[[wizard.py]]` (`WizardConfig`, `run_wizard`)
    - **Externas:** `typing.Any`

> [!INFO] Nota de Arquitectura:
> Este archivo fomenta la arquitectura "Configuración sobre código" separando los pasos (en `tui_steps.py`) de la ejecución real mediante Inversión de Control delegando la aplicación TUI (Textual) dentro de `shared.tui.WizardApp`. Así `app.py` solo necesita llamar `run_tui()` y obtiene datos estructurados asincrónicamente.
