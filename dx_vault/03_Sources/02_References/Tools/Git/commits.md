---
tags: []
source: ia
created: 24-01-2026
updated: 2026-02-09 02:05:06.660234
version: '1.0'
type: note
---
# *Gestión de Commits: Ingeniería de Trazabilidad y Atomicidad*

Esta nota define el estándar de registro de cambios bajo una mentalidad de arquitectura robusta, asegurando que cada commit sea una pieza de rompecabezas perfecta en el historial del proyecto.

### 1. La Anatomía de un Commit Senior
Un commit no es solo un "guardado"; es un **snapshot** del estado del proyecto.
* **Atomicidad Funcional:** Cada commit debe ser reversible. Si un commit rompe algo, hacer `git revert` debe eliminar el error sin afectar otras funcionalidades.
* **Identidad:** Todo commit debe estar firmado. 
    * `git config --global user.name "Daniel Godoy"`
    * `git config --global user.email "tu_email@ejemplo.com"`

### 2. Estándar de Comunicación (Conventional Commits)
El mensaje de commit es documentación técnica.
* **Estructura:** `<tipo>(<scope>): <descripción>`
* **Tipos Obligatorios:**
    * `feat`: Nueva funcionalidad para el usuario.
    * `fix`: Reparación de un error (bug).
    * `refactor`: Cambio de código que no altera el comportamiento (limpieza, optimización).
    * `chore`: Tareas de mantenimiento (actualizar dependencias, configurar linters).
    * `test`: Implementación o ajuste de la suite de pruebas.
* **Sintaxis Imperativa:** El título debe completar la frase: *"Si se aplica, este commit [título]"*. 
    * ✅ `feat: add pydantic validation`
    * ❌ `feat: added pydantic validation`

### 3. El Staging Area: Control de Granularidad
Dominar el área de preparación permite separar lógica mezclada accidentalmente.

#### A. Selección por Hunks (Interactivo)
Cuando el archivo `main.py` tiene un refactor arriba y un bugfix abajo:
* **Comando:** `git add -p [archivo]`
* **Operadores de Decisión:**
    * `y`: (Yes) Agrega el bloque al stage.
    * `n`: (No) Lo deja fuera para el próximo commit.
    * `s`: (Split) Si el bloque es muy grande, Git intenta dividirlo en partes más pequeñas.
    * `e`: (Edit) Abre el editor para que elijas línea por línea qué subir (Nivel Experto).

### 4. Ciclo de Vida y Corrección (Safety Guards)
Protocolos para cuando el commit ya fue realizado pero contiene errores.

* **Enmendar (The Amend Rule):** Solo usar si el commit **no** ha sido subido (`push`) al servidor.
    * `git commit --amend --no-edit`: Agrega cambios olvidados al último commit sin cambiar el mensaje.
* **El Historial como Grafo:** * `git log --oneline --graph --decorate --all`: Comando fundamental para visualizar ramificaciones y estados de punteros (HEAD).

### 5. Directiva de Calidad (Pre-commit)
Un Senior automatiza la validación. Antes de que el commit se cree, el código debe pasar por:
1. **Linter:** (Ruff) para el estilo.
2. **Static Analysis:** (Mypy) para verificar Type Hinting.
3. **Tests:** (Pytest) para asegurar que nada se rompió.