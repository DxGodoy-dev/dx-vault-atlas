# STANDARD: Error Handling Strategy

## 1. Filosofía "Fail Fast"
Es mejor que el programa crashee con un error claro ahora, a que corrompa datos silenciosamente.
**PROHIBIDO:** `try: ... except: pass` (Bare except).

## 2. Jerarquía de Responsabilidad
- **Capas de Lógica (Services/Domain):** SOLO hacen `raise`. Nunca capturan errores para silenciarlos.
- **Entry Points (Main/API Controllers):** Son los únicos autorizados a usar `try/except` para loggear el error y dar una respuesta limpia al usuario.

## 3. Excepciones Semánticas
No uses `ValueError` para todo. Define tus propios errores para que el código hable.

```python
# Malo
raise ValueError("User not found")

# Bueno
class UserNotFoundError(Exception):
    """Raised when a specific user ID does not exist in DB."""
    pass

# Uso
if not user:
    raise UserNotFoundError(f"User {user_id} missing.")
```
