### `pydantic_utils.py` (Shared)

- **Ubicación Original:** `src/dx_vault_atlas/shared/pydantic_utils.py`
- **Propósito Exhaustivo:** Una caja de herramientas exclusiva para el manejo seguro de los modelos de validación de `Pydantic`. Su función principal es interceptar diccionarios no confiables (ej. un YAML Frontmatter que tiene campos antiguos) y podarlos antes de inyectarlos en modelos estrictos (`extra="forbid"`) que de otra forma colapsarían deteniendo la ejecución. Usado por *Note Doctor* y *Note Migrator*.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** 
      - El objeto clase del modelo objetivo (`type[BaseModel]`).
      - Diccionario crudo a validar (`data: dict[str, Any]`).
    - **Process:**
      - Escanea reflexivamente la estructura interna del modelo Pydantic suministrado leyendo `model_cls.model_fields.keys()`.
      - Agrega también al registro tolerado cualquier `alias` que haya sido definido en el modelo (crucial para soportar variables problemáticas YAML como `type`).
      - Mediante comprensión de diccionarios, itera sobre los datos originales filtrando y descartando cualquier variable que no pertenezca a la familia registrada.
    - **Output:**
      - Nuevo Diccionario limpio y 100% garantizado de no romper validadores estrictos.

- **Desglose Interno:**
    - `strip_unknown_fields()`: La función atómica.

- **Dependencias:**
    - **Internas:** Ninguna.
    - **Externas:** `pydantic.BaseModel`, `typing`.

> [!INFO] Nota de Arquitectura:
> Este script minúsculo salvaguarda la viabilidad completa del Note Doctor. Sin la limpieza previa de variables sobrantes, cualquier nota con *metadata* inyectada por otros plugins (ej. Kanbans o Dataview) fallaría las validaciones de Pydantic lanzando Excepciones Fatales inmanejables e interrumpiendo escaneos masivos.
