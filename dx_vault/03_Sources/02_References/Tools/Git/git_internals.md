---
tags: []
source: ia
created: 24-01-2026
updated: 2026-02-09 02:05:06.660234
version: '1.0'
type: note
---
# *Git Internals: Bajo el Capó del Directorio .git*

### La Verdadera Naturaleza de Git
A diferencia de otros sistemas, Git no guarda "diferencias" entre archivos, sino **Snapshots** (instantáneas). Para un perfil **High Junior**, entender la carpeta `.git` es lo que permite diagnosticar errores cuando los comandos de alto nivel fallan.

### Los Objetos de Git (El Grafo)
Git es esencialmente un sistema de archivos direccionable por contenido. Todo se almacena en `.git/objects` como objetos comprimidos con un hash SHA-1:

* **Blobs (Binary Large Objects)**: Contienen el contenido del archivo, pero no su nombre ni permisos.
* **Trees (Árboles)**: Funcionan como directorios. Apuntan a otros *blobs* o *trees* y contienen los nombres de los archivos.
* **Commits**: Contienen el puntero al *tree* principal, el autor, el mensaje y, crucialmente, el hash del commit padre (creando la cadena del historial).

### El Directorio de Trabajo vs. El Grafo
* **HEAD**: Un puntero que indica en qué commit/rama estamos trabajando actualmente (ubicado en `.git/HEAD`).
* **The Index**: Un archivo binario (`.git/index`) que mapea el estado actual de lo que planeas enviar en el próximo commit.

### Guard Clauses de Integridad
* **Verificar la integridad**: Si sientes que el repo está corrupto o quieres ver la salud del grafo.
    [CB-START: bash]
    git fsck  # File System Check
    [CB-END]
* **Explorar el contenido de un hash**:
    [CB-START: bash]
    git cat-file -t <hash> # Muestra el tipo (blob, tree, commit)
    git cat-file -p <hash> # Muestra el contenido (pretty print)
    [CB-END]

### Optimización del Repositorio
Con el tiempo, Git acumula objetos huérfanos. Para mantener el rendimiento en tu Acer 311:
[CB-START: bash]
git gc --prune=now --aggressive # Garbage Collector
[CB-END]