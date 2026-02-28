### `wizard.py` (Shared TUI)

- **Ubicación Original:** `src/dx_vault_atlas/shared/tui/wizard.py`
- **Propósito Exhaustivo:** Repositorio de Modelos Declarativos (DataClasses). Sirve como el "Lenguaje Específico de Dominio" (DSL) interno para que otros módulos (ej. `Note Creator` o `Note Doctor`) puedan definir arquitectónicamente encuestas interactivas paso a paso sin tener que conocer nada acerca del código gráfico de validación, renderizado o colores CSS. Separa por completo el *What* (qué preguntar) del *How* (cómo mostrarlo).

- **Modelo IPO (Input, Process, Output):**
    - **Input:** Variables puras de Python al momento de codificar las reglas de negocio (Keys, labels, defaults y funciones Callbacks anónimas lambda).
    - **Process:**
      - El objeto `WizardStep` permite definir bifurcaciones condicionales enviando punteros a funciones evaluadoras en su atributo `condition: Callable[[dict[str, Any]], bool]`. Esto habilita, por ejemplo, que una pregunta aparezca solo si la anterior fue respondida de cierta manera.
      - Almacena el eslabón final y variables decorativas dentro de un contenedor ensobrado `WizardConfig`.
    - **Output:** Objeto Instanciado inerte, usado más tarde como manual de instrucciones por `WizardApp`.

- **Desglose Interno:**
    - `@dataclass WizardStep`.
    - `@dataclass WizardConfig` (Agrupa los steps e inyecta callbacks asíncronos en `on_complete`).

- **Dependencias:**
    - **Internas:** Ninguna acoplada (Es un DTO).
    - **Externas:** `collections.abc.Callable`, `dataclasses`, `enum`.

> [!INFO] Nota de Arquitectura:
> **Programación Declarativa:** Gracias a la existencia de este archivo, levantar un Wizard completo con decenas de menús anidados toma 40 líneas de pura definición DataClass en los entrypoints, evitando el espagueti de clases _Widgets_ anidadas común en desarrollos Front-End.
