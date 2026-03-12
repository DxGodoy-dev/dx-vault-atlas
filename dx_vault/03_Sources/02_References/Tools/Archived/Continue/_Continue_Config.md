---
tags:
- configuracion
- ai
- continue
- python
source: ia
created: 24-01-2026
updated: 2026-02-09 02:05:06.658235
version: '1.0'
type: note
---
## Arquitectura del Entorno Híbrido (Laptop i5 6ta + Chromebook)

Para maximizar el rendimiento con 8GB de RAM, se ha implementado una arquitectura de inferencia delegada, utilizando APIs externas para evitar el colapso de la CPU local.

### Especificaciones Técnicas del Entorno
* **Host:** Intel Core i5-6200U, 8GB RAM, SSD SATA.
* **Cliente:** Chromebook Acer 311 (4GB RAM) vía VS Code Tunnel.
* **Stack de IA:** Continue.dev + Gemini 1.5 Pro/Flash + Codestral.

## Configuración de Continue (`config.yaml`)

Se aplica el esquema de validación V1 (2026) para asegurar la compatibilidad con el parser de la extensión.

```yaml
name: Daniel-Senior-Config
version: 1.0.0
schema: v1

models:
  - name: "Gemini 1.5 Pro"
    provider: google-generative-ai
    model: gemini-1.5-pro-latest
    roles: [chat, edit, apply]
    requestOptions:
      headers:
        x-goog-api-key: "TU_API_KEY_AQUI"

  - name: "Gemini 1.5 Flash"
    provider: google-generative-ai
    model: gemini-1.5-flash-latest
    roles: [chat]
    requestOptions:
      headers:
        x-goog-api-key: "TU_API_KEY_AQUI"

  - name: "Codestral"
    provider: mistral
    model: codestral-latest
    roles: [autocomplete]
    autocompleteOptions:
      debounceDelay: 250
      maxPromptTokens: 1024
      onlyMyCode: true

rules:
  - "Actúa como Senior Staff Engineer."
  - "Estructura obligatoria: src/, tests/, logs/."
  - "Usar Strict Type Hinting y Docstrings (Google Style)."
  - "Implementar Guard Clauses para eliminar anidación profunda."
  - "Aplicar SOLID: Preferir composición sobre herencia."
  - "Validación estricta con Pydantic en modelos de datos."
  - "Centralizar captura de errores y logs en main.py; funciones solo lanzan (raise) excepciones."

context:
  - provider: file
  - provider: code
  - provider: diff
  - provider: terminal
```

### Directivas de Optimización de Recursos
* **Inferencia:** Se prohíbe el uso de Ollama local debido a restricciones de hardware (2 núcleos/4 hilos).
* **Autocompletado:** Delegado a Codestral/Codeium para mantener latencia mínima en el túnel.
* **Indexación:** Uso de `.continueignore` para prevenir saturación de I/O en el SSD.