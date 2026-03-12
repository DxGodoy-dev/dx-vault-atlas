---
tags: []
source: ia
priority: 5
created: 2026-02-02
updated: 2026-02-09 02:05:06.665235
version: '1.0'
type: note
---
### I. Navegación Atómica (Modo Normal)
* **h / j / k / l**: Izquierda, abajo, arriba, derecha.
* **w / b**: Inicio de siguiente palabra / palabra anterior.
* **W / B**: Salto de palabra ignorando símbolos (basado en espacios).
* **e / ge**: Final de palabra actual / palabra anterior.
* **0 / ^ / $**: Inicio de línea, primer carácter no blanco, final de línea.
* **gg / G**: Inicio / Final del documento.
* **{ / }**: Salto de párrafo (bloque de código o texto).
* **%**: Salta al cierre/apertura de paréntesis, corchete o llave correspondiente.
* **f{char} / t{char}**: Salta hacia adelante hasta el carácter {char} / justo antes.
* **F{char} / T{char}**: Igual que anterior, pero hacia atrás.
* **; / ,**: Repite el último salto `f` o `t` / en dirección contraria.
* **H / M / L**: Salto a la parte alta (High), media (Middle) o baja (Low) de la pantalla.
* **Ctrl+u / Ctrl+d**: Subir / Bajar media pantalla.
* **Ctrl+b / Ctrl+f**: Subir / Bajar pantalla completa.

### II. Edición y Verbos (Operadores)
* **i / a**: Insertar antes / después del cursor.
* **I / A**: Insertar al inicio / final de la línea.
* **o / O**: Nueva línea abajo / arriba.
* **r / R**: Reemplazar un carácter / Entrar en modo reemplazo.
* **s / S**: Borrar carácter y entrar en insert / Borrar línea y entrar en insert.
* **x / X**: Borrar carácter bajo el cursor / antes del cursor.
* **cw**: Cambiar palabra (borra y entra en insert).
* **cc**: Cambiar línea completa.
* **C**: Cambiar desde el cursor hasta el final de la línea.
* **dd / d$**: Borrar línea / Borrar hasta el final de línea.
* **dw / db**: Borrar hasta inicio de siguiente palabra / palabra anterior.
* **D**: Sinónimo de `d$`.
* **yy / y$**: Copiar línea / Copiar hasta el final de línea.
* **p / P**: Pegar después / antes del cursor.
* **u / Ctrl+r**: Deshacer (Undo) / Rehacer (Redo).
* **.**: Repetir el último comando de edición (Clave para DRY).

### III. Objetos de Texto (La Magia de Vim)
Se usan tras un verbo (`c`, `d`, `y`, `v`).
* **i / a**: "Inside" (dentro) / "Around" (alrededor).
* **iw / aw**: Palabra interna / Palabra con espacio.
* **i" / i' / i`**: Contenido entre comillas.
* **i( / i[ / i{**: Contenido entre paréntesis, corchetes o llaves.
* **it**: Contenido dentro de un tag HTML/XML.
* **ip / ap**: Párrafo interno / Párrafo completo.

### IV. Visualización y Bloques
* **v**: Modo Visual (carácter).
* **V**: Modo Visual Lineal (líneas completas).
* **Ctrl+v**: Modo Visual de Bloque (Columnas). Útil para comentar múltiples líneas.
* **gv**: Seleccionar de nuevo el último bloque visual.
* **o**: Saltar al otro extremo de la selección visual.

### V. Comandos de Línea (Modo Ex - `:`)
* **:w / :q / :wq / :q!**: Guardar, Salir, Guardar y Salir, Salir sin guardar.
* **:x**: Similar a `:wq` (solo guarda si hay cambios).
* **:e {file}**: Abrir archivo.
* **:vsp / :sp**: Dividir pantalla vertical / horizontalmente.
* **:set nu / :set rnu**: Activar números de línea / números relativos.
* **:noh**: Quitar el resaltado de la última búsqueda.
* **:%s/old/new/g**: Reemplazar "old" por "new" en todo el archivo.
* **:r !{cmd}**: Insertar salida de comando externo (Ej: `:r !python3 script.py`).
* **:!{cmd}**: Ejecutar comando externo sin salir de Vim.

### VI. Gestión de Ventanas y Buffers
* **Ctrl+w + h/j/k/l**: Moverse entre ventanas divididas.
* **Ctrl+w + r**: Rotar ventanas.
* **Ctrl+w + =**: Igualar tamaño de ventanas.
* **:ls**: Listar buffers abiertos.
* **:bn / :bp**: Siguiente buffer / Buffer anterior.
* **:bd**: Cerrar buffer actual.

### VII. Automatización y Registro
* **q{a-z}**: Empezar a grabar macro en el registro indicado.
* **q**: Detener grabación de macro.
* **@{a-z}**: Ejecutar macro del registro.
* **@@**: Ejecutar última macro usada.
* **"{a-z}y**: Copiar en un registro específico.
* **"{a-z}p**: Pegar desde un registro específico.

### VIII. Búsqueda y Marcas
* **/{query} / ?{query}**: Buscar hacia adelante / atrás.
* **n / N**: Siguiente / Anterior resultado de búsqueda.
* **\*** / **#**: Buscar la palabra bajo el cursor hacia adelante / atrás.
* **m{a-z}**: Crear una marca en la posición actual.
* **'{a-z}**: Saltar a la marca creada.