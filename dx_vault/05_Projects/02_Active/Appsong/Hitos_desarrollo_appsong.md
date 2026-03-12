---
tags:
- Android
- Kotlin
- ProjectManagement
source: ia
created: 20-01-2026
updated: 2026-02-09 02:05:06.675235
version: '1.0'
type: note
---
## 1. Fase de Cimientos y Core (Domain Layer)

- [x] **Hito 1.1:** Definición del Modelo de Datos `Song` con validación exhaustiva (Pydantic-style en Kotlin).    
- [x] **Hito 1.2:** Creación de Interfaces de Repositorio (`ISongRepository`) y protocolos de acceso a archivos.    
- [ ] **Hito 1.3:** Implementación de Use Cases: `SearchSongs`, `GetFileStructure` y `LoadSongDetails`.
 
## 2. Capa de Datos y Persistencia (Data Layer)

- [ ] **Hito 2.1:** Configuración de Database (Room recomendado) para los campos: `nombre_grupo`, `nombre_canción`, `acordes`, `config_teclado`, `canción_letra`.
- [ ] **Hito 2.2:** Servicio de escaneo de sistema de archivos (File System) para detectar archivos `.mp3`.
- [ ] **Hito 2.3:** Lógica de sincronización: Vincular archivos físicos con registros de metadatos en la DB.    
- [ ] **Hito 2.4:** Implementación de Logger centralizado (volcado a carpeta `logs/`).

## 3. Interfaz de Usuario - Explorador (Presentation Layer)

- [ ] **Hito 3.1:** Desarrollo del `FileExplorerViewModel` con manejo de estados de carga y error.
- [ ] **Hito 3.2:** Interfaz de navegación de carpetas y archivos con Jetpack Compose.
- [ ] **Hito 3.3:** Implementación del Buscador en tiempo real con filtrado reactivo.

## 4. Interfaz de Visualización y Reproducción (Viewer Layer)

- [ ] **Hito 4.1:** Pantalla del Visor: Renderizado de letras y acordes con scroll automático.
- [ ] **Hito 4.2:** Integración de `ExoPlayer` para la reproducción del archivo `.mp3`.    
- [ ] **Hito 4.3:** Panel de configuración de teclado (persistencia de presets por canción).

## 5. Pulido, QA y Despliegue (Final Phase)

- [ ] **Hito 5.1:** Optimización de Layouts para Tablet (aprovechamiento de pantalla horizontal).
- [ ] **Hito 5.2:** Pruebas unitarias (Pytest-style con `JUnit/MockK`) para casos de uso y repositorios.
- [ ] **Hito 5.3:** Generación de APK firmado y manual de usuario para el tecladista.