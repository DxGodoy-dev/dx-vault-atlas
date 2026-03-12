---
created: null
updated: null
type: note
tags: []
source: me
version: '1.0'
---
### `title_normalizer.py`

- **Ubicación Original:** `src/dx_vault_atlas/services/note_creator/utils/title_normalizer.py`
- **Propósito Exhaustivo:** Es una clase utilitaria diseñada para convertir cualquier texto suelto ingresado por el usuario en un nombre de archivo seguro, estandarizado (formato *snake_case*) y único conforme a los principios de identificadores Zettelkasten (ZK). Evita que la creación en disco de la nota falle por caracteres inválidos o colisiones de nombres idénticos.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** 
      - En `normalize(raw_title: str)`: String crudo (ej: "¡Hola, Mundo: Nuevo Proyecto 🚀!").
    - **Process:**
        ```mermaid
        graph TD
            A[Entrada: normalize] --> B{¿String vacío?}
            B -- Sí --> C[Lanzar ValueError]
            B -- No --> D[Generar Timestamp YYYYMMDDHHMMSS]
            D --> E[Llamar sanitize]
            E --> F[1. Descomponer Unicode y Ascii NFKD para quitar acentos]
            F --> G[2. Convertir a Minúsculas]
            G --> H[3. Regex: Reemplazar caracteres no alfanuméricos por guion bajo]
            H --> I[4. Strip: Quitar guiones extra de las orillas]
            I --> J[Concatenar: f'{Timestamp}_{Clean_Name}']
        ```
        - Valida activamente que la cadena no esté compuesta solo de espacios en blanco.
        - `sanitize` actúa como un tubo (pipeline) de procesamiento puro de texto que destruye acentos, mayúsculas y símbolos, asegurando robustez para Windows, MacOS y Linux.
    - **Output:**
      - String listo para ser inyectado como un `Path` físico (ej: `"20250101153022_hola_mundo_nuevo_proyecto"`).

- **Desglose Interno:**
    - Variable Privada `_NON_ALPHANUM_RE`: Expresión regular precompilada del patrón `[^a-z0-9]+` para optimizar rendimiento en llamadas repetidas.
    - `class TitleNormalizer`: Espacio de nombres estático para agrupar utilidades.
    - `@classmethod normalize()`: Orquestador primario que calcula la fecha actual y amarra el ID numérico a la cadena saneada.
    - `@staticmethod sanitize()`: Motor atómico de purificación que implementa decodificación destructiva de compatibilidad estricta.

- **Dependencias:**
    - **Internas:** Ninguna.
    - **Externas:** Librerías estándar `re` (Regex), `unicodedata` (UTF-8 encoding), `datetime`.

> [!INFO] Nota de Arquitectura:
> Mantener `sanitize()` separado de `normalize()` es una excelente decisión, porque permite reutilizar la lógica de sanitizado puro en otras partes del ecosistema (como tags o alias automáticos) sin forzar la inyección de una estampa de tiempo indeseada.
