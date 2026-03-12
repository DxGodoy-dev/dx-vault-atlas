---
created: null
updated: null
type: note
tags: []
---
o---
version: '1.0'
type: ref
title: "Typography.css"
created: 2026-01-25 13:55:45-04:00
updated: 2026-02-09 02:05:06.643234
aliases:
- Typography.css
tags:
- arquitectura-css
- obsidian-log
- diseño-ux
- engineering
---
### 📝 Resumen de la Refactorización
Se ha transformado un sistema de estilos con colisiones de herencia en una arquitectura de **Normalización Agresiva (Zero-G Block Layout)**. El objetivo principal fue eliminar los "espacios fantasma" entre títulos y listas que el tema base de Obsidian imponía mediante contenedores internos.

### 🛠️ Conceptos Clave Implementados

* **Normalización de Bloques (`.el-`)**: 
    - Identificación de que Obsidian envuelve cada elemento en un `div` con la clase `el-`. 
    - Reseteo de márgenes y paddings de estos contenedores a cero para eliminar la suma de espacios.
* **Técnica de Succión (Negative Margin Snapping)**: 
    - Aplicación de un margen superior negativo al bloque de las listas. 
    - Compensación de la altura de línea (`line-height`) del bloque anterior para aproximar el primer bullet al encabezado.
* **Aislamiento de Encabezados en Listas**: 
    - Cambio de comportamiento a `display: inline-block` para títulos dentro de un ítem de lista.
    - Alineación vertical precisa entre el punto de la lista (bullet) y el texto del encabezado.
* **Jerarquía Matemática (Tokens)**: 
    - Centralización del control en `:root` y `body`. 
    - Uso de escala armónica basada en el ratio **1.250 (Major Third)** para una progresión de tamaños profesional.
* **Prioridad por Especificidad**: 
    - Desplazamiento de variables críticas al selector `body` con la declaración `!important`.
    - Garantía de que las preferencias de usuario sobrescriban la configuración predefinida del tema.

### 🎯 Resultado Final
- [x] Eliminación de huecos entre Títulos y Checklists.
- [x] Alineación corregida de H3 dentro de listas.
- [x] Control total del ritmo vertical mediante tokens CSS.