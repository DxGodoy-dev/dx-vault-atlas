### `wizard_app.py` (Shared TUI)

- **Ubicación Original:** `src/dx_vault_atlas/shared/tui/wizard_app.py`
- **Propósito Exhaustivo:** El Orquestador Físico Universitario (Motor Creador Asíncrono de Interfaz). Recibe un plano inerte (`WizardConfig`) y lo convierte en una aplicación interactiva viva mediante generación procedimental del Modelo de Objetos de Texto (DOM) de `Textual`. Es una Máquina de Estados Finita (Finite State Machine) que maneja paso a paso el historial de encuestas y limpia la consola a medida que avanza.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** Interacción física con el teclado y señales de terminación de Widget (ej. `OptionList.OptionSelected`).
    - **Process:**
      - Hereda las reglas CSS de `BaseApp`.
      - Mantiene el trackeo de estado actual iterando sobre `self.step_index`.
      - Refresca en vivo el listado de preguntas reevaluando `_compute_active_steps()`, decidiendo si las ramas condicionales siguen vigentes en cada nueva respuesta.
      - **Montaje al vuelo:** Limpia el contenedor general `self.clear_wizard()`. Para los pasos ya contestados inserta pasivamente un widget `StepDone`. Para el paso activo extrae el tipo (`select` o `input`) y llama a las fábricas mágicas de `[[widgets.py]]` inyectando focalización a la nueva instancia `self.wizard.mount()`.
      - Captura las submisiones (tecla Enter), lo guarda en memoria `self.data` y dispara `_advance()`.
    - **Output:** Al saturar todos los pasos, dispara las funciones "Side-Effect" colgadas en `config.on_complete`, destruye el DOM Textual matando la sesión vía `self.exit()` y devuelve un Diccionario limpio con el historial total de respuestas `dict[str, Any]` recuperando la vida de la línea de comandos ordinaria.

- **Desglose Interno:**
    - `WizardApp(BaseApp)`: App principal Textual.
      - Eventos Reactivos: `on_input_submitted()`, `on_option_list_option_selected()`.
      - Flujogramas internos: `_show_current_step()`, `_compute_active_steps()`, `_complete()`.
    - Exposición: `run_wizard()`.

- **Dependencias:**
    - **Internas:** 
      - `[[shared_tui_app.py.md|BaseApp]]`
      - `[[widgets.py]]` (`StepDone`, `create_vim_option_list`)
      - `[[wizard.py]]` (`WizardConfig`)
    - **Externas:** `textual`, `typing.Any`.

> [!INFO] Nota de Arquitectura:
> **Dynamic Type Resolver:** Al enfrentarse a subwidgets Enum complejos (`step.step_type == "select"`), este script contiene un ingenioso bloque `try/except` que mapea reflexivamente y asegura que Textual UI ilumine correctamente la variable *Default* definida por la clase de negocio incluso si este fue declarado erróneamente en el _DataClass_.
