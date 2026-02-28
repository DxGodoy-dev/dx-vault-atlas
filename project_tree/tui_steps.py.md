### `tui_steps.py`

- **Ubicación Original:** `src/dx_vault_atlas/services/note_creator/tui_steps.py`
- **Propósito Exhaustivo:** Este archivo define de forma estática y declarativa todos los pasos (formularios/preguntas) que conforman el asistente interactivo (wizard) utilizado para crear una nueva nota. Emplea lógica condicional (`callbacks` en lambdas) para mostrar u ocultar ciertos pasos (como "Prioridad" o "Área") dependiendo del tipo de plantilla previamente seleccionada por el usuario.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** 
      - Importa valores predeterminados de `[[defaults.py]]`.
      - Importa enumeraciones de `[[enums.py]]`.
      - Durante la ejecución interactiva, el argumento `data` del Wizard (que contiene respuestas previas) es el "input" de las lambdas condicionales.
    - **Process:**
        ```mermaid
        graph TD
            A[TITLE_STEP] --> B[TEMPLATE_STEP]
            B --> C{¿Template NOT IN MOC, REF?}
            C -- Sí --> D[SOURCE_STEP]
            C -- No --> G
            D --> E[PRIORITY_STEP]
            E --> F{¿Template IN TASK, PROJECT?}
            F -- Sí --> H[AREA_STEP]
            F -- No --> I[STATUS_STEP]
            H --> I
            G{¿Template IN TASK, PROJECT?}
            G -- Sí --> H
            G -- No --> I
        ```
        A nivel de código, se declaran instancias de la clase `WizardStep`. Aquellas con el argumento `condition` usan una función anónima (lambda) para evaluar el diccionario vivo `data`. Si retorna `False`, ese paso es salteado en la interfaz.

    - **Output:**
        - Exporta la lista final de pasos `NOTE_CREATOR_STEPS` para ser consumida por el orquestador TUI.

- **Desglose Interno:**
    - `TITLE_STEP`: Instancia de tipo `input` para teclear el nombre de la nota.
    - `TEMPLATE_STEP`: Instancia tipo `select` para elegir el formato de nota (MOC, Info, Task, etc.). Carga las opciones desde `NoteTemplate`.
    - `SOURCE_STEP`: Tipo `select` para el origen de la info. Solo aparece si el template NO es MOC ni REF.
    - `PRIORITY_STEP`: Tipo `select`. Solo aparece si el template NO es MOC ni REF.
    - `AREA_STEP`: Tipo `select`. Solo aparece para TASK y PROJECT.
    - `STATUS_STEP`: Tipo `select` definiendo el progreso. Condicionado también a TASK y PROJECT. *(Ojo: aunque declarado, no está inyectado actualmente en la lista exportada).*
    - `NOTE_CREATOR_STEPS`: Lista Python estándar agrupando los objetos `WizardStep` en orden secuencial.

- **Dependencias:**
    - **Internas:** 
      - `[[defaults.py]]`
      - `[[enums.py]]`
      - `[[wizard.py]]` (`WizardStep`)
    - **Externas:** Ninguna

> [!BUG] Riesgo Potencial:
> El nodo/paso `STATUS_STEP` se define en el archivo (línea 67) con su propia lógica condicional, pero ha sido omitido en el array final exportado `NOTE_CREATOR_STEPS` (línea 79). Como resultado, la TUI jamás preguntará por el "Status" al crear un Task o Project, a menos de que exista un pipeline secundario o esto sea un despiste de desarrollo.
