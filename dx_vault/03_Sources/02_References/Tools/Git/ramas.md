---
tags: []
source: ia
created: 24-01-2026
updated: 2026-02-09 02:05:06.661235
version: '1.0'
type: note
---
# *Ramas (Branching): Estrategias y Flujos de Trabajo*

### El Concepto de Rama en Ingeniería
Una rama es un puntero móvil a un commit. En el nivel **High Junior**, las ramas no son solo "copias", sino entornos aislados para desarrollar micro-pasos sin afectar la estabilidad del producto.

### Estrategias de Trabajo (Workflows)
1. **GitFlow**: 
    * `main`: Código en producción.
    * `develop`: Integración de features terminadas.
    * `feature/*`: Desarrollo de nuevas funciones.
    * `hotfix/*`: Reparaciones urgentes en producción.
2. **Trunk-Based Development**:
    * Se trabaja principalmente sobre `main`.
    * Ramas de vida muy corta (máximo 1-2 días).
    * Ideal para **Continuous Integration (CI)**.

### Operaciones Críticas de Ramas
* **Creación y Salto**:
    ```bash
    git checkout -b feature/auth-system  # Crea y cambia a la rama
    # Alternativa moderna:
    git switch -c feature/auth-system
    ```
* **Fusión (Merge)**:
    ```bash
    git checkout main
    git merge feature/auth-system
    ```
* **Borrado de Ramas**: Mantener el repositorio limpio tras la integración.
    ```bash
    git branch -d feature/auth-system    # Borrado seguro
    git branch -D feature/auth-system    # Borrado forzado
    ```

### Guard Clauses en Branching
* **Regla de Oro**: Nunca trabajar directamente sobre `main` o `master`.
* Antes de crear una rama nueva, ejecutar `git pull` para asegurar que el punto de partida es la versión más reciente del código.