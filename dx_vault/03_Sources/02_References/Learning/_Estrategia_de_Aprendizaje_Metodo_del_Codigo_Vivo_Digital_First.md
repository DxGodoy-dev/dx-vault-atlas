---
version: '1.0'
type: info
title: "Estrategia de Aprendizaje Metodo del Codigo Vivo Digital First"
created: 2026-02-09 02:08:33.845228
updated: 2026-02-09 02:08:33.845228
aliases:
- _Estrategia_de_Aprendizaje_Metodo_del_Codigo_Vivo_Digital_First
tags: []
priority: 2
status: to_read
---
# Método del Código Vivo: Hibridación Zettelkasten + Implementación

## 1. Filosofía: El Código como Fuente de Verdad
Para un perfil técnico autodidacta, la nota no es el destino, sino el subproducto de la construcción. El conocimiento se valida mediante la ejecución, no mediante la lectura.
- **Principio Anti-Fricción**: Prohibido el papel. La captura debe ser digital y directa en Obsidian para evitar el "doble trabajo" de transcripción.
- **Aprendizaje Basado en Artefactos**: Cada concepto nuevo debe generar un artefacto (script, test, diagrama de arquitectura).

## 2. Fase de Captura: Outline Atómico (Input)
Durante el consumo de información (videos, docs, libros), se utiliza un *Outline* dinámico directamente en la nota de entrada:
- **Captura de Lógica**: No anotar definiciones de diccionario, sino lógica de flujo ("Si X, entonces el Logger lanza Y").
- **Pseudocódigo y Tips**: Anotar patrones de diseño o *Guard Clauses* que se identifiquen en el material.

## 3. Fase de Ejecución: Nota de Implementación (Action)
Antes de crear la nota permanente, se debe "ensuciar las manos":
- **Sandbox de Código**: Crear un archivo de prueba (ej. `test_logic.py`) aplicando lo aprendido.
- **Documentación de Errores**: La nota en Obsidian debe registrar los *bugs* encontrados durante esta fase y cómo se resolvieron (esto es lo que da valor Senior).

## 4. Fase de Destilación: Refactorización a Zettelkasten (Storage)
Una vez el código funciona y se entiende la arquitectura:
- **Notas Atómicas**: Extraer el conocimiento en notas pequeñas y vinculadas.
  - *Mal título*: "Notas sobre Pydantic".
  - *Buen título*: `[[Pydantic - Gestión de Errores en Entry-points]]`.
- **Relaciones Técnicas**: Conectar la nueva nota con principios existentes.
  - Ejemplo: Vincular `[[Pydantic]]` con `[[SOLID - Single Responsibility]]`.

## 5. El Obsidian Canvas como Plano Arquitectónico
Para perfiles de ingeniería, el Canvas no es decorativo:
- **Mapeo de Protocols/ABCs**: Usar el Canvas para visualizar cómo las interfaces conectan los módulos del proyecto actual.
- **Visualización de Micro-pasos**: Crear un tablero de flujo dentro de Obsidian para trackear el progreso del proyecto de práctica.

```python
# Ejemplo de nota "Código Vivo" integrada en el script de práctica
from pydantic import BaseModel, field_validator

class UserSchema(BaseModel):
    """
    Nota: Aplicación de validación técnica. 
    Vincular con: [[Pydantic - Field Validators]]
    """
    id: int
    username: str

    @field_validator("username")
    @classmethod
    def name_must_be_senior(cls, v: str) -> str:
        # Guard Clause mental: Si no cumple, raise inmediato
        if len(v) < 3:
            raise ValueError("Username demasiado corto")
        return v
```