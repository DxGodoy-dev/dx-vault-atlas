---
tags: []
source: ia
created: 24-01-2026
updated: 2026-02-09 02:05:06.662235
version: '1.0'
type: note
---
# *Sincronización: Interacción con Remotos*

### Protocolos de Actualización
La sincronización no es solo "subir código", es asegurar que tu entorno local sea un reflejo fiel de la **Fuente de Verdad** (el servidor).

* **Git Fetch**: Descarga la información del servidor pero **no modifica** tu código de trabajo. Es una operación segura para inspeccionar qué han hecho otros.
* **Git Pull**: Es la combinación de `fetch` + `merge`. Actualiza tu rama local con los cambios del remoto.
    * **Modo Senior**: Se recomienda `git pull --rebase` para mantener un historial lineal y limpio.
* **Git Push**: Sube tus commits locales al servidor. Solo funciona si tu historial está al día con el remoto.

### Gestión de Upstream (Remotos)
Un repositorio puede estar vinculado a múltiples servidores (ej. GitHub y un servidor de despliegue).

* **Vincular Repositorio**:
    [CB-START: bash]
    git remote add origin git@github.com:usuario/proyecto.git
    [CB-END]
* **Configurar Upstream**: Para que Git sepa a qué rama remota corresponde tu rama local por defecto.
    [CB-START: bash]
    git push -u origin main
    [CB-END]

### Guard Clauses de Sincronización
1. **Pull antes de Push**: Siempre sincroniza los cambios de otros antes de intentar enviar los tuyos para evitar conflictos evitables.
2. **Status Check**: Usa `git status` para verificar si tu rama está "adelantada" (ahead) o "atrasada" (behind) respecto al origen.