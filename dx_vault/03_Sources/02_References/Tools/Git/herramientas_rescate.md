---
tags: []
source: ia
created: 24-01-2026
updated: 2026-02-09 02:05:06.660234
version: '1.0'
type: note
---
# *Herramientas de Rescate: Stash, Reset y Revert*

### Git Stash: El Portapapeles Temporal
Útil cuando necesitas cambiar de rama urgentemente pero tienes trabajo a medio terminar que no quieres "commitear" aún.

* **Guardar cambios**: `git stash save "descripción"`
* **Recuperar y aplicar**: `git stash pop` (aplica y borra de la lista).
* **Ver lista**: `git stash list`

### Git Reset: Retroceder en el Tiempo (Local)
Se usa para corregir errores en tu historial local **antes** de hacer push.

* **--soft**: Mueve el puntero al commit anterior, pero mantiene tus cambios en el *Staging Area*. (Ideal para corregir un mensaje de commit).
* **--mixed** (Default): Mantiene los cambios pero los saca del *Staging Area*.
* **--hard**: Borra permanentemente los cambios. **Peligro**: No hay vuelta atrás.
    [CB-START: bash]
    git reset --soft HEAD~1  # Retrocede 1 commit manteniendo el código
    [CB-END]

### Git Revert: Deshacer con Seguridad (Público)
Si ya hiciste push y necesitas deshacer un cambio en una rama compartida, **nunca uses reset**. Usa revert.

* **Funcionamiento**: Crea un nuevo commit que hace exactamente lo opuesto al commit que quieres eliminar, manteniendo la integridad del historial.
    [CB-START: bash]
    git revert <hash_del_commit>
    [CB-END]

### Git Commit --amend
Para cuando acabas de hacer un commit y olvidaste añadir un archivo o cometiste un error tipográfico en el mensaje.
[CB-START: bash]
git add archivo_olvidado.py
git commit --amend --no-edit
[CB-END]