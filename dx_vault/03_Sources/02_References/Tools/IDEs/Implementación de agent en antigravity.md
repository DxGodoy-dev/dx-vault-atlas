---
created: null
updated: null
type: note
tags: []
source: me
version: '1.0'
---
Para implementar este sistema de "skills" y "sub-agentes" en un entorno de IDE (como VS Code con extensiones de Agentic AI o Cursor), debemos trabajar con una jerarquía de archivos que la IA pueda leer al iniciar el contexto.

---

## 1. Estructura de Archivos Sugerida

Crea una carpeta raíz llamada `.agent/`. Dentro, separaremos las capacidades para que el agente no se sature de información irrelevante.

- **`.agent/config.md`**: El "Cerebro" o Router. Define quién es el agente principal y cómo decide a qué sub-agente llamar.
    
- **`.agent/skills/`**: Directorio con prompts específicos para tareas técnicas (ej. `refactor.md`, `tests.md`).
    
- **`.agent/prompts/`**: Definiciones de personalidad y metodología (aquí es donde vive tu enfoque de **Micro-pasos**).
    

---

## 2. Definición del Router (config.md)

Este archivo es el "System Prompt" extendido. Debe dar instrucciones claras de que antes de actuar, debe consultar sus habilidades.

> **Instrucción:** "Daniel, siempre que inicies una tarea, verifica el directorio `.agent/skills/`. Si la tarea requiere una especialidad técnica, asume el rol del sub-agente correspondiente."

---

## 3. Implementación de Sub-agentes y Skills

Aquí te dejo un ejemplo de cómo estructurar un sub-agente especializado en tu metodología:

### Skill: Product-Minded Architect (`.agent/skills/architect.md`)

Markdown

```
# Role: Sub-agente de Arquitectura y Producto
- **Objetivo**: Validar que cada línea de código aporte valor al usuario final.
- **Protocolo**: 
  1. Analizar el impacto de la feature.
  2. Aplicar la **Metodología de Micro-pasos**.
  3. No escribir código hasta que el flujo lógico esté aprobado.
```

### Skill: Code Reviewer (`.agent/skills/reviewer.md`)

Markdown

```
# Role: Especialista en Calidad
- **Filtro**: Priorización estricta de deuda técnica vs. velocidad de entrega.
- **Regla**: Todo código debe seguir principios SOLID (High Junior level standard).
```

---

## 4. Conexión con el IDE

Para que esto funcione en la práctica, tienes dos caminos principales:

1. **Cursor / Windsurf**: Copia el contenido de `.agent/config.md` en tu archivo `.cursorrules` o `.windsurfrules`. Indica explícitamente: _"Lee los archivos en .agent/ para ejecutar sub-rutinas"_.
    
2. **Custom Instructions**: Si usas extensiones como Cline o Roo Code, apunta el "Custom Instructions Path" a tu carpeta `.agent/`.
    

### Beneficios de este sistema para tu perfil:

- **Enfoque de Pausa**: Al separar los agentes, obligas a la IA a "detenerse" y cambiar de contexto antes de escupir código.
    
- **Escalabilidad**: Si mañana quieres un experto en bases de datos, solo creas `.agent/skills/db-expert.md`.