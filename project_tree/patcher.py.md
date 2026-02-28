### `patcher.py` (Note Doctor)

- **Ubicación Original:** `src/dx_vault_atlas/services/note_doctor/core/patcher.py`
- **Propósito Exhaustivo:** Mientras que `NoteFixer` arregla lógicas autónomas en segundo plano, `FrontmatterPatcher` es la aguja y el hilo para las reparaciones manuales. Se encarga de inyectar las respuestas interactivas que el usuario proporcionó en la TUI dentro del diccionario YAML que compone a la nota. Su propósito colateral -y más importante- es reordenar estéticamente todos los campos de la nota (Canonical Field Order) para que mantengan fidelidad visual homogénea a lo largo de toda la Bóveda de Obsidian.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** 
      - `frontmatter`: El diccionario original dañado/incompleto.
      - `fixes`: Un diccionario `{key: value}` de correcciones devuelto por `[[note_doctor_tui.py.md|tui.py]]`.
    - **Process:**
        ```mermaid
        graph TD
            A[Entrada: apply_fixes] --> B[Iterar sobre cada Corrección en Fixes]
            B --> C{¿La llave es especial?}
            C -- template --> D[Renombrar key a 'type']
            C -- title --> E[Asignar Título y Forzarlo dentro del Listado de Alias]
            C -- aliases/tags --> F[Convertir CSV Crudos a Listas Limpias]
            C -- Enum Object --> G[Extraer propiedad .value]
            C -- Literal --> H[Aplicar como valor directo]
            
            D --> I
            E --> I
            F --> I
            G --> I
            H --> I
            
            I[Terminar Inserciones y Empezar Reordenado: Ordered_Frontmatter] --> J[1. Recorrer ORDERED_FIELDS]
            J --> K{¿Existe en Frontmatter parcheado?}
            K -- Sí --> L[Insertar en Nueva Estructura Ordenada]
            K -- No --> J
            
            L --> M[2. Recorrer claves sobrantes o Custom Fields]
            M --> N[Añadirlos al final de la nota]
            N --> O[Retornar Diccionario Final]
        ```
    - **Output:**
      - Objeto dict de `ordered_frontmatter` pulido, parcheado y re-ordenado listo para serialización a disco.

- **Desglose Interno:**
    - Atributo de Clase `ORDERED_FIELDS`: Lista de peso que dicta qué campo debe ir primero (ej. `version` siempre encabeza y `up` o `level` van últimos).
    - `class FrontmatterPatcher`: Exposición estática utilitaria.
      - `@classmethod apply_fixes`: El inyector y organizador canónico.

- **Dependencias:**
    - **Internas:** Ninguna acoplada (Recibe tipos primitivos).
    - **Externas:** `typing`.

> [!INFO] Nota de Arquitectura:
> **Orden Visual Consistente:** Aplicar iterativamente un diccionario de un nuevo contenedor a través de los `ORDERED_FIELDS` resuelve un problema clásico de diccionarios en Python/YAML: Sin este reordenamiento, los nuevos campos inyectados aparecerían de forma desorganizada y fragmentada al final del archivo, haciendo terrible la lectura humana posterior. Al reescribirlo siempre mediante un molde estético riguroso, Obsidian presenta una visual inmaculada sin importar que una nota haya sido "parcheada".
