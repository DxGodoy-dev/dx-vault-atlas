---
version: '1.0'
type: info
title: "_Guia_Transcripción_Jig"
created: 2026-01-25 13:55:45-04:00
updated: 2026-02-09 02:05:06.668235
aliases:
- _Guia_Transcripción_Jig
tags: []
priority: 3
status: to_read
---
# Estándar Global de Transcripción y Anotación para el Proyecto Jigglypuff: Manual Técnico de Referencia Versión 2.3

## Evolución y Propósito del Marco de Anotación Jigglypuff

La creación de conjuntos de datos de alta fidelidad para el entrenamiento de modelos de lenguaje y sistemas de reconocimiento automático de voz (ASR) constituye uno de los pilares fundamentales de la inteligencia artificial contemporánea. El proyecto Jigglypuff, gestionado a través de la plataforma ADAP de Appen y detallado en sus directrices de la versión 2.3 fechadas al 31 de diciembre de 2025, se erige como un protocolo riguroso diseñado para capturar no solo el contenido léxico del habla humana, sino también su textura acústica, emocional y contextual. Este manual de referencia tiene como objetivo consolidar de manera exhaustiva todas las reglas operativas, técnicas y lingüísticas necesarias para transformar segmentos de audio bruto en datos estructurados de calidad superior.

El analista de datos asignado a este proyecto no actúa simplemente como un transcriptor convencional; se desempeña como un especialista en anotación que debe interpretar señales complejas en entornos de audio que a menudo presentan ruido, solapamientos y variaciones dialectales significativas. La precisión en este dominio no es opcional, ya que la arquitectura de Jigglypuff se basa en la mejora sistemática de transcripciones pre-completadas por máquinas, eliminando el sesgo algorítmico y refinando la segmentación para reflejar la realidad de la comunicación humana. Para lograr este nivel de exactitud, es imperativo que el profesional comprenda la jerarquía de las unidades de trabajo: la "Unidad" (Unit) representa el contenedor total de la tarea; el "Segmento" (Segment) define la porción de audio visible en la forma de onda; y la "Región" (Region) delimita el espacio específico donde ocurre un evento de habla o ruido.

## Infraestructura Técnica y Herramientas de Navegación de Audio

El éxito en la anotación depende intrínsecamente del dominio de la interfaz de usuario en ADAP. La herramienta de transcripción de Jigglypuff integra controles avanzados que permiten una manipulación granular del flujo de audio, lo cual es crítico para identificar matices que pasarían desapercibidos en una escucha superficial.

### Componentes de la Interfaz y Controles de Reproducción

La interfaz de ADAP está diseñada para maximizar la eficiencia del transcriptor mediante una representación visual del espectro acústico. La forma de onda (waveform) no es meramente decorativa; sirve como una línea de tiempo interactiva donde la amplitud de la señal indica la presencia de habla o ruido. El uso de deslizadores de zoom permite al analista expandir la resolución temporal, facilitando la colocación de etiquetas en el milisegundo exacto donde comienza un evento.

|**Elemento Técnico**|**Función Principal**|**Relevancia Operativa**|
|---|---|---|
|**Waveform (Línea de Tiempo)**|Visualización de la amplitud del audio.|Identificación visual de picos de voz y valles de silencio.|
|**Control de Velocidad (Speed)**|Ajuste del ritmo de reproducción (0.5x a 1.0x+).|Fundamental para descifrar habla rápida o tartamudeos densos.|
|**Deslizador de Zoom**|Modificación de la resolución de la onda.|Permite una precisión quirúrgica en el etiquetado de solapamientos.|
|**Botones de Salto (Skip ±5s/25s)**|Navegación rápida por el segmento.|Optimiza el tiempo de revisión en segmentos de larga duración.|

Un requisito técnico ineludible es que el audio principal debe reproducirse en su totalidad al menos una vez antes de que el sistema permita el envío de la tarea. Este mecanismo de seguridad asegura que ninguna porción del audio sea ignorada. Asimismo, se establece como norma obligatoria el uso de auriculares de alta calidad para capturar detalles como respiraciones débiles, susurros de fondo o ruidos ambientales sutiles que son fundamentales para la integridad del conjunto de datos.

