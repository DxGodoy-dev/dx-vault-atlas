---
tags: []
source: ia
priority: 4
created: 2026-02-02
updated: 2026-02-09 02:05:06.666234
version: '1.0'
type: note
---
## Project Context Sync: Vim Shortcuts Research

*Objetivo de Producto*
Establecer una base de conocimiento técnica y práctica sobre comandos avanzados de Vim para optimizar el flujo de trabajo de ingeniería senior, centrándose en la manipulación de bloques de texto y automatización de edición.

*Módulos definidos en src/*
- `navigation/`: Movimiento experto (H, M, L, %, f, t).
- `editing/`: Manipulación de registros y macros.
- `regex/`: Sustitución avanzada y patrones de búsqueda.
- `config/`: Mapeos en `.vimrc` o `init.lua`.

*Interfaces/Protocols actuales*
- [Protocolo de Sustitución]: Uso de delimitadores alternativos en `:s`.
- [Protocolo de Bloques]: Manejo de `Ctrl + v` para edición vertical.

*Librerías utilizadas y Versiones*
- Vim 9.0+ / Neovim 0.9+.
- Motor de Regex: Vim default (Magic mode).

*Estado de la Suite de Tests*
- [OK] Sustitución global de patrones simples.
- [OK] Eliminación de delimitadores con `\w*`.
- [PENDIENTE] Validación de macros complejas para refactorización de código.

*Esquemas de Pydantic validados*

```yaml
shortcuts:
  - command: ":%s/pattern/replace/g"
    scope: global_replace
  - command: "ctrl+v"
    scope: block_visual_mode
```

*Siguiente Micro-paso*
Investigar y documentar el uso de registros nominados (`"ay`, `"ap`) para gestionar múltiples fragmentos de código simultáneamente.