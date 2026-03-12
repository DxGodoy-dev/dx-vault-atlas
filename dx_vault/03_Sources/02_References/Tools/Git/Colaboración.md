---
tags: []
source: ia
created: 24-01-2026
updated: 2026-02-09 02:05:06.659235
version: '1.0'
type: note
---
# *Colaboración: Pull Requests y Automatización*

### El Ciclo del Pull Request (PR)
En un entorno de **Ingeniería Senior**, no se sube código directamente a las ramas principales. El PR es el espacio de revisión y auditoría de calidad.

* **Protocolo de Apertura**:
    * **Título**: Debe seguir los *Conventional Commits*.
    * **Descripción**: Explicar el "qué" y el "por qué", no el "cómo" (el código ya lo dice).
    * **Checklist**: Asegurar que los tests pasan y no hay errores de linting.

### Git Hooks: Calidad Automatizada
Los hooks son scripts que Git ejecuta automáticamente ante eventos específicos. Son los guardianes de la **Directiva de Calidad**.

* **Pre-commit**: Se ejecuta antes de crear el commit. Ideal para:
    * Ejecutar `flake8` o `black` (formateo).
    * Correr tests unitarios rápidos.
* **Pre-push**: Valida que el código esté listo para el servidor.

#### Ejemplo de Implementación Simple
Localizados en `.git/hooks/`, puedes crear un archivo `pre-commit` para evitar subir código con errores básicos:
[CB-START: bash]
#!/bin/sh
pytest tests/
if [ $? -ne 0 ]; then
 echo "Tests fallidos. Commit abortado."
 exit 1
fi
[CB-END]

### Code Review (Cultura de Producto)
Como **High Junior**, recibir reviews es la forma más rápida de crecer.
* **Actitud**: Ver los comentarios como mejoras al producto, no ataques personales.
* **Sugerencias**: Usar el formato de "Sugerencias de GitHub" para proponer cambios de código directos.