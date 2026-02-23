# STANDARD: S.O.L.I.D. in Python

## 1. Dependency Inversion (DIP) - La más crítica
Los módulos de alto nivel (Lógica de Negocio) no deben depender de detalles de bajo nivel (SQLAlchemy, Requests, drivers). Ambos deben depender de **Abstracciones**.

**Cómo:** Usa `typing.Protocol` (Interfaces implícitas) o `abc.ABC`.

```python
# Abstracción (Contrato)
class NotificationSender(Protocol):
    def send(self, message: str) -> None: ...

# Detalle (Implementación)
class EmailService:
    def send(self, message: str) -> None: 
        # Lógica real de SMTP
        pass

# Alto Nivel (Usa la abstracción, no el detalle)
def alert_user(sender: NotificationSender, msg: str):
    sender.send(msg)
```

## 2. Single Responsibility (SRP)
Una clase debe tener una sola razón para cambiar.
- Si una clase `User` guarda en DB, envía emails y valida contraseñas, viola SRP.
- **Solución:** `UserRepository` (DB), `EmailService` (Email), `UserValidator` (Lógica).

## 3. Composición sobre Herencia
Evita crear jerarquías de clases profundas (`BaseController > AuthController > AdminController`).
Mejor inyecta funcionalidades como componentes.
