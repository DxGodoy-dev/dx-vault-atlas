---
version: '1.0'
type: task
title: _Obsidian_Automation_Ideas
created: 2026-02-04
updated: 2026-02-09 02:05:06.664235
aliases:
- _Obsidian_Automation_Ideas
tags: []
priority: 4
status: to_do
area: personal
---
## MOCs
1. Crear automatización para creación automática de MOCs diarios con las notas creadas por día.
2. Investigar sobre cómo aprovechar al máximo dataview. 
3. Crear sistema de MOCs para forzar a linkear notas y mejor navegación por los archivos.
4. Cambiar tabla de YT Links por un MOC actualizado que lleve a un archivo .md con:
    - Video: `[Título del vídeo](link)`
    - Canal: `[Nombre del canal](link)`
    - Resumen de gemini: `[[Nota en sources]]` 
    - Resumen personal: `[[Nota en Zettlekasten]]`
    -  Esto es un borrador preliminar, está sujeto a cambios y tengo que pensar en: 
	    - Mejoras estéticas: Uso de emojis, mejor organización, etc. 
	    - Mejoras de eficiencia: Creación de script [[proyecto YT_extractor]] para obtención automática de los campos solo pegando el link. 
	        - Actualización de script note_creator para notas yt source style.
5. Actualización de tags predeterminados para actualización automática de los MOCs.
    - Pensar en los tags.
    - Incluir lógica de tags por defecto.
    - En los Templates (Específicos según el template, muy generales). Ej: youtube_video, project, task, etc. 
        - Investigar viabilidad para utilizar type en vez de tag para este caso.
    - En Enum (Específicos para temas, pensar). Ej: python_arch, git_commands, etc. 
        - Investigar forma de elegir varios tags desde enum. 
        - Mejorar menú para dividir tags por MOCs o áreas de trabajo/estudio. 

## Limpieza y organización
1. Creación de script para limpiar jhonny decimal, tanto carpetas como nombres de archivos (normalizer).
2. Actualizar organización al nuevo estándar de MOCS [[]].
3. Actualizar script note creator para adaptarse a la nueva organización y estándar de notas [[]].
    - Templates: Actualizar Templates y modelo Pydantic en models.py (agregar title y alias).
    - Título de la nota: Actualizar Normalizer de título para que el nombre del archivo sea un timestamp para organización por tiempo en carpeta Zettelkasten.
    - title = Título ingresado en el input.
    - alias = [Título ingresado en el input].

## Nueva Estructura (Sugerida por Gemini)
1. 00 Inbox: El punto de entrada único. Aquí cae todo lo que capturas rápido (notas de móvil, clips de web, pensamientos fugaces). Debe estar vacía al final de la semana.
2. 10 System: La sala de máquinas.
    - 11 Templates: Tus plantillas (Notas de micro-pasos, MOCs, Libros).
    - 12 Attachments: Carpeta centralizada para imágenes y PDFs (así no ensucian tus notas).
    - 13 Scripts: Si usas plugins como Templater o DataviewJS.
3. 20 Journal: Registro temporal. Aquí van tus Notas Diarias. Es el registro cronológico de tus micro-pasos y logs de trabajo.
4. 30 Sources: Notas de "bajo nivel" o externas. Resúmenes de libros, artículos, videos o cursos. Es información que alguien más escribió. Se procesan aquí antes de pasar a notas propias.
5. 40 Zettelkasten: El cerebro real. Aquí van todas tus notas atómicas y permanentes. Sin subcarpetas. El orden lo dan los enlaces y los MOCs.
6. 50 Maps (MOCs): Tu centro de control. Aquí residen exclusivamente tus mapas de contenido. Es la carpeta que más usarás para navegar.
7. 60 Projects: Notas activas. Espacio para proyectos con fecha de fin. Una vez terminado, la nota se archiva o se convierte en conocimiento permanente en la carpeta 40.
8. 90 Archive: Lo que ya no usas pero quieres conservar por historial técnico.

---
-*Relacionados:** [[ ]]
