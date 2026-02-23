# STANDARD: Environment & Configuration

## 1. Cero "Magic Strings"
**PROHIBIDO:** Usar os.getenv("API_KEY") disperso por el código.
**MANDATORIO:** Centralizar todo en una clase de configuración validada.

## 2. Pydantic Settings
Usar pydantic-settings para cargar y validar el .env. Si falta una variable crítica, la app debe fallar al arrancar (Fail Fast).

### Patrón de Implementación:
```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "MyService"
    DB_URL: str # Si falta en .env, lanza error inmediatamente
    DEBUG_MODE: bool = False
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
```

## 3. Seguridad
- .env siempre en .gitignore.
- Nunca commitear secretos por defecto en el código.
- Usar SecretStr de Pydantic para ocultar valores sensibles en logs.
