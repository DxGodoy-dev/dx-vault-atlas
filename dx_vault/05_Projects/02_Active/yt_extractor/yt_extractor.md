---
created: 2026-01-25 13:55:45-04:00
updated: 2026-02-09 02:05:06.679235
version: '1.0'
type: note
tags: []
source: me
---
[[Tabla_YT]], [[Youtube]]

### Estructura del Proyecto (Directiva de Ingeniería)

Para construir esta herramienta de forma profesional y escalable, sigue estos pasos:

1. **Preparación del Entorno:**
    - [ ] Crear carpeta raíz del proyecto.  
    - [ ] Configurar entorno virtual: `python -m venv venv`.        
    - [ ] Crear estructura de directorios: `src/services/`, `src/models/`, `logs/`, `tests/`.        
    - [ ] Crear archivo `.env` y `requirements.txt`.        

2. **Definición de Modelos y Contratos:**    
    - [ ] En `models/`, definir el esquema de datos usando **Pydantic** (título, autor, duración).        
    - [ ] En `services/`, definir un **Protocol** (Interface) para el extractor de metadatos.

3. **Implementación del Servicio:**    
    - [ ] Implementar la clase `YouTubeService` usando la librería `yt-dlp`.        
    - [ ] Configurar `ydl_opts` con `skip_download: True` para optimizar velocidad y recursos.        
    - [ ] Aplicar **Guard Clauses** para validar la existencia de datos antes de instanciar el modelo.

4. **Lógica Principal y Robustez:**    
    - [ ] Configurar el logger centralizado en `main.py` para volcar errores en `logs/`.        
    - [ ] Implementar el bloque `try/except` en el punto de entrada (main) para capturar excepciones del servicio.        
    - [ ] Inyectar la dependencia del servicio en la lógica de control.    

5. **Validación:**    
    - [ ] Crear un test unitario básico en `tests/` para verificar la extracción con una URL conocida.