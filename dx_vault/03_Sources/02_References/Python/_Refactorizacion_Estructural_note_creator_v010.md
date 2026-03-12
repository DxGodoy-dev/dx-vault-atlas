---
tags: []
source: ia
priority: 2
created: 2026-02-04
updated: 2026-02-09 02:05:06.657235
version: '1.0'
type: note
---
# Reporte de Ingeniería: Localización de Recursos y Empaquetado Estándar

Este documento detalla la transición de un sistema de archivos basado en rutas de desarrollo (Git-centric) a un sistema de distribución de paquetes Python (PEP 517/518).

## I. Arquitectura de Rutas (ProjectPaths)

El sistema anterior dependía de un "anchor file" (`.gitignore`), lo cual es un anti-patrón en producción porque los archivos de control de versiones no se distribuyen en el *Wheel*.

### Lógica de Resolución Dinámica
Se implementó un sistema de doble raíz para separar el código de solo lectura de los datos volátiles del usuario:

```python
import sys
from pathlib import Path

class ProjectPaths:
    # PACKAGE_ROOT: Resuelve la ubicación física de los archivos .py instalados.
    # Se suben dos niveles desde note_creator/utils/paths.py para llegar a note_creator/
    PACKAGE_ROOT: Path = Path(__file__).resolve().parent.parent
    
    # TEMPLATES: Ubicación de recursos estáticos dentro del paquete.
    # Al estar en la raíz del paquete, Hatch los incluye si se configuran correctamente.
    TEMPLATES: Path = PACKAGE_ROOT / "templates"

    # USER_CONTEXT: Define dónde se crearán los archivos del usuario final.
    # Path.cwd() permite que la herramienta sea portable entre directorios.
    USER_ROOT: Path = Path.cwd()
    LOGS: Path = USER_ROOT / "logs"
    NOTES: Path = USER_ROOT / "notes"
    LOG_FILE: Path = LOGS / "automation.log"

    @classmethod
    def ensure_dirs(cls) -> None:
        """Asegura el entorno de ejecución aplicando Guard Clauses."""
        for directory in [cls.LOGS, cls.NOTES]:
            directory.mkdir(parents=True, exist_ok=True)
        
        if not cls.TEMPLATES.exists():
            raise FileNotFoundError(f"Missing templates at: {cls.TEMPLATES}")
```

## II. Configuración del Build Backend (Hatchling)

El archivo `pyproject.toml` es el plano de construcción. El error `TemplateNotFound` era consecuencia de una estructura de carpetas anidada incorrectamente tras la instalación.

### Ajustes de Empaquetamiento
1. **Source Mapping:** Se utilizó `"src" = ""` en `wheel.sources`. Esto "aplana" la estructura: en desarrollo usas `src/note_creator`, pero instalado usas simplemente `import note_creator`.
2. **Data Inclusion:** Se forzó la inclusión de archivos no-Python (`.md`) mediante la sección de `sdist`.

### Fragmento del Manifiesto de Construcción
```toml
[tool.hatch.build.targets.wheel]
packages = ["src/note_creator"]

[tool.hatch.build.targets.wheel.sources]
"src" = ""

[tool.hatch.build.targets.sdist]
include = [
    "src/note_creator/templates/*.md",
]
```

## III. Servicio de Plantillas (TemplatingService)

Se refinó el servicio para que sea el primer punto de fallo controlado (Fail-Fast) si los recursos no están presentes.

### Mejoras Implementadas
- **Deserialización Segura:** Implementación de `_serialize_for_template` para procesar Enums de Pydantic, evitando que el nombre de la clase aparezca en el Markdown final.
- **Tratamiento de Espacios:** Configuración de `trim_blocks` y `lstrip_blocks` en el entorno Jinja2 para generar Markdown limpio sin saltos de línea accidentales.
- **Abstracción de Rutas:** El servicio ya no sabe "dónde" están las plantillas; simplemente le pide la ruta absoluta a `ProjectPaths.TEMPLATES`.

## IV. Ciclo de Vida de la Herramienta (uv tool)

Para aplicar estos cambios, el comando de reinstalación forzada es mandatorio:
`uv tool install . --force`

Este comando destruye el entorno virtual previo en `/home/dxgodoy/.local/share/uv/tools/` y recompila el Wheel con el nuevo mapeo de fuentes y archivos incluidos.