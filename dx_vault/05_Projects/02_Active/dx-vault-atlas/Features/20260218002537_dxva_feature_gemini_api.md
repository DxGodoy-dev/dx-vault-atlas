---
version: '1.0'
title: "dxva feature Gemini API"
aliases:
- dxva feature Gemini API
tags: []
created: 2026-02-18 00:25:37
updated: 2026-02-18 00:25:37.984855
type: task
priority: 3
status: to_do
area: personal
---
# Arquitectura del Automatismo dx-vault atlas

> [!INFO] Backlinks:
> - **Metadata**: [[ ]]
> - **Zettelkasten**: [[ ]]

## Arquitectura de Contexto: Carga Dinámica y Fusión de Prompts

La viabilidad técnica del sistema reside en la reconstrucción programática del entorno de ejecución del agente. En lugar de depender de una sesión de chat persistente en una interfaz web, el script motor del proyecto debe orquestar la carga de archivos locales para definir el comportamiento del modelo en cada ejecución.

Este proceso se denomina Carga Modular (Lazy Loading) y consiste en la lectura sistemática de la infraestructura de configuración alojada en el directorio local. El script identifica el comando de entrada del usuario para seleccionar el blueprint temático correspondiente. La fusión de prompts combina el `core/constitution.md`, que establece las reglas de integridad y el Protocolo de Extracción Secuencial (PES), con el módulo específico solicitado (ej. `modules/sw.md`). Esta amalgama de instrucciones se inyecta como el `system_instruction` del modelo, garantizando que el autómata opere bajo el rol de "Obsidian Saver" con total fidelidad a los estándares de densidad y seguridad definidos en la carta fundamental del sistema.

## Flujo de Ejecución PES (The Atlas Loop): Fase de Handshake e Inventario

El Protocolo de Extracción Secuencial (PES) se inicia con la fase de Handshake, diseñada para establecer un mapa cognitivo antes de la generación de contenido masivo. En esta etapa, el script motor de dx-vault atlas envía el recurso de origen al modelo, quien actúa bajo las restricciones del `core/constitution.md`. La respuesta obligatoria del sistema es el "Inventario de Extracción", una lista numerada que identifica los átomos de información detectados sin profundizar en ellos.

Desde la perspectiva de la automatización, esta fase actúa como un punto de control de calidad. El script recibe el inventario y lo procesa como una estructura de datos temporal. En un flujo totalmente automatizado, el programa detecta la presencia del bloque titulado "INVENTARIO DE EXTRACCIÓN" y, tras confirmar que la respuesta ha finalizado de acuerdo con el Veto de Continuidad (Hard Stop), procede a emitir el comando disparador ("proceder" o "siguiente") sin intervención humana. Este paso es crítico para asegurar que el modelo ha comprendido la extensión total del recurso antes de dedicar el 100% de los tokens de los turnos siguientes a la ejecución segmentada de cada punto.

## Flujo de Ejecución PES (The Atlas Loop): Fase de Fundación (H1 + Headers)

La Fase de Fundación, ejecutada en el Turno 2 del protocolo, constituye el punto de anclaje estructural de la nota técnica en Obsidian. En esta etapa, el script automatizado procesa el primer bloque de contenido sustancial generado por el modelo, el cual debe contener el Título Principal (H1) y el Header de Backlinks obligatorio. La automatización debe ser capaz de identificar y extraer el título sugerido en la primera línea de la respuesta (texto plano) para definir el nombre del archivo `.md` en el sistema de archivos local.

El motor de `dx-vault atlas` debe aplicar una lógica de filtrado para asegurar la integridad de la jerarquía blindada. Esto implica que el bloque de código markdown sea extraído limpiamente, eliminando las etiquetas de apertura y cierre del bloque contenedor. Un aspecto crítico de seguridad en esta fase es la Regla de Oro de los Corchetes: el script debe verificar que los campos de Metadata y Zettelkasten se mantengan como `[[ ]]`, dado que cualquier intento del modelo por rellenarlos se considera un fallo crítico de seguridad y debe ser gestionado por el sistema de control de errores del programa. Una vez validada y procesada, esta información se escribe como la base del nuevo recurso en el Vault, estableciendo el contexto para las inserciones atómicas posteriores.

## Flujo de Ejecución PES (The Atlas Loop): Bucle de Iteración y Append

La fase de ejecución atómica (Turnos 3+) representa el núcleo de la automatización operativa del sistema dx-vault atlas. Una vez establecida la fundación del archivo en el Turno 2, el script entra en un bucle lógico diseñado para agotar los puntos definidos en el Inventario de Extracción. El motor de automatización debe enviar de forma secuencial el comando "siguiente" o el numeral correspondiente al punto del inventario, recibiendo en respuesta un único bloque de contenido técnico denso por cada iteración.

La gestión de estos bloques requiere una lógica de anexado (append) en lugar de escritura limpia. El script debe procesar cada respuesta eliminando el título en texto plano de la primera línea y las etiquetas envolventes de markdown, para luego insertar el contenido directamente al final del archivo creado en la fase anterior. Este proceso asegura que la nota final sea un recurso masivo y continuo que respeta la jerarquía de encabezados (H2 para cada punto). El bucle finaliza cuando el script detecta que el modelo ha cubierto la totalidad del inventario o cuando se activa el Veto de Continuidad (Hard Stop) sin que existan más puntos pendientes de desarrollar, garantizando una transferencia de conocimiento sin fragmentación manual.

