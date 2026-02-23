# STANDARD: Static Typing Strictness

## 1. La Regla del "No Any"
**PROHIBIDO:** Usar Any. Es código perezoso que desactiva el chequeo de tipos.
**ALTERNATIVA:** - Si no sabes el tipo: Investiga.
- Si puede ser cualquier cosa (JSON): Usar dict[str, object] o TypeVar.
- Si es dinámico: Usar Protocol para definir comportamiento esperado.

## 2. Sintaxis Moderna (Python 3.10+)
Usar los tipos nativos en lugar de importar de typing (deprecated para colecciones estándar).

| Legacy (Evitar) | Moderno (Usar) |
| :--- | :--- |
| List[str] | list[str] |
| Dict[str, int] | dict[str, int] |
| Tuple[int] | tuple[int] |
| Optional[str] | str | None (Solo py3.10+) o Optional[str] |
| Union[A, B] | A | B (Solo py3.10+) |

## 3. Type Aliases
Para estructuras complejas, crear un alias descriptivo.

```python
# Malo
def process_data(data: list[dict[str, str | int]]) -> None: ...

# Bueno
JsonPayload = list[dict[str, str | int]]
def process_data(data: JsonPayload) -> None: ...
```
