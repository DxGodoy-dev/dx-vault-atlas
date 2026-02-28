### `app.py` (Shared TUI)

- **Ubicación Original:** `src/dx_vault_atlas/shared/tui/app.py`
- **Propósito Exhaustivo:** Sirve como la súper-clase base obligatoria (Contenedor Abstracto) para todas las interfaces gráficas TextualTUI del sistema (Como el recolector de notas de Note Creator o la de Note Doctor). Garantiza la herencia unificada de un layout fundamental (Cabecera, Cuerpo y Pie de página) y estandariza los atajos de teclado globales.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** Señales de Teclado declaradas en `BINDINGS`.
    - **Process:**
      - Inyecta el modelo de Caja Visual CSS asíncrona de Textual.
      - Construye el esqueleto HTML-like mediante `compose()` estableciendo un `#header-panel` superior, un contenedor padre vacío `<Vertical id="wizard">` y un pie de página.
      - Mapea funciones a los Keyboard Shortcuts (`F11` -> `action_toggle_maximize()`, `Ctrl+P` -> `ThemeManager.cycle_theme()`).
      - Sobrescribe la paleta de comandos nativa de Textual (`get_system_commands()`) para borrar botones inncesarios e inyectar acciones contextuales como "Skip".
    - **Output:** Árbol DOM interactivo renderizado en memoria de la Terminal usando buffer alterno (para no destruir la consola de fondo del usuario una vez que el programa termine).

- **Desglose Interno:**
    - `class BaseApp(App[None])`: Herencia directa del loop asyncio de Textual.
    - Propiedad `wizard`: Exponer el contenedor central para rápido acceso y mutación de DOM desde los hijos.

- **Dependencias:**
    - **Internas:** `[[theme.py]]` (Para recarga dinámica CSS).
    - **Externas:** `textual.app`, `textual.containers`, `textual.widgets`.

> [!INFO] Nota de Arquitectura:
> **Puntos de Inversión de Control:** Definir abstractamente `def action_skip(self)` pero dejándolo como `pass` empuja un patrón Polimórfico limpio: Permite que el framework registre el botón en la UI universal, pero cada submódulo especializado decide qué significa realmente "Skip" en su contexto.
