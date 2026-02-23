# SKILL: Error Handling
**Strategy:** Fail Fast, Handle Centralized
## Directivas
1. **Solo Raise:** Servicios y lógica NUNCA capturan excepciones, solo hacen raise.
2. **Custom Exceptions:** Crear excepciones semánticas (ej: UserNotFoundError).
3. **Main Catch:** El único try/except global debe estar en main.py.
## Referencia Externa
> path: .agent/skills/python/docs/python_core/error_handling.md
