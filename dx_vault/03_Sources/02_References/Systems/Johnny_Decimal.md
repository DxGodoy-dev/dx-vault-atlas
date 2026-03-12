---
tags:
- Organización
- Metodología
- GestiónDeDatos
source: ia
created: 20-01-2026
updated: 2026-02-09 02:05:06.657235
version: '1.0'
type: note
---
# Sistema Johnny.Decimal
El sistema Johnny.Decimal es una metodología de organización lógica diseñada para encontrar cualquier archivo o nota en menos de dos segundos. Se basa en una jerarquía numérica fija que elimina la ambigüedad en la categorización.

### 1. Estructura Jerárquica

El sistema se divide en tres niveles de granularidad:

- **Áreas (10-19):** Las categorías de nivel superior (ej. Finanzas).
- **Categorías (11):** Divisiones específicas dentro de un área (ej. Impuestos).    
- **IDs de Objeto (11.01):** El archivo o carpeta final (ej. Declaración 2025).

### 2. Los Códigos de Área (00-99)

El sistema reserva 10 áreas principales, cada una con capacidad para 10 categorías:

- **00–09: Sistema y Gestión:** Administración del propio sistema, índices y metadatos.    
- **10–19: Finanzas:** Contabilidad, impuestos, facturación y banca.
- **20–29: Legal:** Contratos, seguros, propiedad intelectual y documentos de identidad.
- **30–39: Salud y Bienestar:** Historial médico, rutinas de ejercicio y nutrición.
- **40–49: Educación y Aprendizaje:** Cursos, certificaciones, idiomas y notas de estudio.
- **50–59: Proyectos Profesionales:** Trabajo, clientes específicos y desarrollo de carrera.
- **60–69: Proyectos Personales:** Hobbies, viajes, hogar y reparaciones.
- **70–79: Activos Digitales:** Fotos, vídeos, librerías de código y recursos multimedia.
- **80–89: Referencia:** Artículos guardados, manuales y archivos históricos.
- **90–99: Archivo:** Proyectos finalizados y datos que ya no están activos.

### 3. Reglas de Implementación

- **No más de dos niveles de profundidad:** Solo existen Áreas y Categorías antes del punto decimal.
- **Numeración decimal:** El punto decimal (`.`) no funciona como en matemáticas; es un separador visual para identificar el objeto final (01, 02, 03...).
- **Nombres descriptivos:** El código siempre precede al nombre para mantener el orden alfanumérico (ej. `11.02 Factura de Internet`).