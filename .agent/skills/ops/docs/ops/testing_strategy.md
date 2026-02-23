# STANDARD: Testing Strategy (Pytest)

## 1. Framework
**MANDATORIO:** Usar `pytest`. Es más pythonico, requiere menos boilerplate y sus fixtures son superiores a `unittest`.

## 2. Estructura de Tests
Cada módulo en `src/` tiene su contraparte en `tests/`.
- `src/services/auth.py` -> `tests/services/test_auth.py`

## 3. Uso de Fixtures
Evita repetir código de setup en cada test. Usa `conftest.py` para fixtures compartidas (ej: cliente de DB, usuario fake).

```python
# tests/conftest.py
import pytest
from src.models import User

@pytest.fixture
def mock_user():
    return User(id=1, name="Daniel", role="admin")

# tests/test_service.py
def test_admin_access(mock_user):
    assert mock_user.role == "admin"
```

## 4. Mocking vs Integration
- **Unit Tests:** MOCK TODO lo externo (DB, API Calls). Deben correr en milisegundos.
- **Integration Tests:** Usar base de datos real (o contenedor Docker efímero).

## 5. Coverage
No busques el 100% ciegamente.
- **Prioridad Alta:** Lógica de negocio compleja y Happy Paths.
- **Prioridad Baja:** Getters/Setters simples o configuraciones.
