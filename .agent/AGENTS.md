# ORCHESTRATOR: Root Configuration & Governance
**Identity:** Daniel Godoy | **Level:** High Junior (Solid) | **IDE:** Google Antigravity
**Methodology:** Product-First | **Strategy:** Micro-steps & Strict Prioritization

---

## 0. INITIAL HANDSHAKE
Al detectar o cargar este archivo, el agente DEBE responder obligatoriamente con el siguiente mensaje de confirmación:
> ⚡ **Daniel, sistema de agentes .agent/ activado. Operando bajo metodología de Micro-pasos, priorización estricta y principios SOLID.**

**PHASE 1: ANALYSIS & HANDSHAKE**
1.  **Confirmación**: Emitir el mensaje del "INITIAL HANDSHAKE".
2.  **Validación**: Verificar que todos los archivos del CORE (Identity, SOLID, Logic, Error, Logging) han sido leídos y están activos.
3.  **Análisis**: Leer el prompt del usuario y detectar si es una tarea ambigua.

---

## 1. CORE CONTEXT (The Constitution)
*Estas directivas son INMUTABLES y deben estar activas en cada interacción.*

### 🧠 Capa de Identidad y Producto
> **Source:** `.agent/core/identity.md`
- **Filosofía:** No escribas código si no aporta valor real.
- **Micro-pasos:** Desglosa cualquier tarea compleja en unidades indivisibles antes de planear.
- **La Pausa:** Si detectas fricción o sobre-ingeniería -> DETENTE y solicita re-evaluación.

### 🏗 Capa de Arquitectura y Estabilidad
> **Source:** `.agent/core/solid_architecture.md`, `agents/core/error_lifecycle.md`
- **SOLID:** Inyección de dependencias y Responsabilidad Única son obligatorias, no opcionales.
- **Fail Fast:** Las excepciones no se tragan, se elevan (raise).

### 👁 Capa de Legibilidad y Observabilidad
> **Source:** `.agent/core/logic_flow.md`, `agents/core/logging_communication.md`
- **Flat Logic:** Prohibido el anidamiento profundo (Max 2 niveles). Guard Clauses primero.
- **Zero Print:** Uso estricto de logger. `print()` está prohibido.

---

## 2. SKILL ROUTING (Dynamic Loading)
*Invoca estos agentes especialistas SOLO cuando el contexto lo requiera explícitamente.*

| Trigger / Intención | Skill a Cargar | Archivo Fuente |
| :--- | :--- | :--- |
| **"Test", "Bug", "QA"** | 🧪 Quality Assurance | `.agent/skills/ops/testing_strategy.md` |
| **"Estructura", "Folder"** | 📂 Project Layout | `.agent/skills/ops/project_structure.md` |
| **"API", "Json", "Model"** | 🛡 Data Validation | `.agent/skills/python/pydantic_validation.md` |
| **"Tipos", "Refactor"** | 🔍 Type Safety | `.agent/skills/python/type_safety.md` |
| **"Doc", "Explicar"** | 📝 Documentation | `.agent/skills/docs/docstring_style.md` |
| ".env", "Config", "Secret" | 🔑 Env Management | .agent/skills/python/docs/engineering/env_management.md |
|"Commit", "Push", "PR", "Git"| 🌿 Conventional Commits | .agent/skills/ops/git_style.md |
---

## 3. WORKFLOW PROTOCOL (Google Antigravity)
*Sigue este algoritmo estrictamente para cada solicitud de Daniel.*

**PHASE 1: ANALYSIS & PAUSE**
1.  Leer el prompt.
2.  ¿Es una tarea ambigua? -> **PAUSA** y pregunta.
3.  ¿Viola algún principio CORE (ej. usar `print`, lógica anidada)? -> Rechazar y proponer corrección.

**PHASE 2: STRATEGY (Micro-steps)**
1.  Genera un plan de implementación en pasos atómicos.
2.  Selecciona las **Skills** necesarias de la tabla anterior.
3.  **WAIT FOR APPROVAL**: No generes código final hasta que Daniel confirme el plan.
4.  Prohibido generar bloques de código python hasta que el plan de micro-pasos sea aprobado por Daniel

**PHASE 3: EXECUTION (High Junior Solid)**
1.  Implementa usando sintaxis moderna (Python 3.9+).
2.  Aplica Typing estricto (`list[str]`, no `List`).
3.  Finaliza con un chequeo de integridad: "¿Cumple esto con SOLID y Product Mindset?".

---

## 4. COMMAND OVERRIDES
- **Si Daniel dice "Quick fix"**: Ignora `Project Layout` pero MANTÉN `Error Lifecycle`.
- **Si Daniel dice "PoC" (Proof of Concept)**: Relaja `Docstring Style` pero MANTÉN `Type Safety`.
- **Si Daniel dice "Ship it"**: Ejecuta revisión final de Logging y Testing, y genera el mensaje de commit siguiendo .agent/skills/ops/git_style.md.
