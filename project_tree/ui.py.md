### `ui.py` (Shared)

- **Ubicación Original:** `src/dx_vault_atlas/shared/ui.py`
- **Propósito Exhaustivo:** Funciona estrictamente como un "Módulo Fachada" (Facade Pattern) y re-exportador. Sirve para proveer retrocompatibilidad arquitectónica a archivos que todavía hacen `import dx_vault_atlas.shared.ui`, redirigiendo todo el tráfico estructural hacia su verdadero hogar unificado en el nuevo archivo `console.py`.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** N/A (Solo sentencias de importación teórica).
    - **Process:** Extrae los tokens `show_header`, `success_message`, `UserQuitError`, etc., desde `shared.console`.
    - **Output:** Expone las herramientas hacia fuera definiendo afirmativamente la lista `__all__`.

- **Desglose Interno:**
    - Lista `__all__`: Declara las propiedades públicas explícitamente compartidas del módulo.

- **Dependencias:**
    - **Internas:** `[[shared_console.py.md|console.py]]`.
    - **Externas:** N/A.

> [!WARNING] Deuda Técnica:
> Este archivo representa estrictamente un ancla de Retrocompatibilidad (Backwards Compatibility shim). Si el proyecto realiza una refactorización de todas las importaciones `from shared import ui` reemplazándolas por `from shared import console`, este archivo `ui.py` puede ser eliminado por completo sin pérdida de funcionalidad.
