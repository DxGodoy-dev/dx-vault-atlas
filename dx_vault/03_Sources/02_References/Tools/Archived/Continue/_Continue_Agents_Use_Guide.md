---
tags:
- workflow
- ai
- productividad
- python
- solid
source: ia
created: 24-01-2026
updated: 2026-02-09 02:05:06.658235
version: '1.0'
type: note
---
## Flujo de Trabajo con Agentes de IA (Continue.dev)

Este manual define el uso operativo del entorno para maximizar la productividad de un desarrollador **High Junior** con mentalidad de producto, optimizando el uso de modelos según su rol y capacidad.

### 1. Modelos por Rol Operativo

| Tarea | Modelo Sugerido | Comando / Interfaz |
| :--- | :--- | :--- |
| **Arquitectura y SOLID** | Gemini 1.5 Pro | Chat lateral (`@codebase`) |
| **Refactorización Rápida** | Gemini 1.5 Flash | `Ctrl + I` (Inline Edit) |
| **Escritura de Código** | Codestral / Codeium | Tab-Autocomplete |
| **Depuración de Errores** | Gemini 1.5 Flash | `@terminal` en Chat |

### 2. Comandos de Contexto Vitales

El uso de `@` permite inyectar información precisa al modelo, reduciendo alucinaciones y respetando la **Directiva de Ingeniería**:

* **`@codebase`**: Analiza todo el proyecto. Úsalo para preguntar: *"¿Cómo puedo implementar un nuevo servicio siguiendo el patrón de los actuales?"*
* **`@file`**: Enfoca la atención en archivos específicos (ej. `models.py` y `schemas.py`) para asegurar consistencia en **Pydantic**.
* **`@terminal`**: Envía el historial de la consola. Ideal para resolver errores de importación o fallos en `pytest`.
* **`@docs`**: Referencia documentación oficial externa sin salir de VS Code.

### 3. Aplicación de la Directiva de Ingeniería

Para mantener el estándar de calidad y alcanzar la meta de **$100/semana**, se deben seguir estos micro-pasos en cada interacción:

1.  **Validación de Tipos**: Si la IA genera código sin tipos, usar `Ctrl + I` con la instrucción: *"Aplica Strict Type Hinting"*.
2.  **Desacoplamiento**: Ante funciones extensas, pedir: *"Refactoriza usando Guard Clauses y extrae lógica a métodos privados"*.
3.  **Testing**: Antes de dar por finalizada una tarea, usar el chat: *"Genera los unit tests en la carpeta /tests usando dependency injection"*.

### 4. Atajos de Teclado (Productividad)

* **`Ctrl + L`**: Abre/Cierra el panel de chat.
* **`Ctrl + I`**: Edición rápida sobre el código seleccionado.
* **`Ctrl + Shift + R`**: (Custom) Ejecuta la regla de validación SOLID definida en el config.