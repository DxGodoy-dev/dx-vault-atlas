# Dx Vault Atlas (dxva)

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Gestor de baúles Obsidian y herramientas de automatización de flujo de trabajo.**

`dx-vault-atlas` (o `dxva`) es un conjunto de herramientas CLI modernas e interactivas para gestionar, crear y mantener notas en Obsidian siguiendo metodologías de productividad (PARA, Zettelkasten, etc.). Está construido usando tecnologías potentes como `Typer`, `Rich`, y `Textual` para proveer una experiencia de terminal fluida y visualmente atractiva.

---

## 🚀 Características Principales

- **Creador Mágico de Notas (`note`)**: Asistente interactivo en terminal para generar nuevas notas (Proyectos, Tareas, MOCs, Info) usando plantillas y metadatos predefinidos.
- **Configuración mediante TUI (`config`)**: Configura el flujo de trabajo (directorios, templates, etc.) a través de una Interfaz de Usuario de Texto (TUI) rica y amigable.
- **Migrador Inteligente (`migrate`)**: Herramienta automatizada para actualizar esquemas antiguos de notas a la nueva versión, o simplemente para renombrar campos de metadatos.
- **Doctor de Notas (`doctor`)**: Una utilidad interactiva para arreglar problemas estructurales y fechas en tus notas existentes dentro del baúl.

## 🛠 Instalación

Este proyecto utiliza [`uv`](https://github.com/astral-sh/uv) para una gestión rápida y eficiente de dependencias y entornos. Se recomienda instalar como una herramienta global para que esté disponible en todo el sistema.

```bash
# Instalación como herramienta global (Recomendado)
uv tool install .

# O instalación en modo editable para desarrollo
uv tool install -e .
```

Si prefieres usarlo de forma local dentro de un entorno virtual activo:
```bash
uv sync
uv run dxva --help
```

## 📖 Guía de Uso

Una vez instalado, el comando `dxva` o `dx-vault-atlas` estará disponible globalmente en tu terminal.

### 📝 Creador de Notas
Lanza un asistente interactivo para crear notas o documentos. Soporta Tareas, Proyectos, notas de Información, MOCs, etc.

```bash
dxva note
```
1. Ingresa el título.
2. Selecciona el tipo de nota desde el menú interactivo.
3. Configura los metadatos visualmente (prioridad, área de enfoque, estado).
*La nota se creará automáticamente en el directorio configurado de tu baúl.*

### ⚙️ Configuración del Sistema
Administra toda la configuración técnica del proyecto de manera sencilla y centralizada.

```bash
# Ver configuración actual
dxva config show

# Editar visualmente mediante TUI 
dxva config edit

# Resetear la configuración y lanzar el wizard inicial
dxva config reset
```

### 🔧 Mantenimiento del Baúl

- **Migrar Esquemas**: Actualiza notas viejas al formato moderno de tu proyecto de Obsidian.
  ```bash
  dxva migrate
  
  # Opcional: Solo renombrar metadatos en vez de migrar completamente
  dxva migrate --rename-only
  ```

- **Doctor de Notas**: Busca inconsistencias en las notas del baúl y te asiste para corregirlas.
  ```bash
  dxva doctor
  
  # Opcional: Solo arreglar problemas de fechas sin revisión manual
  dxva doctor --fix-date
  ```

*(Nota: Puedes usar el flag `--debug-mode` en los comandos de mantenimiento para deshabilitar la interfaz visual (TUI) e imprimir o depurar logs de error completos).*

## 🏗 Estructura del Proyecto

El código fuente principal se encuentra de forma modular en `src/dx_vault_atlas/`:

- `cli.py`: Controlador principal de comandos usando el framework `Typer` con manejo sofisticado y amigable de errores.
- `shared/` & `core/`: Configuración maestra, plantillas base, módulos de TUI (`Textual`), y helpers de sistema.
- `services/`: Lógica central y componentes separados por característica (`note_creator`, `note_migrator`, `note_doctor`).

## 👨‍💻 Desarrollo Local

Para contribuir, depurar o extender las funcionalidades de la CLI:

```bash
# Instalar todo (incluyendo extras de dependencias para desarrollo)
uv sync

# Ejecutar tests unitarios e integracionales
uv run pytest

# Ejecutar linter y análisis estático de código
uv run ruff check .

# Ejecutar validaciones de tipado estricto
uv run mypy src
```

## ⚖️ Licencia

Este proyecto está distribuido bajo la licencia **MIT**. Consulta el archivo `LICENSE` para más información legal detallada.
