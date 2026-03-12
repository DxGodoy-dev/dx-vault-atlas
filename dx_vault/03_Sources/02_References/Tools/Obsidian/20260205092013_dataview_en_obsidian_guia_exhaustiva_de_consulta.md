---
version: '1.0'
title: "Dataview en Obsidian: Guía Exhaustiva de Consulta"
aliases:
- 'Dataview en Obsidian: Guía Exhaustiva de Consulta'
tags: []
created: 2026-02-05 09:20:13
updated: 2026-02-09 02:08:33.889228
type: info
priority: 4
status: to_read
---
# Dataview: El Motor de Bases de Datos para Obsidian

Dataview es un motor de consulta de alto rendimiento que transforma tu bóveda de notas planas en una base de datos dinámica. Permite indexar metadatos (YAML frontmatter e inline fields) para generar tablas, listas y calendarios automáticos.

---

## 1. Tipos de Consultas (DQL)

Dataview utiliza su propio lenguaje llamado *Dataview Query Language (DQL)*. Aunque no sepas SQL, su estructura es lógica y jerárquica.

### LIST
Es la consulta más simple. Devuelve una lista de notas que cumplen ciertos criterios.
* **Uso:** Ideal para índices de proyectos o registros diarios.

### TABLE
Permite visualizar columnas de datos específicos extraídos de tus notas.
* **Uso:** Comparativas de libros (Autor, Nota, Estado) o seguimiento de hábitos.

### TASK
Extrae todas las tareas (`- [ ]`) que coincidan con los filtros.
* **Uso:** Centralizar tareas pendientes de múltiples notas en un "Dashboard de Hoy".

### CALENDAR
Ubica tus notas en una vista de calendario basada en una fecha específica (usualmente la fecha de creación).

---

## 2. Anatomía de una Consulta

Una consulta estándar se divide en cuatro partes obligatorias u opcionales:

```markdown
TABLE campo1, campo2
FROM "Carpeta" o #etiqueta
WHERE campo1 = valor
SORT campo2 ASC/DESC
```

### Orígenes de Datos (FROM)
* **Carpeta:** `FROM "Proyectos/Activos"`
* **Etiqueta:** `FROM #libros`
* **Enlaces:** `FROM [[NotaEspecífica]]` (notas que enlazan a esa nota) o `FROM outgoing([[NotaEspecífica]])` (notas enlazadas por esa nota).
* **Combinaciones:** `FROM #trabajo AND "Proyectos"` (intersección) o `FROM #ocio OR #personal` (unión).

---

## 3. Metadatos: El Combustible

Para que Dataview funcione, tus notas deben tener datos. Hay dos formas de insertarlos:

### Frontmatter (YAML)
Se coloca al inicio de la nota, entre triples guiones.
```yaml
---
tipo: libro
autor: Brandon Sanderson
puntuacion: 10
leido: 2026-02-05
---
```

### Campos Inline (En línea)
Permiten anotar datos dentro del texto de la nota usando la sintaxis `Clave:: Valor`.
* *Ejemplo:* "Hoy me siento con un animo:: excelente". Dataview reconocerá "animo" como una columna.

---

## 4. Funciones de Filtrado y Lógica (WHERE)

Aquí es donde ocurre la magia. No necesitas SQL, solo entender estas comparaciones:

### Comparadores Básicos
* `=` (Igual a)
* `!=` (Diferente de)
* `<` / `>` (Menor o mayor que)
* `contains(campo, "valor")` (Si el texto contiene algo)

### El poder de `file`
Dataview añade metadatos automáticos a cada nota bajo el objeto `file`:
* `file.name`: El título del archivo.
* `file.ctime`: Fecha de creación.
* `file.mtime`: Fecha de última modificación.
* `file.tasks`: Tareas dentro de la nota.
* `file.outlinks`: Enlaces que salen de la nota.

## 5. Operaciones Avanzadas y Transformación

Dataview permite manipular los datos antes de mostrarlos para que la información sea más útil y legible.

### GROUP BY
Agrupa los resultados según un campo específico. Al usarlo, las demás columnas deben ser tratadas con funciones de agregación (como sumar o contar).
* *Ejemplo:* Agrupar tus notas por `autor` para ver cuántos libros tienes de cada uno.

### FLATTEN
"Aplana" listas. Si una nota tiene varios valores en un campo (ej. `etiquetas: [ia, python, tutorial]`), `FLATTEN` creará una fila individual para cada etiqueta en lugar de una sola fila con todas.

### Cálculos Matemáticos
Puedes realizar operaciones en tiempo real:
* `(precio * 1.21) AS precio_con_iva`
* `(fecha_fin - fecha_inicio) AS duracion`

---

## 6. DataviewJS: El Siguiente Nivel

Si bien el DQL (el lenguaje estándar) es potente, Dataview ofrece una API de JavaScript para usuarios que necesitan lógica compleja, bucles o renderizado personalizado.

### Diferencia Principal
Mientras que DQL es declarativo ("Qué quiero"), DataviewJS es imperativo ("Cómo lo obtengo"). Permite usar funciones de JavaScript puro para filtrar notas con condiciones que el lenguaje básico no puede manejar.

---

## 7. Buenas Prácticas y Rendimiento

A medida que tu bóveda crece, las consultas mal optimizadas pueden ralentizar Obsidian.

### El Filtro Temprano
Usa siempre `FROM` antes de `WHERE`. El comando `FROM` reduce la cantidad de archivos que Dataview debe leer en memoria, mientras que `WHERE` analiza el contenido de los archivos ya filtrados.

### Tipado de Datos
* **Fechas:** Usa siempre el formato `AAAA-MM-DD` para que Dataview las reconozca como objetos temporales y no como simple texto.
* **Listas:** Si usas YAML, usa corchetes `[item1, item2]` o guiones.

---

## 8. Ejemplos Prácticos para Principiantes

### Dashboard de Proyectos Activos
```markdown
TABLE prioridad, fecha_entrega
FROM "Proyectos"
WHERE estado = "En curso"
SORT prioridad DESC
```

### Tareas Pendientes en Notas de Reunión
```markdown
TASK
FROM "Reuniones"
WHERE !completed
```

### Registro de Libros Leídos este Año
```markdown
TABLE autor, puntuacion
FROM #libros
WHERE leido.year = 2026
SORT leido DESC
```

---

## 9. Plugins Complementarios

Para potenciar Dataview, Daniel, considera estos aliados:
* **Buttons:** Para ejecutar comandos o cambiar metadatos con un click.
* **Meta Bind:** Para crear formularios (inputs, dropdowns) que editen los campos de Dataview visualmente.
* **Charts:** Para crear gráficos de barras o pasteles alimentados por tus consultas de Dataview.
