# STANDARD: Data Validation with Pydantic V2

## 1. Separation of Concerns
Nunca pases diccionarios crudos (`dict`) entre capas. Convierte los datos a modelos tipados en la frontera (API Entry point).

## 2. Definición de Modelos
Usar `BaseModel` y `Field` para documentación automática.

```python
from pydantic import BaseModel, Field, EmailStr, field_validator

class UserCreateDTO(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr
    age: int = Field(gt=18, description="Must be legal age")

    @field_validator('username')
    @classmethod
    def validate_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v
```

## 3. Configuración
Habilitar `populate_by_name=True` si tu API recibe `camelCase` pero tu Python usa `snake_case`.
