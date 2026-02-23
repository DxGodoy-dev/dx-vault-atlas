# STANDARD: Logic Flow (Anti-Nesting)

## 1. La Regla del "Happy Path"
El flujo principal (éxito) debe estar alineado a la izquierda (identación 0 dentro de la función). Las condiciones de error deben retornar/salir inmediatamente.

## 2. Guard Clauses
Invierte tus `if`. En lugar de comprobar si **puedes** continuar, comprueba si **debes detenerte**.

```python
# ❌ MALO (Nesting Hell - Forma de Flecha)
def process_payment(order):
    if order.is_valid:
        if order.has_stock:
            if payment_service.charge(order):
                return "Success"
            else:
                raise PaymentError()
        else:
            raise StockError()
    else:
        raise ValidationError()

# ✅ BUENO (Flat & Clean)
def process_payment(order):
    if not order.is_valid:
        raise ValidationError()
    
    if not order.has_stock:
        raise StockError()

    # El código importante siempre a la izquierda
    if not payment_service.charge(order):
        raise PaymentError()

    return "Success"
```