### Sistemas de Identificación del Hablante: Paneles de Referencia

La arquitectura de Jigglypuff emplea un sistema de doble panel para resolver la ambigüedad en diálogos multihablante. El Panel Izquierdo contiene el audio principal que debe ser transcrito en su totalidad, mientras que el Panel Derecho proporciona las muestras de referencia del hablante principal.

El proceso de identificación es el primer paso crítico en el flujo de trabajo. El analista debe escuchar las muestras de referencia (Sample 1, 2 y 3) para internalizar el tono, ritmo, volumen y timbre del hablante primario. Esta huella vocal sirve como el estándar contra el cual se comparan todas las voces escuchadas en el audio principal. Es vital distinguir entre las dos versiones de la herramienta que pueden encontrarse en producción:

- **Versión Actual:** Las muestras del panel derecho representan exclusivamente al hablante principal. Cualquier otra voz detectada en el audio principal que no coincida con esta huella debe ser encapsulada en la etiqueta de hablante no primario.
- **Versión Legacy:** En esta configuración, las muestras del panel derecho representan a los hablantes secundarios o no primarios. Aquí, el analista utiliza estas muestras para saber qué voces _no_ debe transcribir como principales.    

Independientemente de la versión, la regla de oro es nunca transcribir el contenido de las muestras de referencia; su única función es la calibración auditiva del analista.

## Metodología Core de Transcripción: El Estándar Verbatim

El núcleo del proyecto Jigglypuff es la transcripción literal o _verbatim_. A diferencia de la transcripción editada para lectura, la transcripción para IA busca preservar la "suciedad" lingüística del habla espontánea, ya que estos elementos proporcionan pistas cruciales sobre el procesamiento del lenguaje en el cerebro humano y la naturalidad de la interacción.

### El Hablante Principal y el Flujo Lingüístico

Todo lo expresado por el hablante principal debe transcribirse exactamente como suena, sin aplicar correcciones gramaticales o de estilo. Esto incluye la captura obligatoria de disfluencias y rellenos, que a menudo son eliminados en otros tipos de transcripción.

|**Fenómeno Lingüístico**|**Regla de Transcripción**|**Ejemplo**|
|:---:|:---:|:---:|
|**Rellenos (Fillers)**|Transcribir la forma estándar del idioma.|"um", "uh", "eh".|
|**Inicios Falsos**|Capturar la interrupción inicial.|"I- I thought...".|
|**Tartamudeos**|Usar guiones para sonidos repetidos.|"I was go-going to...".|
|**Palabras Truncadas**|Usar guion al final de la palabra cortada.|"What the he-?".|

Es una violación severa de las directrices añadir etiquetas de identificación de hablante (como "Speaker 1" o "Locutor A") para el hablante principal. Su discurso debe fluir directamente en el área de texto.

### Gestión de Voces Secundarias y Solapamientos

La complejidad aumenta cuando aparecen otras voces en el segmento. Jigglypuff utiliza una etiqueta estructural única para manejar todo lo que no proviene del hablante principal: `<nonprimaryspeakertalking>`. Esta etiqueta debe envolver cualquier discurso, risa, tos o susurro que provenga de una persona distinta al sujeto de estudio identificado en las muestras de referencia.

El tratamiento de los solapamientos (overlaps) exige una atención meticulosa a la sincronización. Si un hablante secundario interrumpe al principal, la etiqueta debe colocarse exactamente en el punto de interrupción, incluso si es a mitad de una palabra. Es aceptable, y a menudo necesario, utilizar esta etiqueta varias veces en un mismo segmento si ocurren múltiples interrupciones o sonidos de fondo. La omisión de voces de fondo, por muy débiles que sean, se considera un error de precisión, ya que el modelo de IA necesita aprender a distinguir entre señales de audio primarias y secundarias en entornos ruidosos.

## Normas de Formato y Convenciones Ortográficas

