# Dx Vault Atlas

**Gestor de baules Obsidian y automatización de flujo de trabajo.**

`dx-vault-atlas` (o `dxva`) es un conjunto de herramientas CLI para gestionar, crear y mantener notas en Obsidian siguiendo metodologías de productividad (PARA, Zettelkasten, etc.).

## Instalación

Este proyecto utiliza `uv` para la gestión de dependencias y entornos. Se recomienda instalar como herramienta global o en un entorno aislado.

```bash
# Instalación como herramienta global (recomendado)
uv tool install .

# O instalación en modo editable para desarrollo
uv tool install -e .
```

Si prefieres usarlo dentro de un entorno virtual activo:
```bash
uv sync
uv run dxva --help
```

## Uso

Una vez instalado, el comando `dxva` estará disponible en tu terminal.

### Creador de Notas (`note`)

Lanza el asistente interactivo para crear notas (Proyectos, Tareas, MOCs, Info) con plantillas predefinidas.

```bash
dxva note
```

Sigue las instrucciones en pantalla para:
1.  Ingresar el título.
2.  Seleccionar el tipo de nota.
3.  Configurar metadatos (prioridad, área, estado).

La nota se creará en tu directorio configurado (por defecto `~/dx-vault-atlas/notes`).

## Estructura del Proyecto

El código fuente se encuentra en `src/dx_vault_atlas`.
-   `services/note_creator`: Lógica del creador de notas.
-   `cli.py`: Punto de entrada de la aplicación.

## Desarrollo

```bash
# Setup
uv sync

# Tests
uv run pytest

# Linting
uv run ruff check .
```
