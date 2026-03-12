---
tags:
- roadmap
- android
- firebase
- architecture
source: ia
created: 21-01-2026
updated: 2026-02-09 02:05:06.675235
version: '1.0'
type: note
---
Esta guía establece los pasos técnicos para transformar la persistencia local en un sistema híbrido sincronizado, garantizando que el usuario final (tecladista) no tenga que gestionar archivos manualmente.

## Fase 1: Infraestructura Remota (Setup)
- [ ] **Configuración Firebase**: Crear proyecto en Console e integrar `google-services.json`.
- [ ] **Firestore**: Definir colección `songs` para almacenar metadatos (acordes, letras, configs).
- [ ] **Storage**: Configurar buckets para almacenamiento de binarios (.mp3).

## Fase 2: Evolución del Modelo de Datos
- [ ] **Extensión de Entity**: Añadir `lastUpdated` (Timestamp) y `remoteUrl` a `SongEntity`.
- [ ] **Remote Data Source**: Crear interfaces para llamadas a Firebase separadas de la lógica local.
- [ ] **Mappers V2**: Crear funciones de extensión para transformar `FirebaseDTO` a `Song` (Domain).

## Fase 3: Motor de Sincronización (Background)
- [ ] **WorkManager**: Implementar `SyncWorker` para tareas de fondo.
- [ ] **Lógica de Comparación**:
    * Comparar `lastUpdated` local vs remoto.
    * Descargar solo archivos inexistentes o desactualizados.
- [ ] **Download Manager**: Implementar descargas asíncronas de archivos pesados (.mp3) hacia el almacenamiento interno.

## Fase 4: UX para Usuario Senior
- [ ] **Sincronización Silenciosa**: La UI siempre lee de Room; la actualización de datos ocurre en segundo plano.
- [ ] **Restricciones de Red**: Configurar descargas automáticas solo mediante **Wi-Fi**.
- [ ] **Indicadores de Estado**: Iconografía simple (Nube) para informar disponibilidad de nuevas canciones.

## Fase 5: Estrategia de Gestión (Admin)
- [ ] **Panel de Carga**: (Tú) Subir archivos a la consola de Firebase.
- [ ] **Validación de Integridad**: Asegurar que cada registro en Firestore tenga su correspondiente archivo en Storage.