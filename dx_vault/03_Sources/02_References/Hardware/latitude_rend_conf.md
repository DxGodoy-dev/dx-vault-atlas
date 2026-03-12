---
version: '1.0'
type: ref
title: "latitude_rend_conf"
created: 2026-02-09 02:08:33.838228
updated: 2026-02-09 02:08:33.838228
aliases:
- latitude_rend_conf
tags: []
---
## Configuraciones de Rendimiento y Red

#### 1. Exclusiones de Desarrollo (Windows Defender)
* **Acción:** Se agregaron carpetas de proyectos (ej. `C:\Dev`) a la lista de exclusiones.
* **Propósito:** Evitar que el proceso `Antimalware Service Executable` escanee archivos de código en tiempo real, reduciendo latencia en I/O.

#### 2. Optimización de Drivers Intel (igfx)
* **Acción:** Deshabilitación de `igfxCUIService` e `igfxEM` en `msconfig`.
* **Propósito:** Eliminar telemetría y procesos de bandeja de entrada que consumen hilos de CPU innecesarios.

#### 3. Prioridad de GPU para Remote Desktop
* **Acción:** Configuración de `remoting_desktop.exe` en "Alto Rendimiento" dentro de los ajustes de gráficos de Windows.
* **Propósito:** Forzar el uso del chip **Intel HD 520** para la codificación de video, liberando los núcleos físicos de la CPU. [CB-START: PATH] C:\Program Files (x86)\Google\Chrome Remote Desktop\ [CB-END]

#### 4. Memoria Virtual Fija (Pagefile)
* **Acción:** Tamaño personalizado establecido en **4096 MB (Inicial)** y **8192 MB (Máximo)**.
* **Propósito:** Evitar el redimensionamiento dinámico del archivo de paginación, reduciendo el micro-stuttering en el disco.

#### 5. Programación del Procesador
* **Acción:** Ajuste de rendimiento para **Servicios en segundo plano** (Background services).
* **Propósito:** Priorizar el servicio de streaming remoto sobre las aplicaciones locales de la laptop.

#### 6. Prioridad de Red (Registry Hack)
* **Acción:** Modificación de `NetworkThrottlingIndex` a [CB-START: REG] ffffffff [CB-END].
* **Ruta:** `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile`
* **Propósito:** Desactivar el estrangulamiento de red de Windows para mantener la fluidez del stream bajo carga de CPU.

#### 7. Privacidad y AppX
* **Acción:** Desactivación global de **Aplicaciones en segundo plano**.
* **Propósito:** Reducir el número de procesos activos de ~40 a un estado más minimalista.

#### 8. Privacidad y Apps en Segundo Plano
* **Acción:** Desactivación global del interruptor "Permitir que las aplicaciones se ejecuten en segundo plano" en el menú de Privacidad.
* **Propósito:** Evitar que aplicaciones UWP (Calculadora, Tienda, Mapas) consuman RAM y ciclos de reloj de forma silenciosa, reduciendo el conteo de procesos activos.

#### 9. Optimización de Efectos de Transparencia
* **Acción:** Desactivado el interruptor de "Effects de transparencia" en Configuración > Personalización > Colores.
* **Propósito:** Aligerar la carga de codificación de video para Google Remote Desktop al eliminar el renderizado de capas traslúcidas.

#### 10. Optimización de I/O de Disco (Indexado)
* **Acción:** Desactivación de la casilla "Permitir que los archivos de esta unidad tengan el contenido indizado" en las propiedades del Disco C:.
* **Propósito:** Reducir la latencia de escritura y el trabajo constante del cabezal/controlador de disco, especialmente útil al manejar miles de archivos pequeños en proyectos de desarrollo.

#### 11. Desactivación de Optimización de Entrega
* **Acción:** Apagado del interruptor "Permitir descargas de otros equipos" en Configuración > Actualización y seguridad.
* **Propósito:** Evitar que la laptop use ancho de banda de subida (Upload) y CPU para enviar actualizaciones a terceros, protegiendo la estabilidad del stream de Google Remote Desktop.

#### 12. Limpieza de Interfaz (Widgets y Barra de Tareas)
* **Acción:** Desactivación de "Noticias e intereses" y botones de sistema (Meet Now) mediante clic derecho en la barra de tareas.
* **Propósito:** Reducir el DPC Latency y evitar que el encoder de video tenga que procesar cambios visuales innecesarios en la barra de tareas.

#### 13. Eliminación de Hibernación
* **Acción:** Ejecución del comando [CB-START: CMD] powercfg -h off [CB-END] en terminal como administrador.
* **Propósito:** Liberar entre 4GB y 8GB de espacio en disco (hiberfil.sys) y eliminar ciclos de escritura redundantes en el almacenamiento.

#### 14. Mantenimiento de Temporales y Caché
* **Acción:** Vaciado manual de las carpetas de sistema mediante el comando Ejecutar.
* **Rutas:** [CB-START: PATHS] %temp%, temp, prefetch [CB-END].
* **Propósito:** Limpiar archivos residuales que pueden causar conflictos en el bus de datos y asegurar un estado del sistema más liviano.

