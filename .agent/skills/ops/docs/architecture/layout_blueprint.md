# STANDARD: Project Layout & Path Management

## 1. Estructura de Directorios Mandatoria
El proyecto debe seguir estrictamente esta jerarquía para mantener el código limpio:

root/
├── .standards/         # Submódulo de conocimiento (Vendorized)
├── src/                # ÚNICO lugar para código fuente de la aplicación
│   ├── modules/        # Dominios de negocio (User, Order, Payment)
│   ├── shared/         # Utilidades compartidas y Value Objects
│   └── main.py         # Entry point
├── tests/              # Espejo de src/ para pruebas
├── logs/               # Rotación de archivos de log (ignorado en git)
├── config.py           # Configuración centralizada
└── README.md

## 2. Gestión de Rutas (Pathlib Strict)
**PROHIBIDO:** Usar os.path.join, os.getcwd, etc.
**MANDATORIO:** Usar pathlib.Path.

### Ejemplo Correcto:
```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
```

## 3. Entry Points
- main.py debe ser minimalista. Solo orquesta la inicialización de configuración, logging y arranque de servicios.
- No debe contener lógica de negocio.
