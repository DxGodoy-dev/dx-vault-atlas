---
tags: []
source: ia
created: 20-01-2026
updated: 2026-02-09 02:05:06.650234
version: '1.0'
type: ref
---
## Guía Técnica de Alto Rendimiento

El método **CFOP** (acrónimo de Cross, F2L, OLL, PLL) es el estándar de ingeniería para la resolución veloz del cubo de Rubik 3x3. Su arquitectura se basa en la reducción de pasos mediante el procesamiento masivo de algoritmos y la optimización del reconocimiento visual.

### 1. Cross (Cruz) - [Fase de Cimentación]

- **Metodología:** Construcción de una cruz (generalmente blanca) en la cara inferior (D-face).
- **Cantidad de Algoritmos:** 0 (Es 100% intuitivo).    
- **Hito Técnico:** Debe resolverse en **8 movimientos o menos** y ejecutarse sin mirar (blindfolded) tras la inspección.    
- **Objetivo Senior:** Realizar la cruz en la base para facilitar el _look-ahead_ de la siguiente fase.    

### 2. F2L (First Two Layers) - [Fase de Eficiencia]

- **Metodología:** Resolución simultánea de la esquina de la primera capa y su arista correspondiente de la segunda capa, formando un "par".    
- **Cantidad de Algoritmos:** 41 casos básicos (aunque se recomienda el enfoque intuitivo).    
- **Hito Técnico:** Minimizar las rotaciones del cubo (cube rotations) y usar _finger tricks_ para maximizar el TPS.
- **Variantes Avanzadas:** - _Multislotting_: Insertar un par mientras se prepara el siguiente.    
    - _Keyhole_: Insertar aristas usando huecos de esquinas no resueltas.        

### 3. OLL (Orientation of the Last Layer) - [Fase de Orientación]

- **Metodología:** Orientar todas las piezas de la última capa para que el color superior sea uniforme.    
- **Cantidad de Algoritmos:** 57 algoritmos.    
- **Subdivisión:**    
    - **2-Look OLL:** 10 algoritmos (para nivel intermedio).      
    - **Full OLL:** 57 algoritmos (para nivel profesional).        

### 4. PLL (Permutation of the Last Layer) - [Fase de Cierre]

- **Metodología:** Permutar las piezas de la última capa entre sí para finalizar el cubo, manteniendo la orientación ganada en el OLL.
- **Cantidad de Algoritmos:** 21 algoritmos.    
- **Hito Técnico:** Reconocimiento instantáneo basado en los "bloques" o "luces" de colores en las caras laterales.    

### Resumen de Carga Cognitiva

|**Paso**|**Naturaleza**|**Algoritmos**|**Movimientos (Avg)**|
|---|---|---|---|
|**Cross**|Intuitivo|0|6-8|
|**F2L**|Intuitivo/Alg|41|28-32|
|**OLL**|Algorítmico|57|9-12|
|**PLL**|Algorítmico|21|12-15|
|**Total**||**119**|**~55-60**|

---

### Checkboxes de Progreso

- [ ] Dominar la Cruz en la cara inferior en menos de 8 movimientos.
- [ ] Implementar F2L intuitivo sin rotaciones innecesarias de cubo (y o y').    
- [ ] Memorizar los 21 algoritmos de Full PLL.    
- [ ] Transición de 2-Look OLL a Full OLL (57 algos).    
- [ ] Desarrollar _Look-ahead_ (predecir el siguiente par mientras ejecutas el actual).

---

**Ruta de aprendizaje:** [[Ruta_Maestra_Full_CFOP]]