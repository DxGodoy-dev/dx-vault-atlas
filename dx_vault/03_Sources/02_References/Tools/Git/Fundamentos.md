---
tags: []
source: ia
created: 24-01-2026
updated: 2026-02-09 02:05:06.659235
version: '1.0'
type: note
---
# *Fundamentos: El Ciclo de Vida de los Archivos*

### Estados de un Archivo en Git
Para dominar Git a nivel **High Junior**, es vital entender que los archivos no solo se "guardan", sino que transitan por estados lógicos que garantizan la integridad del código.

* **Untracked (Sin seguimiento)**: Archivos nuevos que Git detecta en el directorio pero que no forman parte de ningún snapshot.
* **Unmodified (Sin modificar)**: Archivos que ya están en la base de datos de Git y no han recibido cambios desde el último commit.
* **Modified (Modificado)**: Archivos rastreados que han sido editados pero aún no se han marcado para el próximo commit.
* **Staged (Preparado)**: El área de preparación o **Index**. Aquí residen los cambios que formarán parte del siguiente snapshot.

### Operaciones de Transición
* **De Untracked/Modified a Staged**:
    ```bash
    git add <archivo>  # Agrega un archivo específico
    git add .          # Agrega todos los cambios del directorio actual
    ```
* **De Staged a Unmodified (Snapshot)**:
    ```bash
    git commit -m "feat: implementar lógica de validación de esquemas"
    ```

### El Área de Staging (The Index)
Es el "limbo" donde curamos nuestros commits. Siguiendo la **Directiva de Ingeniería**, solo debemos mover al Index aquellos cambios que cumplan con una unidad lógica (Commit Atómico), evitando subir archivos basura o logs.