La consistencia en el formato es lo que permite que los datos transcritos sean legibles por máquinas y útiles para el entrenamiento de modelos. Jigglypuff establece reglas granulares sobre cómo representar visualmente diversos tipos de información.

### Puntuación, Capitalización y Prosodia

Se debe emplear la puntuación estándar del idioma de destino, pero su uso debe estar guiado por la acústica más que por la gramática estricta. Si una frase suena como una pregunta debido a la entonación ascendente, debe llevar signo de interrogación, incluso si gramaticalmente es una afirmación. En casos de énfasis extremo, Jigglypuff ha desarrollado un sistema de marcado específico:

- **Énfasis Tonal:** Si una palabra se pronuncia con una fuerza notable, se escribe en mayúsculas y se rodea de tres asteriscos: `***PALABRA***`.
    
- **Alargamiento de Vocales:** Para evitar inconsistencias (como escribir "holaaaaa" vs "holaaa"), se ha estandarizado el uso de un solo asterisco rodeando la vocal o sílaba prolongada: `h*o*la` o `que t*a*l`. Esta regla es una de las adiciones más importantes de la versión 2.1 y su incumplimiento es un error frecuente detectado en las revisiones de calidad.
    

### Representación de Datos Numéricos y Técnicos

El manejo de números y símbolos en Jigglypuff es estrictamente digital. El uso de palabras para representar números (como "veinte" en lugar de "20") está prohibido, a menos que el número forme parte de un nombre propio o marca específica.

|**Tipo de Dato**|**Regla de Formato**|**Ejemplo Correcto**|
|:---:|:---:|:---:|
|**Números Generales**|Siempre usar dígitos arábigos.|"El total fue 15.".|
|**Horas y Fechas**|Usar formato numérico estándar.|"Son las 7:30.", "En el año 2025.".|
|**Moneda**|Escribir el número y la palabra de la moneda.|"Cuesta 200 dollars." (No usar "$").|
|**Sitios Web**|Sin espacios y con formato URL.|"[www.google.com](https://www.google.com/)", "google.com".|
|**Símbolos**|Usar el símbolo real si existe en el teclado.|"Me dio el 7%.", "Fue una relación amor/odio.".|

Es crucial notar que el sistema ADAP no procesa correctamente el símbolo de dólar ($), por lo que las directrices exigen explícitamente deletrear la palabra "dollars" después del dígito. Esta regla subraya la importancia de adaptar la transcripción a las limitaciones técnicas de la herramienta de procesamiento de datos.

### Abreviaturas, Acrónimos e Inicialismos

La regla general para las abreviaturas es transcribirlas tal como se pronuncian. Si el hablante dice "Doctor", se escribe la palabra completa, no "Dr.". Si el hablante utiliza la abreviatura de forma natural en su discurso, se mantiene la forma hablada.

- **Acrónimos:** Palabras formadas por siglas que se pronuncian como una sola palabra (ej. NASA, UNESCO) deben escribirse en mayúsculas sin puntos ni espacios.
    
- **Inicialismos:** Siglas donde cada letra se pronuncia individualmente (ej. IBM, FBI, US). Deben escribirse en mayúsculas sin puntos ni espacios entre las letras.
    
- **Palabras Deletreadas:** Si un hablante deletrea deliberadamente una palabra (ej. "Mi nombre es Jamie, J-A-M-I-E"), se escriben las letras en mayúsculas.
    

## Ecosistema de Etiquetas (Tags): Capturando lo No Verbal

Las etiquetas son el mecanismo mediante el cual Jigglypuff traduce eventos no lingüísticos en información procesable. Estas deben estar siempre encerradas en corchetes `[ ]` y escritas en el idioma de destino del proyecto.

### Clasificación de Sonidos del Hablante y del Entorno

Los sonidos producidos por el hablante principal deben integrarse en su flujo de texto. Estos sonidos son vitales para entender el estado físico y emocional del locutor durante la conversación.

