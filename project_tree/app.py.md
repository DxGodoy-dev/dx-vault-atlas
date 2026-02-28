### `app.py`

- **Ubicación Original:** `src/dx_vault_atlas/services/note_creator/app.py`
- **Propósito Exhaustivo:** Este archivo actúa como el orquestador principal del flujo de creación de notas (`Note Creator`). Su responsabilidad es coordinar los diferentes servicios y módulos (TUI interactiva, editor externo, procesador de plantillas y escritura a disco) para capturar los datos del usuario, generar el contenido de la nota y guardarla en el `vault_inbox`. Además, maneja el bucle de reintento/salida si algo sale mal o el usuario desea seguir creando notas.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** 
        - Instancias inyectadas: `settings` (`GlobalConfig`), `processor` (`NoteProcessor`), `writer` (`NoteWriter`).
        - Entrada del usuario recolectada a través de TUI (título, tipo, etc.) y contenido del cuerpo ingresado en el editor externo temporal.
    - **Process:**
        ```mermaid
        graph TD
            A[Inicio: run] --> B[Ejecutar TUI Wizard]
            B --> C{¿Datos válidos?}
            C -- No (Cancelado) --> D[Fin]
            C -- Sí --> E[Abrir Editor Externo Temporal]
            E --> F[Esperar Cierre de Editor]
            F --> G[Normalizar Título]
            G --> H[Fabricar Instancia de Nota via Factory]
            H --> I[Procesar/Renderizar Contenido via Processor]
            I --> J[Escribir Archivo en Disco via Writer]
            J --> K{¿Éxito?}
            K -- No (Error) --> L[Mostrar Error y Pausar]
            L --> D
            K -- Sí --> M[Ejecutar Result TUI]
            M --> N{¿Reintentar?}
            N -- Sí --> B
            N -- No --> D
        ```
        1. Se ejecuta el TUI Wizard (`run_tui`) interactivo para obtener los metadatos de la nota. Si es cancelado, finaliza.
        2. Llama a `_get_editor_content()` que abre el editor de sistema en un archivo temporal bloqueante para registrar el contenido del cuerpo. Lee el contenido y borra el temporal.
        3. El título es saneado utilizando `TitleNormalizer.normalize()`.
        4. Construye el objeto modelo usando `NoteFactory.create_note(...)`.
        5. Renderiza el texto final de la nota utilizando `processor.render_note(...)` y la plantilla correspondiente.
        6. Escribe el archivo en disco (`writer.write(...)`) en la carpeta `vault_inbox`.
        7. Muestra el resultado (`run_result_tui`) y evalúa la opción de volver a iniciar (Retry).
        
    - **Output:**
        - Un archivo `.md` generado físicamente en la carpeta Inbox (`vault_inbox`) de Obsidian.
        - Llamadas secundarias a las terminales (impresión con `rich` y `textual`).

- **Desglose Interno:**
    - `Class NoteCreatorApp`: 
        - Contiene el flujo orquestado completo con dependencias inyectadas.
    - `NoteCreatorApp.run()`: 
        - Contiene el bucle principal `while True` que maneja todo el pipeline descrito en el diagrama.
    - `NoteCreatorApp._get_editor_content()`:
        - Abre un `NamedTemporaryFile`, llama a `SystemEditor.open_file()`, recupera el texto y elimina el temporal de manera segura.
    - `create_app(settings, show_header)`:
        - Función constructora (Factory pattern) que arma la aplicación inyectando explícitamente `TemplatingService()`, `NoteProcessor()` y `NoteWriter()`.

- **Dependencias:**
    - **Internas:** 
      - `[[factory.py]]` (`NoteFactory`)
      - `[[processor.py]]` (`NoteProcessor`)
      - `[[writer.py]]` (`NoteWriter`)
      - `[[templating.py]]` (`TemplatingService`)
      - `[[tui.py]]` (`run_tui`)
      - `[[title_normalizer.py]]` (`TitleNormalizer`)
      - `[[config.py]]` (`GlobalConfig`)
      - `[[system_editor.py]]` (`SystemEditor`)
      - `[[logger.py]]` (`logger`)
      - `[[result_app.py]]` (`run_result_tui`)
      - `[[console.py]]` (`console`)
    - **Externas:** `tempfile`, `contextlib`, `pathlib`, `rich.prompt.Prompt`

> [!INFO] Nota de Arquitectura:
> Este módulo implementa Inyección de Dependencias a través de un constructor factory (`create_app`), separando limpiamente la UI (`tui.py`), la lógica de renderizado (`processor.py`) y el acceso a disco (`writer.py`, `system_editor.py`).

> [!BUG] Riesgo Potencial:
> El manejo de excepciones en `run()` detiene la ejecución actual para mostrar un mensaje rojo y hace un `return` global del flujo, rompiendo el ciclo `while True` en caso de fallo, lo cual implica que el usuario debe volver a lanzar el comando CLI entero si hay un pequeño error de escritura en disco, en lugar de permitir un retry sin perder el estado/contenido.
