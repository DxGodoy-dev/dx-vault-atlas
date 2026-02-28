### `theme.py` (Shared TUI)

- **Ubicación Original:** `src/dx_vault_atlas/shared/tui/theme.py`
- **Propósito Exhaustivo:** Administrador Singleton de la Estética y los Cascading Style Sheets (CSS) en toda la interfaz interactiva. Importa e implementa a nivel atómico el popular sistema de diseño de paletas de color `Catppuccin`, permitiendo al usuario mutar instantáneamente todo el colorimetraje del programa ciclando presettups sin recargar el ejecutable.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** Solicitudes estáticas al método utilitario `ThemeManager.get_css()` o `cycle_theme()`.
    - **Process:**
      - Contiene un mega-diccionario estricto (`THEMES`) de constantes Hardcodeadas mapeando Claves Semánticas de Catppuccin (`base`, `surface0`, `blue`, `mauve`) a sus valores HEX físicos.
      - Guarda un índice cíclico en memoria de Clase (`current_theme: ClassVar[str] = "mocha"`), saltando de Mocha -> Latte -> Frappe -> Macchiato.
      - Ejecuta una interpolación de String enorme de Python F-Strings inyectando todos los colores HEX crudos en una mega plantilla pura CSS (Que rige elementos visuales estrictos de Textual UI, e.g. `OptionList > .option-list--option`).
    - **Output:** Salida gigantesca de String plano CSS, absorbido y compilado por el Motor Base de TextualTUI en vivo.

- **Desglose Interno:**
    - Mega `dict`: `THEMES` y arreglo de orden `THEME_ORDER`.
    - Modulo estricto `ThemeManager`.
      - `get_colors()`, `cycle_theme()`, `get_css()`.

- **Dependencias:**
    - **Internas:** Ninguna (Independiente total, Hoja del árbol de dependencias).
    - **Externas:** Ninguna (Agnóstico).

> [!INFO] Nota de Arquitectura:
> **Dynamic Hot Reloading CSS:** En lugar de leer un archivo oculto `.css` local desde disco (lo cual causaría frágiles caóticas si este paquete es distribuido compilado o via PyPI), inyectar absolutamente todas las reglas estéticas desde variables F-String de Python en la ejecución unifica el ecosistema. Esto permite que el atajo global de teclado (Ctrl+P) dispare `cycle_theme` para mutar los Hexes e instantáneamente re-renderizar los pixeles.
