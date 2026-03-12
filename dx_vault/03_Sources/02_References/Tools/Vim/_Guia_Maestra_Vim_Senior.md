---
version: '1.0'
type: task
title: _Guia_Maestra_Vim_Senior
created: 2026-02-02
updated: 2026-02-09 02:05:06.665235
aliases:
- _Guia_Maestra_Vim_Senior
tags:
- tarea
priority: 5
status: to_do
area: personal
---
## Hoja de Ruta: De Usuario a Editor Senior

Para dominar Vim bajo los principios de **Arquitectura y Calidad**, la progresión debe ser modular, priorizando la gramática sobre la memorización.

### I. Fundamentos de Gramática (El "Por qué")
Vim no usa atajos, usa **sentencias**. La estructura es: `[Número] + [Verbo] + [Modificador] + [Objeto]`.
* **Verbos:** `d` (delete), `c` (change), `y` (yank/copy), `v` (visual).
* **Modificadores:** `i` (inside), `a` (around), `t` (till), `f` (find).
* **Objetos:** `w` (word), `p` (paragraph), `"` (comillas), `t` (tag/etiqueta), `(` (paréntesis).

> **Ejemplo:** `ci"` -> *Change Inside Quoted text* (Borra el contenido de las comillas y entra en modo inserción).

### II. Hitos de Aprendizaje (Micro-pasos)

1.  **Mecánica Básica (Semana 1):**
    * Navegación con `h j k l`.
    * Entrada/Salida: `i`, `a`, `o`, `:w`, `:q!`.
    * **Recurso:** Terminal > `vimtutor`.

2.  **Edición de Precisión (Semana 2):**
    * Uso del punto `.` para repetir la última acción (DRY: Don't Repeat Yourself).
    * Saltos rápidos con `f{char}` y `t{char}`.
    * Navegación por párrafos `{` y `}`.

3.  **Configuración y Tooling (Semana 3):**
    * Creación de `.vimrc` modular.
    * Integración de **LSP (Language Server Protocol)** para Python.
    * Gestión de buffers para multiactividad.

4.  **Automatización (Avanzado):**
    * **Macros:** `q{registro}` para grabar procesos repetitivos en el Protocolo Obsidian.
    * **Comandos Globales:** `:g/pattern/command` para refactorización masiva.

### III. Recursos de Ingeniería

| Recurso | Tipo | Utilidad |
| :--- | :--- | :--- |
| **:help {comando}** | Interno | La fuente de verdad absoluta. |
| **The Primeagen** | YouTube | Filosofía de "0.1% Engineer" y velocidad. |
| **Vim Golf** | Web | Desafíos para resolver ediciones en mínimos pasos. |
| **Learn Vim (Smart Way)** | Libro/Web | Enfoque en la lógica detrás de los comandos. |

### IV. Integración con Protocolo Obsidian
Para tu flujo actual, el comando clave es la lectura de la salida del sistema:
```VIML
" Ejecuta tu script de automatización y pega el resultado
nnoremap <leader>os :r !python3 ~/scripts/obsidian_save.py<CR>
```