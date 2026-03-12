---
version: '1.0'
type: info
title: "Taxonomía_y_Estrategia_de_Web_Scraping"
created: 2026-01-20 00:00:00
updated: 2026-02-09 02:08:33.851228
aliases:
- Taxonomía_y_Estrategia_de_Web_Scraping
tags:
- Python
- Scraping
- Arquitectura
- SOLID
- Playwright
- WebData
priority: 3
status: to_read
---
Esta guía técnica define la selección de stack y estrategias de extracción según la complejidad del objetivo, alineada con la **Directiva de Ingeniería Senior**.

---
## 1. Clasificación por Entorno de Ejecución
Determina la eficiencia del consumo de recursos y la velocidad de obtención.
- ### A. Protocol-Based (Stateless Scraping):
    - **Definición:** Peticiones HTTP directas al servidor.
    - **Herramientas:** `httpx` (asíncrono), `requests`, `aiohttp`.
    - **Uso:** Sitios con SSR (Server Side Rendering) o ingeniería inversa de APIs internas (JSON).
    - **Ventaja:** Consumo de recursos mínimo; sin overhead de motor de renderizado.
- ### B. Browser-Based (Stateful/Dynamic Scraping):
    - **Definición:** Uso de navegadores headless para sitios que ejecutan JavaScript (SPA).
    - **Herramientas:** `Playwright` (preferido), `Selenium`.        
    - **Uso:** Interacciones complejas (clics, scrolls), logins con tokens dinámicos.
    - **Desventaja:** Alto impacto en CPU/RAM. Debe ser el _último recurso_.        
---
## 2. Clasificación por Estrategia de Parseo
Determina la precisión y mantenibilidad del código de extracción.
- ### A. Selectores CSS (Vía Rápida):
    - **Librería:** `Selectolax` (Ultra-rápida, basada en C).
    - **Uso:** Estructuras semánticas claras y constantes.        
- ### B. XPath (Vía de Precisión):
    - **Librería:** `Parsel` o `lxml`.        
    - **Uso Senior:** Navegación relacional (padres/hermanos) y lógica basada en contenido de texto.        
---
## 3. Nivel de Seguridad y Evasión
Estrategias para mitigar bloqueos y detección de bots.

| **Nivel**      | **Estrategia**                | **Lógica**                                                       |
| -------------- | ----------------------------- | ---------------------------------------------------------------- |
| **Bajo/Medio** | Rotación de Headers & Proxies | Imitación de `User-Agent` y `Referer` con proxies residenciales. |
| **Alto**       | Anti-Fingerprinting           | Uso de `Playwright Stealth` para ocultar `navigator.webdriver`.  |

---
## 4. Implementación bajo Estándares SOLID
1. **Modularización:** Separar `http_client.py` (red) de `parsers.py` (lógica de extracción).    
2. **Validación (Pydantic):** Forzar tipos de datos (int, float, datetime) inmediatamente después del parseo.
3. **Inyección de Dependencias:** El cliente de red se inyecta al extractor para permitir **Unit Testing** con mocks.
---
## 5. Checklist de Selección (Hitos)
- [ ] **¿Existe endpoint JSON?** Si es así, priorizar `httpx`.
- [ ] **¿HTML Estático?** Implementar con `Selectolax`.
- [ ] **¿Requiere Interacción?** Implementar con `Playwright`.
- [ ] **¿Data inconsistente?** Usar `XPath` + validación estricta con `Pydantic`.