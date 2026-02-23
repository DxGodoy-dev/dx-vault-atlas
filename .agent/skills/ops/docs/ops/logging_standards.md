# STANDARD: Logging & Observability

## 1. Zero Print Policy
**PROHIBIDO:** `print()`. Los prints no tienen timestamp, ni nivel de severidad, ni origen. En producción son basura.
**MANDATORIO:** Usar `logging` standard de Python o librerías estructuradas (`structlog`).

## 2. Niveles de Log
- **DEBUG:** Trazas detalladas para dev (SQL queries, payload dump).
- **INFO:** Eventos del negocio ("User created", "Payment processed").
- **WARNING:** Algo inesperado pero recuperable ("Retry connection").
- **ERROR:** Fallo de operación, requiere atención.

## 3. Uso Correcto
No construyas strings manuales. Pasa los argumentos al logger para permitir lazy evaluation.

```python
import logging

logger = logging.getLogger(__name__)

# Malo
logger.info(f"User {user.id} logged in") 

# Bueno (Mejor performance y formateo)
logger.info("User %s logged in", user.id)

# Excepciones
try:
    ...
except ValueError:
    # logger.exception incluye el traceback automáticamente
    logger.exception("Failed to process user data")
```
