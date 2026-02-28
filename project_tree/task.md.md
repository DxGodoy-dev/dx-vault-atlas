### `task.md`

- **Ubicación Original:** `src/dx_vault_atlas/services/note_creator/templates/task.md`
- **Propósito Exhaustivo:** Asset Jinja asignado estructuralmente para definir Entidades Accionables atómicas (`TaskNote`). Funciona de manera paralela a Project, pero sin la sobrecarga de campos temporales para mantener la interfaz ligera en tareas del día a día.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** Objeto tipado asimilable a `TaskNote` inyectando propiedades como `area`, `status`, `priority`.
    - **Process:** Copiado directo al formato de salida.
    - **Output:** Texto renderizado.

- **Desglose Interno:**
    - Adopta el grupo `WorkflowNote` inyectando `area` y `status`.
    - Exclusivo de esta plantilla: El campo `deadline:` posicionado al final para un ingreso rápido de la meta límite sin rellenar campos de inicio (`start`) o término (`outcome`).

- **Dependencias:**
    - **Internas:** `[[note.py]]` (`TaskNote`).
    - **Externas:** N/A.
