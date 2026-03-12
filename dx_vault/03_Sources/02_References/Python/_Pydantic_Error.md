---
version: '1.0'
type: ref
title: "_Pydantic_Error"
created: 2026-02-09 02:08:33.857228
updated: 2026-02-09 02:08:33.857228
aliases:
- _Pydantic_Error
tags: []
---
### 1. Filosofía de Validación: Single Source of Truth
En una arquitectura profesional, la validación no es solo "revisar datos", es asegurar que la representación en memoria coincida exactamente con la intención del negocio. Al utilizar `model_config = {"extra": "forbid"}`, transformamos el modelo de una simple bolsa de datos a un **contrato estricto**.

### 2. Jerarquía Semántica vs. Técnica
La estructura se organiza en niveles para respetar el principio *DRY* y la coherencia lógica:

* **Nivel 1: BaseNote (El ADN)**: Contiene los metadatos que toda nota en *Obsidian* debe poseer (título, fecha, tipo). Es el punto de control para la configuración global del modelo.
* **Nivel 2: WorkflowNote (La Abstracción de Estado)**: No todas las notas son tareas, pero todas las tareas y proyectos comparten un "ciclo de vida" (status, área). Crear este nivel intermedio evita la redundancia sin forzar una herencia antinatural entre tareas y proyectos.
* **Nivel 3: Modelos de Implementación**: `TaskNote` y `ProjectNote` solo definen sus campos exclusivos (ej. *deadline* o *outcome*).

### 3. El Guardián de la Integridad: Extra Forbid
Activar `extra: "forbid"` en el `BaseNote` tiene tres propósitos críticos:
1.  **Detección de Typos**: Evita que un error al escribir el frontmatter (ej. `statuss: todo`) pase desapercibido.
2.  **Sincronización con Templates**: Garantiza que si el modelo cambia, tus plantillas de Markdown también deban actualizarse.
3.  **Seguridad de Dominio**: Impide que datos malformados o inyectados contaminen la lógica de la aplicación.

```python
class BaseNote(BaseModel):
    model_config = {"extra": "forbid"}
    # ADN común aquí

class WorkflowNote(BaseNote):
    status: NoteStatus
    area: NoteArea

class TaskNote(WorkflowNote):
    deadline: Optional[datetime] = None
```