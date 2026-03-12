---
tags: []
source: ia
created: 24-01-2026
updated: 2026-02-09 02:05:06.661235
version: '1.0'
type: note
---
# *Limpieza y Reescritura: Rebase y Cherry-pick*

### Git Rebase: La Alternativa Elegante al Merge
El **Rebase** toma los commits de una rama y los "vuelve a escribir" sobre la punta de otra rama. Esto crea un historial lineal, sin los ruidosos "Merge commits".

* **Uso estándar**: Para actualizar tu rama de funcionalidad con lo último de `main`.
    [CB-START: bash]
    git checkout feature/logic
    git rebase main
    [CB-END]
* **Rebase Interactivo (`-i`)**: Permite limpiar tu historial antes de entregarlo. Puedes combinar commits (squash), editarlos o eliminarlos.
    [CB-START: bash]
    git rebase -i HEAD~3  # Gestiona los últimos 3 commits
    [CB-END]

### Git Cherry-pick: Selección Quirúrgica
Permite tomar un commit específico de cualquier rama y aplicarlo en tu rama actual. Es útil cuando necesitas una corrección de bug que está en otra rama sin traer todo el historial de esa rama.

* **Comando**:
    [CB-START: bash]
    git cherry-pick <hash_del_commit>
    [CB-END]

### Guard Clauses de Reescritura
* **Regla de Oro**: **NUNCA** hagas rebase de ramas que ya han sido publicadas (Push) en un repositorio compartido. Esto altera el historial de tus compañeros y causa caos en la sincronización.
* **Uso Senior**: Usa Rebase en local para limpiar tus Micro-pasos y que el historial se vea profesional antes del Pull Request.