### `widgets.py` (Shared TUI)

- **Ubicación Original:** `src/dx_vault_atlas/shared/tui/widgets.py`
- **Propósito Exhaustivo:** Una caja de herramientas y herencias (Subclassing) de los bloques de Construcción visual de `Textual`. Abstraen y personalizan el comportamiento de nodos puramente visuales y de recolección de entrada, dotando de ergonomía de primer nivel a listas e inputs textuales en un terminal sin necesidad de ensuciar los archivos orquestadores con este polvillo repetitivo. Destaca fuertemente por proveer navegación Estilo-VI y generadores Mágicos Enum-To-GUI.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** Referencias pasadas por componentes Padres (Listas de Enums de Negocio, strings `id_prefix`).
    - **Process:**
      - Extiende la clase `OptionList` nativa (El contenedor base que procesa encuestas visuales con selectores up/down interactivos) llamándola `VimOptionList`, inyectando la reaccionalidad mágica a las letras de navegación de programador clásicas "j" y "k", previniendo que el usuario deba sacar su mano del teclado central para ubicar las flechas físicas.
      - Componentizo dinámico: La fábrica mágica de factorías `create_vim_option_list` itera clases `Enum` subyacentes del _Business Layer_ de Python puras desarmándolas para montar dinámicamente cada iteración en formato `Option(Text.from_markup())` respetando minúsculas e indicadores de `(Default)` visuales.
      - Crea la clase histórica de rastro pasivo `StepDone(Static)` que es escupida al historial visual cada vez que el usuario confirma una elección en los listados interactivos.
    - **Output:**  Objetos Componentes Listos del Virtual DOM.

- **Desglose Interno:**
    - `VimOptionList`: Herencia directa con bindings customizados.
    - `StepDone`: Generador HTML-like simplificado.
    - Emisarios de fábricas funcionales: `create_enum_options`, `create_vim_option_list`.

- **Dependencias:**
    - **Internas:** `[[shared_console.py.md|console.py]]` (`format_enum_label`).
    - **Externas:** `textual.binding.Binding`, `textual.widgets.OptionList`, `textual.widgets.Static`, `rich.text`.

> [!INFO] Nota de Arquitectura:
> **Desacoplamiento Visual/Negocio:** Centralizar cómo los Enums nativos de Python de los módulos pesados (i.e. Pydantic Models) se mapean visualmente a `VimOptionList` es un patrón arquitectónico crítico. Impide que la lógica de renderizado inunde los modelos estrictos de validación, y si Obsidian un día cambia un Tipo de Nota o se altera la colección de Tags de Enum, este generador dibujará dinámicamente listas más largas automáticamente y las auto-highlighteará en verde para el TUI de Python.
