---
tags: []
source: ia
priority: 4
created: 2026-02-03
updated: 2026-02-09 02:05:06.668235
version: '1.0'
type: note
---
# uv: *High-Performance Python Package & Project Manager*

## Introducción y Filosofía
*uv* es una herramienta extremadamente rápida escrita en *Rust*, diseñada para reemplazar a `pip`, `pip-compile`, `venv`, `pyenv` y `poetry` en un único binario. Su principal propuesta de valor es la velocidad (hasta 100x más rápido que pip) y la predictibilidad mediante un archivo de bloqueo (*lockfile*).

## Gestión de Herramientas y Python
A diferencia de los flujos tradicionales, *uv* gestiona las versiones de Python de forma aislada sin depender del sistema.

### Instalación de Versiones de Python
*uv* permite instalar y usar versiones específicas sin configurar variables de entorno manualmente.

```bash
# Instalar una versión específica
uv python install 3.12

# Listar versiones instaladas y disponibles
uv python list
```

### Ejecución de Herramientas Efímeras
Permite ejecutar paquetes sin instalarlos en el entorno global o del proyecto.

```bash
# Ejecutar Ruff o Black sin instalación previa
uvx ruff check .
```

---

## Estructura de Proyecto con uv
El flujo de trabajo moderno de *uv* se centra en el archivo `pyproject.toml` y el archivo de bloqueo `uv.lock`.

### Inicialización
Al iniciar un proyecto, *uv* crea la estructura base siguiendo los estándares de empaquetado de Python.

```bash
uv init mi-proyecto
cd mi-proyecto
```

### Gestión de Dependencias
Las dependencias se añaden de forma declarativa, actualizando automáticamente el entorno virtual (`.venv`) y el *lockfile*.

* **Añadir paquetes:** `uv add fastapi`
* **Grupos de desarrollo:** `uv add --dev pytest`
* **Eliminar paquetes:** `uv remove requests`

---

## Entornos Virtuales y Sincronización
*uv* maneja los entornos virtuales de forma transparente. El comando `uv sync` es fundamental para garantizar que el entorno local coincida exactamente con lo definido en `uv.lock`.

### El comando uv run
Es la forma recomendada de ejecutar scripts. Se asegura de que el entorno esté actualizado antes de la ejecución.

```bash
uv run main.py
```

---

## Comparativa Técnica: uv vs Herramientas Tradicionales

| Característica | pip + venv | Poetry | uv |
| :--- | :--- | :--- | :--- |
| **Lenguaje** | Python | Python | **Rust** |
| **Velocidad** | Lenta | Moderada | **Instantánea** |
| **Lockfile** | No (manual) | Sí (`poetry.lock`) | **Sí (`uv.lock`)** |
| **Gestión de Python** | Externa (pyenv) | Limitada | **Nativa (`uv python`)** |

## Workspaces y Monorepos
*uv* soporta la gestión de múltiples paquetes dentro de un mismo repositorio mediante *Workspaces*. Esto permite compartir un único *lockfile* y un entorno virtual común para optimizar el almacenamiento y la coherencia de versiones.

### Configuración en pyproject.toml
Para definir un espacio de trabajo, se utiliza la sección `[tool.uv.workspace]`.

```toml
[tool.uv.workspace]
members = ["packages/*"]

[tool.uv.sources]
mi-libreria-interna = { workspace = true }
```

---

## Scripts de Archivo Único (PEP 723)
Una de las funciones más potentes de *uv* es la capacidad de ejecutar scripts aislados que declaran sus propias dependencias en los metadatos del archivo.

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests",
#   "rich",
# ]
# ///

import requests
from rich import print

response = requests.get("https://api.github.com")
print(f"[bold blue]Status:[/bold blue] {response.status_code}")
```

*Uso:* `uv run script.py`. *uv* creará un entorno temporal, instalará las dependencias y ejecutará el script en un solo paso.

---

## Optimización en CI/CD (GitHub Actions)
Debido a que *uv* es un binario estático y utiliza un sistema de caché agresivo basado en *content-addressable storage*, es ideal para pipelines rápidos.

```yaml
- name: Install uv
  uses: astral-sh/setup-uv@v5
  with:
    enable-cache: true

- name: Install dependencies
  run: uv sync --frozen
```

*Nota:* El flag `--frozen` asegura que *uv* no intente actualizar el *lockfile*, garantizando reproducibilidad exacta.

---

## Configuración Avanzada y Pip Interface
Si prefieres un flujo de trabajo compatible con `pip`, *uv* ofrece el subcomando `uv pip`, que replica el comportamiento de `pip` pero con la velocidad de *Rust*.

* **Compilar requerimientos:** `uv pip compile pyproject.toml -o requirements.txt`
* **Sincronizar entorno:** `uv pip sync requirements.txt`

---

## Comandos Esenciales de Referencia

| Acción | Comando |
| :--- | :--- |
| **Actualizar uv** | `uv self update` |
| **Limpiar caché** | `uv cache clean` |
| **Ver árbol de dependencias** | `uv tree` |
| **Exportar a requirements.txt** | `uv export --format requirements-txt` |

## Resolución de Conflictos y Troubleshooting
Gracias a su algoritmo de resolución basado en *PubGrub*, *uv* proporciona mensajes de error altamente legibles cuando existen conflictos de versiones, indicando exactamente qué restricción está causando el fallo.

### Estrategias de Resolución
Si encuentras conflictos, puedes forzar versiones específicas o utilizar *overrides*.

```toml
[tool.uv]
# Forzar una versión específica para todo el proyecto
override-dependencies = [
    "pydantic==2.6.0"
]
```

---

## Gestión de Índices y Registros Privados
*uv* permite configurar múltiples índices de paquetes (como PyPI y un registro privado de la empresa) de forma eficiente y segura.

```toml
[[tool.uv.index]]
name = "mi-repo-privado"
url = "https://pypi.mi-empresa.com/simple"
explicit = true # Evita buscar paquetes públicos aquí a menos que se especifique
```

*Uso:* `uv add mi-paquete --index mi-repo-privado`

---

## Migración desde otras herramientas

### De Poetry a uv
1. Borra `poetry.lock`.
2. Ejecuta `uv init`. *uv* leerá la sección `[project]` de tu `pyproject.toml`.
3. Ejecuta `uv lock` para generar el nuevo archivo de bloqueo.

### De pip (Requirements.txt) a uv
1. Ejecuta `uv init`.
2. Importa las dependencias: `uv add -r requirements.txt`.
3. Borra el archivo `.txt` y usa `uv.lock` en su lugar.

---

## Mejores Prácticas (Senior Level)
* **No toques .venv:** Deja que *uv* gestione el entorno. Si necesitas resetearlo, simplemente bórralo y ejecuta `uv sync`.
* **Usa uvx para herramientas CLI:** Mantén tu entorno de proyecto limpio; herramientas como `ruff`, `mypy` o `black` deben ejecutarse vía `uvx` o definirse como dependencias de desarrollo.
* **Commit uv.lock:** Siempre incluye el archivo de bloqueo en tu control de versiones para garantizar que todos los desarrolladores y el CI/CD operen sobre el mismo grafo de dependencias.

---

## Resumen de Flujo de Trabajo Ideal
1. `uv init`: Crear proyecto.
2. `uv python pin 3.12`: Fijar versión de lenguaje.
3. `uv add [paquete]`: Añadir lógica de negocio.
4. `uv add --dev [paquete]`: Añadir tooling (test, lint).
5. `uv run [script]`: Ejecutar con auto-sync.