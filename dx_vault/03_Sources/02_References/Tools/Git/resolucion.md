---
tags: []
source: ia
created: 24-01-2026
updated: 2026-02-09 02:05:06.662235
version: '1.0'
type: note
---
# *Resolución de Conflictos: Control del Caos*

### ¿Por qué ocurre un conflicto?
En la metodología de **Micro-pasos**, el conflicto surge cuando Git no puede decidir automáticamente qué cambio mantener porque dos personas (o tú en ramas distintas) editaron la misma línea del mismo archivo.

### Protocolo de Resolución (Guard Clauses)
Nunca resuelvas un conflicto por "instinto". Sigue este orden técnico:
1. **Identificación**: Git detendrá el proceso de merge/rebase y marcará los archivos.
2. **Análisis de Marcas**:
    * `<<<<<<< HEAD`: Tus cambios locales actuales.
    * `=======`: El separador de conflicto.
    * `>>>>>>> branch-name`: Los cambios que vienen de la otra rama.
3. **Curación**: Editar el archivo manualmente para dejar el código final funcional y eliminar las marcas (`<<<`, `===`, `>>>`).

### Comandos de Control
* **Abortar**: Si el conflicto es demasiado complejo y necesitas replantear la estrategia.
    [CB-START: bash]
    git merge --abort
    git rebase --abort
    [CB-END]
* **Finalización**: Tras editar los archivos, se deben marcar como resueltos.
    [CB-START: bash]
    git add <archivo_resuelto>
    git commit -m "fix: resolve merge conflict in user validation"
    [CB-END]

### Herramientas de Apoyo
Como usas **VS Code** en tu Acer 311, aprovecha la interfaz visual de "Conflict Resolution" que resalta en colores los cambios. Es más eficiente y evita errores de sintaxis al borrar marcas manualmente.