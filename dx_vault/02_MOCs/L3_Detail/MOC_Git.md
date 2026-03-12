---
version: '1.0'
type: moc
title: "MOC_Git"
created: 2026-01-24 00:00:00
updated: 2026-02-09 02:08:33.831228
aliases:
- MOC_Git
tags: []
---
# *Map of Content: Ingeniería de Git Senior*

Esta es la ruta de aprendizaje estructurada para Daniel Godoy. El orden garantiza que los conceptos más complejos (como Internals) se apoyen en una base sólida de comandos y flujos de trabajo.

### I. Fundamentos e Infraestructura
1. [[Fundamentos]]: El ciclo de vida de los archivos y los 4 estados de Git.
2. [[conf y ssh]]: Protocolos de identidad y seguridad mediante llaves Ed25519.
3. [[commits]]: Estándar de commits atómicos y semántica profesional.

### II. Gestión de Ramas y Flujo Remoto
4. [[ramas]]: Estrategias de Branching (GitFlow vs Trunk-Based).
5. [[sincr]]: Gestión de upstream, fetch, pull y push seguro.

### III. Control de Crisis y Limpieza
6. [[resolucion]]: Protocolo de resolución de conflictos y marcas de merge.
7. [[herramientas_rescate]]: Uso avanzado de Stash, Reset (--soft/--hard) y Revert.
8. [[limpieza]]: Rebase interactivo y Cherry-pick para un historial impecable.

### IV. Colaboración y Arquitectura Interna
9. [[Colaboración]]: Pull Requests, Code Reviews y automatización con Git Hooks.
10. [[git_internals]]: El grafo de objetos, Blobs, Trees y la mecánica del directorio .git.

---
**Directiva de Ingeniería:**
* **Atomicidad:** Un commit por micro-paso.
* **Validación:** Siempre ejecutar `git status` antes de cualquier operación de escritura.
* **Sync:** `pull --rebase` como protocolo estándar antes de subir cambios.

**Relacionados:** [[]]