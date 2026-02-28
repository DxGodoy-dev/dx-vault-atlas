### `console.py`

- **Ubicación Original:** `src/dx_vault_atlas/services/note_creator/services/console.py`
- **Propósito Exhaustivo:** Administra la I/O (Input/Output) a nivel de terminal cuando no se está operando dentro del bucle del entorno TUI principal (Textual). Proporciona herramientas de interfaz de línea de comandos iterativas (CLI) embellecidas usando las librerías `questionary` y `rich` para mostrar mensajes de error coloreados y hacer preguntas de teclado simples (query, choose, confirm).

- **Modelo IPO (Input, Process, Output):**
    - **Input:** 
      - Strings puros enviados como el título de la pregunta (`prompt_text`).
      - Tipos genéricos herederos de Enum para la selección de opciones.
    - **Process:**
      - Aplica silenciosamente un estilo visual en cyan llamado `MENU_STYLE` configurado localmente.
      - Para selecciones de Enum, ejecuta `_format_enum_label` que sanea el texto (ej. quita `.md` y pone la primera letra mayúscula).
      - Invoca a las primitivas de `questionary` para bloquear el hilo hasta que el usuario responda.
      - Si el usuario interrumpe intencionalmente (p. ej. Ctrl+C provoca que `questionary` retorne None), la clase lo intercepta y lanza un `KeyboardInterrupt` para cancelar el flujo padre.
    - **Output:**
      - El valor crudo insertado (`str`), la propiedad `Enum` (`_E`) elegida, o el booleano (`bool`) confirmado. Imprime texto coloreado a `stdout`.

- **Desglose Interno:**
    - Variable Global `console`: Instancia abierta lista de `Rich.Console` usada externamente para imprimir logs visuales (ej. errores en `app.py`).
    - `MENU_STYLE`: Configuración de tokens de colores para `questionary`.
    - Función privada `_format_enum_label`: Trata el texto para la UI de consola.
    - `class ConsoleInterface`: Contenedor estático para:
      - `@staticmethod query()`: Emula un `input()`.
      - `@staticmethod choose_enum()`: Despliega una lista navegable de flechas en CLI.
      - `@staticmethod confirm()`: Pregunta `Y/n`.

- **Dependencias:**
    - **Internas:** Ninguna (Genérica).
    - **Externas:** `rich.console`, `questionary`.

> [!WARNING] Deuda Técnica:
> Viendo cómo `[[app.py]]` y la arquitectura actual utilizan la librería externa basada en Textual `[[tui.py]]` para la captura de variables en *Note Creator*, este módulo de `questionary` parece haber quedado obsoleto o al menos desplazado ("Dead Code / Legacy Flow") como método de entrada principal, conservándose quizá únicamente por la instancia utilitaria `console.print()` para excepciones.