## Solución Técnica: Post-procesamiento de Triple Backticks (Sanitización)

La integridad del renderizado en Obsidian depende de una gestión técnica precisa de los bloques de código anidados. El Protocolo de Extracción Secuencial (PES) establece el uso obligatorio de triple comilla simple ( ''' ) para bloques de código internos, con el fin de evitar colisiones sintácticas que romperían el bloque contenedor de Markdown enviado por la API. En el flujo de automatización de dx-vault atlas, el script motor debe actuar como una capa de sanitización antes de la persistencia en disco.

El proceso de post-procesamiento implica una transformación de cadenas (string replacement) en tiempo de ejecución. Una vez que el script extrae el contenido técnico del bloque de respuesta, debe realizar una búsqueda global del patrón de triple comilla simple y sustituirlo por el delimitador estándar de Markdown (triple backtick). Esta operación permite que, aunque el modelo genere el contenido de forma "segura" para el transporte de datos, el usuario final visualice y ejecute bloques de código (Python, Bash, YAML) con el resaltado de sintaxis nativo de Obsidian una vez guardados en el vault.

## Solución Técnica: Preservación de Integridad en Metadatos

La Regla de Oro de los Corchetes es un pilar de seguridad diseñado para prevenir la corrupción de la estructura de enlaces de Obsidian durante la generación automatizada. Según el protocolo de constitución, los campos destinados a Metadata y Zettelkasten deben permanecer exclusivamente como marcadores de posición vacíos: `[[ ]]`. El autómata tiene terminantemente prohibido inferir o rellenar estos campos, ya que dicha acción se clasifica como un fallo crítico de seguridad en la gestión de la base de conocimientos.

En la implementación mediante API, el script de automatización debe validar la respuesta del Turno 2 para asegurar que esta estructura no ha sido alterada. Al tratar el flujo de datos como texto crudo (raw text), el sistema garantiza que no existan interpretaciones erróneas de los caracteres especiales. La preservación de estos corchetes vacíos permite que el usuario mantenga el control total sobre la red de conexiones de su vault, delegando en el algoritmo de dx-vault atlas únicamente la responsabilidad de la extracción de información técnica densa y estructurada.

## Solución Técnica: Gestión del Hard Stop y Control de Flujo

El éxito del Protocolo de Extracción Secuencial (PES) en un entorno automatizado depende de la capacidad del script para detectar y respetar el Veto de Continuidad (Hard Stop). Según la carta fundamental del sistema, el modelo tiene prohibido emitir cualquier palabra, comentario o cierre fuera del bloque de código tras finalizar el contenido técnico. Esta restricción no es solo estética, sino funcional: permite al motor de dx-vault atlas identificar el final exacto de un segmento de datos sin riesgo de incluir ruido o texto conversacional en la nota final de Obsidian.

El control de flujo se gestiona mediante la monitorización del estado de la generación. El script debe estar programado para detener la escucha inmediatamente después de detectar el cierre del bloque de código ( ` ). Cualquier intento de añadir metadatos no solicitados, resúmenes o frases de cortesía se considera una violación del protocolo y debe ser truncada por la lógica del programa. Esta rigidez asegura que el sistema se comporte como un autómata puro, optimizando el uso de la ventana de contexto y garantizando que el archivo .md resultante sea exclusivamente técnico y libre de artefactos de chat.

## Pseudocódigo de Implementación (Atlas Script Logic)

La traducción del flujo manual a un sistema autónomo se puede sintetizar en la siguiente lógica de control para el script motor:

'''python
# 1. SETUP DE CONTEXTO
Cargar 'core/constitution.md' y 'core/router.md'
Identificar comando de usuario (ej. 'sw') -> Cargar 'modules/sw.md'
Inicializar sesión de API con instrucciones de sistema fusionadas

# 2. FASE DE HANDSHAKE (TURNO 1)
Respuesta = API.enviar(Input_Usuario)
Si "INVENTARIO DE EXTRACCIÓN" en Respuesta:
    Extraer lista de puntos
    Enviar comando "proceder"

# 3. BUCLE DE EXTRACCIÓN (TURNO 2+)
Mientras existan puntos en el Inventario:
    Bloque = API.recibir_respuesta()
    
    # Limpieza y Sanitización
    Contenido = Extraer_Markdown(Bloque) 
    Contenido = Contenido.replace("'''", "```") # Restaurar bloques de código
    
    Si es el primer bloque:
        Nombre_Archivo = Extraer_H1(Contenido)
        Crear_Archivo(Nombre_Archivo, Contenido)
    Sino:
        Anexar_Al_Archivo(Nombre_Archivo, Contenido)
    
    Si quedan puntos:
        API.enviar("siguiente")
    Sino:
        Finalizar_Proceso()
'''

Esta estructura lógica permite que el sistema dx-vault atlas funcione de manera cíclica, transformando una simple entrada de texto en una nota de conocimiento masiva, estructurada y lista para el consumo dentro de Obsidian sin intervención humana entre fases.
