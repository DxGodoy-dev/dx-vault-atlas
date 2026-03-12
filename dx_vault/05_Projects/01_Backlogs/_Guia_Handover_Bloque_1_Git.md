---
tags:
- Handover
- Git
- Infraestructura
source: ia
created: 25-01-2026
updated: 2026-02-09 02:05:06.672235
version: '1.0'
type: note
---
## *Handover: Bloque 1 - Infraestructura y Git Senior*

Esta guía está diseñada para re-hidratar el contexto técnico al iniciar la jornada. El objetivo es consolidar la base de operaciones antes de proceder a la automatización en Python.

### Contexto de Ejecución
* **Usuario:** Daniel Godoy (High Junior / Product Mindset).
* **Entorno:** Acer 311 (Linux/Crostini), VS Code, Obsidian.
* **Meta:** Migrar de un flujo manual a un repositorio privado con versionado profesional y scripts de sincronización robustos.

### Paso 1: Auditoría de Conocimiento (MOC Git)
Antes de tocar la terminal, realizaremos una validación rápida de los conceptos clave documentados ayer:
* Verificación de los 4 estados (Working, Staging, Local Repo, Remote).
* Diferencia crítica entre `git reset --soft` y `--hard` para recuperación de desastres.
* Uso de *Conventional Commits* para el historial de la bóveda.

### Paso 2: Configuración del Repositorio Privado
Establecer la conexión segura y el filtrado de archivos:
* **SSH Check:** Validar conexión con `ssh -T git@github.com`.
* **.gitignore:** Crear el archivo en la raíz del Vault para excluir:
    * `workspace.json` y `workspace-mobile.json`.
    * Caché de plugins y archivos temporales (`.trash/`).
* **Initial Push:** `git init`, vinculación del `remote origin` y primer commit de base.

### Paso 3: Script de Sincronización (`sync_vault.sh`)
Desarrollo de un script de bash optimizado para la Acer 311 que automatice el mantenimiento:
1.  **Pull con Rebase:** `git pull --rebase` para mantener un historial lineal.
2.  **Add & Commit:** Capturar todos los cambios con un mensaje automático que incluya la marca de tiempo (`date`).
3.  **Push:** Subir cambios al repositorio privado.
4.  **Guard Clause:** El script debe abortar si el `pull` genera conflictos, protegiendo la integridad de la nota.



---

### 📌 Instrucciones para Gemini
1. No entregar el código del script de una vez; esperar a que Daniel confirme la creación de los archivos previos.
2. Mantener el enfoque de **Modo Mentor**: explicar la bandera `--rebase` y por qué es vital en este flujo.
3. Asegurar que el script sea ejecutable (`chmod +x`).