|**Categoría de Etiqueta**|**Ejemplos de Etiquetas Comunes**|**Contexto de Uso**|
|:---:|:---:|:---:|
|**Auditivas del Hablante**|`[laugh]`, `[cough]`, `[sigh]`, `[clears throat]`|Sonidos hechos por el locutor principal.|
|**Auditivas Externas**|`[ring]`, `[music]`, `[knock]`, `[background conversation]`|Ruidos que interfieren o acompañan el habla.|
|**Estructurales**|`[unintelligible]`, `[foreign]`, ``|Indican problemas de comprensión o cambios de idioma.|

Es fundamental localizar las etiquetas. En un proyecto en español, se debe usar `[risa]` en lugar de `[laugh]`, y `[tos]` en lugar de `[cough]`. El incumplimiento de esta regla de localización es uno de los motivos principales de rechazo de tareas en el control de calidad, ya que invalida el etiquetado semántico para el idioma específico del modelo.

### El Manejo de la Ininteligibilidad y el Cambio de Idioma

Cuando una porción del audio es imposible de descifrar tras múltiples intentos y el uso de las herramientas de zoom y velocidad, se debe emplear la etiqueta `[unintelligible]`. No se debe adivinar; la integridad del modelo depende de saber dónde hay lagunas en la señal acústica.

Para los cambios de idioma o _code-switching_, Jigglypuff ha introducido una regla sofisticada en la versión 2.1:

1. **Palabras Aisladas o Frases Cortas:** Se transcriben literalmente y se rodean de hashtags: `#zeitgeist#`, `#bon voyage#`. Esta regla aplica solo si el término no es un préstamo común en el idioma de destino.
    
2. **Frases Largas o Diálogos en Otro Idioma:** No se transcriben. En su lugar, se usa la etiqueta del idioma identificado: `[French]`, `[German]`. Si el idioma no es identificable, se usa `[foreign]`.
    
3. **Excepción del Inglés:** En la mayoría de los mercados, el habla en inglés se considera parte del flujo transcribible y no requiere etiquetas de idioma extranjero, simplemente se escribe normalmente.
    

## Casos Especiales: Canto, Risas y Segmentos de Ruido

Existen situaciones acústicas que desafían la estructura estándar de transcripción y requieren protocolos de manejo especializados para evitar la contaminación de los datos de habla.

### Protocolos para el Canto y la Música

El canto es una forma híbrida de comunicación que Jigglypuff categoriza según su contexto y origen:

- **Canto Espontáneo del Hablante Principal:** Si el locutor empieza a cantar durante la conversación, se debe transcribir la letra y marcar el inicio con la etiqueta `[sings]` o ``. No se considera un segmento de ruido.
    
- **Canto en Idioma Extranjero:** Si la canción es en otro idioma y es reconocible (ej. ópera), se etiqueta como ``. Si no es reconocible, se usa `[sings foreign song]`.
    
- **Música de Fondo:** Si no hay voz humana predominante, se utiliza la etiqueta `[background music]` y se maneja bajo las reglas de segmentos de ruido.
    

### Gestión de Risas Complejas y Audiencias

La risa puede ser un evento individual o colectivo, y su etiquetado varía drásticamente:

- **Risa Enlatada (Canned Laughter):** Común en medios pregrabados. Se etiqueta el segmento como `[noise]` y se anota `[canned laughter]`.
    
- **Risa de Audiencia:** Si tres o más voces ríen simultáneamente (público en vivo), se etiqueta como `[crowd laughing]` dentro de un segmento marcado como ruido.
    
- **Risa del Hablante vs. Terceros:** La risa del locutor principal es `[laugh]`. La de cualquier otra persona debe estar dentro de `<nonprimaryspeakertalking> [laughing] </nonprimaryspeakertalking>`.
    

### Segmentos de Solo Ruido (Noise-Only Segments)

En ocasiones, el sistema marca automáticamente un segmento como "Noise". En estos casos, la regla de oro es **prohibido transcribir**. El objetivo es etiquetar únicamente el sonido ambiental dominante. Intentar transcribir voces lejanas o murmullos en estos segmentos se considera un error técnico, ya que estos datos se utilizan para entrenar algoritmos de cancelación de ruido y no de reconocimiento de voz.

