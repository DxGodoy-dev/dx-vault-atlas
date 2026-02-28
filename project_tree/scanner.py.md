### `scanner.py` (Shared Core)

- **Ubicación Original:** `src/dx_vault_atlas/shared/core/scanner.py`
- **Propósito Exhaustivo:** Una caja negra altamente optimizada para escanear localmente el sistema de archivos (Disk I/O). Itera recursivamente a través de la Vault del usuario buscando unívocamente archivos de Markdown (`.md`), implementando exclusiones forzosas in-memory para no desperdiciar ciclos computacionales navegando carpetas basura o de metadatos como `.git` u `.obsidian`.

- **Modelo IPO (Input, Process, Output):**
    - **Input:** Instanciador recibe set de exclusiones (o usa las Default). `scan(vault_path: Path)`.
    - **Process:**
      - Llama a `os.walk(vault_path)`.
      - **Poda in-situ (In-place Pruning):** Reescribe la lista mágica `dirs[:]` del OS Walk al vuelo para ignorar rutas ocultas (nodos que empiezan con `.`) o que coinciden con los nombres excluidos (como cachés o `templates`). *Si no hiciera esto, Python exploraría cientos de MBs de historial de Git de manera inútil*.
      - Filtra los archivos descartando todo lo que no termine en `.md` exactamante.
    - **Output:** Expone un **Generador** de Python (`yield`) entregando punteros puros de tipo `Path`.

- **Desglose Interno:**
    - Constante Conjunto: `DEFAULT_EXCLUDES`.
    - `class VaultScanner`.
      - `__init__()`.
      - `scan()`: Función principal generadora con yield.

- **Dependencias:**
    - **Internas:** Ninguna acoplada (Es un cimiento reutilizable en cualquier proyecto Python genérico).
    - **Externas:** `os`, `pathlib.Path`, `collections.abc.Generator`.

> [!INFO] Nota de Arquitectura:
> Emplear el patrón Generator (`yield`) en lugar de devolver una lista gigante de Paths (`return list()`) garantiza que este escáner mantenga un consumo de RAM estable por más microscópico que sea su uso, siendo capaz de escanear una bóveda de un usuario con más de 100,000 notas distribuidas y entregar resultados uno a uno según el Note Doctor los necesite.
