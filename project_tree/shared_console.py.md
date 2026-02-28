### `console.py` (Shared)

- **Ubicación Original:** `src/dx_vault_atlas/shared/console.py`
- **Propósito Exhaustivo:** Una abstracción global de I/O que homogeniza la Interfaz de Terminal en todo el aplicativo. Concentra y exporta funciones embellecedoras de impresión (`Rich`) y contenedores interactivos de encuestas (`Questionary`), actuando como la "tarjeta de video/teclado" para comandos CLI aislados o volcados globales antes de escalar a la interfaz gráfica pesada (TUI).

- **Modelo IPO (Input, Process, Output):**
    - **Input:** Llamadas de funciones internas con cadenas, enums o booleanos (`show_header`, `success_message`, `choose_enum`, `confirm`).
    - **Process:**
      - Encapsula excepciones de interrupción de Teclado, envolviendo *Ctrl+C* (`KeyboardInterrupt`) y *q* o *Ctrl+Q* (`UserQuitError` custom).
      - Parsea Enums de Python para mostrar en listados amigables capitalizando títulos (ej: quita el sufijo explícito `.md` de visualización para que "project.md" sea visible como "Project").
      - Fuerza estilos `Rich` uniformes mediante tokens inyectados como `[bold cyan]` en cada advertencia de Error o Éxito.
    - **Output:** Pixeles terminales formateados interactivamente, retornos bloqueantes resolviendo tipos `Enums` literales u strings tipeados.

- **Desglose Interno:**
    - Objeto Abierto `console = Console()` (Usado globalmente por todos los módulos, i.e., Note Doctor y Note Migrator para sus reportes).
    - Estéticos: `MENU_STYLE` pre-formatea los punteros interactivos de questionary.
    - Excepciones: `UserQuitError`.
    - Decoradores/UI: `show_header()`, `success_message()`, `error_message()`, `show_preview()`.
    - Interactivos de Bloqueo: `query()`, `choose_enum()`, `confirm()`.

- **Dependencias:**
    - **Internas:** Ninguna acoplada a negocio.
    - **Externas:** `rich.console`, `rich.panel`, `questionary`.

> [!INFO] Nota de Arquitectura:
> Este archivo `shared/console.py` es el canon operativo actual. Se puede confirmar que el archivo `services/note_creator/services/console.py` evaluado anteriormente es una pieza muerta / "Legacy Code" sin limpiar, dado que toda la lógica ha sido subsumida y mejorada globalmente en este archivo compartido.