## El Atributo de Estilo de Habla (Speech Style)

El estilo de habla es un campo de metadatos opcional que describe la cualidad emocional o física de la voz. Su uso requiere un alto grado de objetividad por parte del analista.

### Criterios de Aplicación y Ejemplos de Estilos

Solo se debe completar este campo si el tono es **inconfundible**. En la mayoría de los casos, este campo se deja vacío. El analista no debe intentar inferir emociones sutiles; debe limitarse a lo que es auditivamente evidente.

|**Estilo de Habla**|**Descripción Acústica**|
|:---:|:---:|
|**Whispering**|Susurro claro con poco o nada de apoyo vocal.|
|**Screaming**|Gritos o habla con volumen extremadamente alto.|
|**Angry**|Tono con agresividad verbal evidente.|
|**Excited**|Tono de alta energía y entusiasmo.|
|**Crying**|El habla se interrumpe por sollozos audibles.|
|**Bored**|Tono monótono y falta de energía prosódica.|

Las etiquetas de estilo deben ingresarse en el idioma del proyecto (ej. "Susurrando" en lugar de "Whispering") y deben ser concisas (1-3 palabras). Se debe evitar el uso de jerga o términos repetitivos como "Gritando muy fuerte".

## Control de Calidad y Protocolos de Envío Final

La etapa final del flujo de trabajo es la verificación sistemática. Jigglypuff impone un estándar de calidad extremadamente alto, donde más de un error ortográfico o de formato por unidad puede resultar en el rechazo de la tarea y, eventualmente, en la descalificación del transcriptor del proyecto.

### Banderas de Segmento (Audio Segment Flags)

Antes de enviar, el analista tiene la opción de marcar "Flags" para alertar sobre problemas estructurales en el audio que impiden una transcripción normal.

- **Fully Unintelligible:** Se activa solo si **absolutamente nada** del audio es comprensible. Es una medida de último recurso. Si se puede entender una sola palabra, no se debe usar esta bandera; en su lugar, se transcribe esa palabra y se etiqueta el resto como `[unintelligible]`.
- **Incorrect Segmentation:** Se usa cuando los límites del audio son técnicamente erróneos, como silencios de más de 5 segundos al final del habla o cuando la voz principal se corta abruptamente. Es importante notar que, aunque se marque esta bandera, se debe transcribir todo el contenido audible que haya quedado dentro del segmento.    

### Checklist Final para la Excelencia en la Entrega

El proceso de revisión debe ser metódico y cubrir los siguientes puntos críticos :

1. **Validación de Identidad:** ¿He comparado la voz en el panel izquierdo con las muestras de referencia del panel derecho? ¿He asegurado que la voz principal no tenga etiquetas de locutor?.
    
2. **Integridad Verbatim:** ¿He incluido cada "um", "uh" y tartamudeo? ¿He usado guiones para palabras cortadas y elipsis para pausas?.
    
3. **Higiene de Etiquetas:** ¿Están todas las voces secundarias y ruidos de terceros dentro de `<nonprimaryspeakertalking>`? ¿Están todas las etiquetas localizadas en el idioma correcto y dentro de corchetes?.
    
4. **Precisión Técnica de Formato:** ¿He convertido todos los números a dígitos? ¿He deletreado "dollars"? ¿Están los acrónimos en mayúsculas sin puntos?.
    
5. **Ortografía de Entidades:** ¿He investigado la ortografía correcta de los nombres propios, lugares y marcas mencionadas?.
    
6. **Revisión Final de Reproducción:** ¿He escuchado el segmento completo una última vez mientras leo mi transcripción para asegurar que no falten palabras u overlaps?.
    

La adherencia estricta a este manual no solo garantiza la remuneración por tarea, sino que contribuye a la creación de modelos de inteligencia artificial capaces de comprender la diversidad y complejidad de la comunicación humana global. En el ecosistema de Jigglypuff, la precisión técnica es la forma más alta de respeto hacia los datos y hacia el futuro de la tecnología del lenguaje.