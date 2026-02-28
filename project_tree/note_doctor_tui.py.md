### `tui.py` (Note Doctor)

- **Ubicación Original:** `src/dx_vault_atlas/services/note_doctor/tui.py`
- **Propósito Exhaustivo:** Orquesta la experiencia de usuario interactiva para la curación de notas. En lugar de limitarse a informar errores, ensambla dinámicamente un asistente (Wizard TUI) a medida basándose exclusivamente en los campos faltantes o inválidos detectados por el validador, solicitando al usuario que introduzca los datos correctorios requeridos.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** 
      - Un objeto `ValidationResult` proveniente del escáner.
      - Importación de los prefabricados `TITLE_STEP`, `TEMPLATE_STEP`, `SOURCE_STEP`, etc., desde el módulo `NoteCreator`.
    - **Process:**
        ```mermaid
        graph TD
            A[Entrada: gather_fixes] --> B[Extraer missing/invalid fields]
            B --> C[Descartar campos no interactivos: dates, filenames]
            C --> D[Remover extraneous fields del scope]
            D --> E{¿Es info y falta status?}
            E -- Sí --> F[Auto-fill a To Read y quitar de missing]
            E -- No --> G
            F --> G[Ensamblar pasos: _build_steps]
            G --> H{¿Hay pasos necesarios?}
            H -- Sí --> I[Configurar WizardConfig y Lanzar interfaz gráfica Textual]
            H -- No --> J[Retornar diccionario de arreglos vacío / auto-completados]
            I --> K[Aplicar auto-fill post-wizard si se volvió InfoNote en el proceso]
            K --> J
        ```
    - **Output:** 
      - Un diccionario resolutivo (`dict[str, Any]`) con el formato `{ "campo": "nuevo_valor" }`.

- **Desglose Interno:**
    - `class DoctorTUI`: 
      - `gather_fixes`: Evalúa el reporte, filtra "falsos positivos" para la TUI (como fechas corruptas que deben arreglarse vía código o alias) y llama al constructor visual.
      - `_build_steps`: Genera una lista inyectando pasos prefabricados. Si el título está corrupto, usa el `stem` del archivo para ofrecer un título por defecto (Data recovery).
      - `_add_dependency_steps`: Regla estricta; si el "Template" es reparado o modificado en este Wizard, obliga a desplegar los pasos dependientes (`Source`, `Priority`, etc.) para asegurar consistencia tipo cascada.
      - `_filter_conditions_if_missing`: Quita sentencias condicionales (lambdas) de los `WizardStep` si el escáner afirma rígidamente que el campo está roto, forzando la obligatoriedad de respuesta en la pantalla de terminal.

- **Dependencias:**
    - **Internas:** 
      - `[[validator.py]]` (`ValidationResult`, `MODEL_MAP`).
      - `[[tui_steps.py]]` (Doble importación transversal desde NoteCreator).
      - `[[wizard.py]]` (`run_wizard`).
    - **Externas:** `dataclasses.replace`, `typing.Any`.

> [!INFO] Nota de Arquitectura:
> **Máxima Reutilización (DRY):** Este módulo importa y re-purpone (mediante `dataclasses.replace`) los exactos mismos componentes visuales `WizardStep` que fueron creados originalmente para el `Note Creator`, garantizando que la experiencia de selección (colores, menús) sea idéntica al crear una nota que al arreglar una.
