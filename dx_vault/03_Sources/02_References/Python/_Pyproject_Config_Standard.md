---
version: '1.0'
type: ref
title: "_Pyproject_Config_Standard"
created: 2026-01-24 00:00:00
updated: 2026-02-09 02:08:33.859228
aliases:
- _Pyproject_Config_Standard
tags:
- python
- architecture
- dev-tools
---
## *Configuración de Ecosistema Python (pyproject.toml)*

### Definición de Herramientas y Estándares
Este archivo centraliza la gobernanza técnica del proyecto, alineando las herramientas de análisis estático con la **Directiva de Ingeniería Senior**. Se prioriza el **Strict Type Hinting**, la eliminación de deuda técnica y la validación de contratos mediante interfaces.

### Estructura del Archivo

```toml
[project]
name = "project-name"
version = "0.1.0"
description = "High Junior (Solid) Production Template"
authors = [{name = "Daniel Godoy"}]
requires-python = ">=3.11"
dependencies = [
    "pydantic>=2.0.0",
]

[tool.ruff]
target-version = "py311"
line-length = 88
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort (import sorting)
    "B",    # flake8-bugbear (design flaws)
    "ANN",  # flake8-annotations (Type Hinting)
    "C90",  # mccabe (complexity)
    "UP",   # pyupgrade (modern syntax)
]
ignore = ["ANN101", "ANN102"] # Ignore self/cls type hints

[tool.ruff.mccabe]
max-complexity = 10

[tool.mypy]
python_version = "3.11"
strict = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_explicit = false
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]

[tool.black] # Opcional si ruff format no es suficiente
line-length = 88
```

### Implementación en Arquitectura
* **Guard Clauses:** Ruff detecta automáticamente estructuras complejas que pueden simplificarse.
* **SOLID:** Mypy valida que la **Inyección de Dependencias** cumpla con los **Protocols** definidos en el `core/`.
* **Logs:** La configuración asegura que no existan `prints` perdidos, delegando todo al sistema de logs en `logs/`.