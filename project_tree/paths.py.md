### `paths.py` (Shared)

- **Ubicación Original:** `src/dx_vault_atlas/shared/paths.py`
- **Propósito Exhaustivo:** Repositorio canónico de la Verdad (Single Source of Truth) para las definiciones y comprobaciones de rutas dentro y fuera del paquete de la aplicación. Elimina toda resolución manual frágil mediante concatenaciones de strings rígidas (`C:/` vs `/users/`).

- **Modelo IPO (Input, Process, Output):**
    - **Input:** Strings ingresados por el usuario como variables genéricas (`~/my-vault`).
    - **Process:**
      - Estipula reflectivamente (mirándose a sí mismo) la raíz del paquete local en tiempo de ejecución: `Path(__file__).resolve().parent.parent`.
      - Exporta variables globales para cruzar fronteras de dominio (hace que Migrator pueda ver un directorio de Creador).
      - La función de validación inyecta dinámicamente `.expanduser()` solventando el dilema de Linux del símbolo tilde `~`.
    - **Output:** 
      - Excepciones descriptivas de `ValueError` si las rutas no referencian Directorios.
      - Retorno de Instancias Fuertes `pathlib.Path`.

- **Desglose Interno:**
    - Constantes Base: `PACKAGE_ROOT`, `TEMPLATES_DIR`, `APP_NAME`.
    - Utilidades Defensivas: `validate_directory()`.

- **Dependencias:**
    - **Internas:** Ninguna acoplada (Es un cimiento basal).
    - **Externas:** `pathlib.Path`.

> [!INFO] Nota de Arquitectura:
> **Dynamic Refection:** Al computar dinámicamente el `PACKAGE_ROOT` basándose en el propio archivo físico (`__file__`), el ecosistema entero soporta ser re-ubicado, empaquetado vía Pip, o embebido en `site-packages` sin que esto rompa los punteros relativos a la carpeta `/templates`.
