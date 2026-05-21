# P1 — ¿Cuánto pesa tu algoritmo?
**Módulo:** MP0485 Programación · CFGS DAM · 1º curso · RA3**Duración:** 3 sesiones × 50 min · Individual

---

## Objetivo

Medir y comparar el consumo energético de dos implementaciones del mismo algoritmo.
Al finalizar serás capaz de:
- Ejecutar CodeCarbon y leer los resultados de emisiones
- Relacionar la complejidad algorítmica (O(2ⁿ) vs. O(n)) con el consumo de CO₂
- Extrapolar el ahorro de laboratorio a una escala de producción real

---

## Escenario

> *La empresa acaba de adquirir un servicio de análisis de datos que procesa
> 10 millones de peticiones al día. El CTO os pide optimizar el módulo central.
> ¿Cuánto CO₂ ahorraríais con un cambio de implementación?*

El problema concreto: calcular Fibonacci con dos enfoques y medir cuál "pesa" más.

---

## Sesión 1 — Experiencia concreta y primera medición (50 min)

### Antes de ejecutar nada (10 min)
Responde en tu diario de práctica usando la rutina **Veo-Pienso-Me pregunto**:
- **Veo:** Tienes dos funciones que calculan lo mismo. Una usa recursividad, la otra un bucle.
- **Pienso:** ¿Cuál crees que consume más energía? ¿Por qué? Escribe tu hipótesis *antes* de medir.
- **Me pregunto:** ¿Cuánto crees que se diferencia el consumo entre ambas para n=35?

### Instalación del entorno (5 min)
```bash
pip install codecarbon
```
Si no hay internet, el profesor te dará el paquete `.whl`:
```bash
pip install --no-index --find-links=./wheels codecarbon
```

### Ejecución (35 min)
1. Abre el archivo `medicion.py` y léelo completo antes de ejecutar.
2. Ejecuta el script:
   ```bash
   python medicion.py
   ```
3. Anota los resultados en la **Tabla 1** de tu informe para n=30, 33 y 35.

| n | CO₂ recursivo (gCO₂eq) | CO₂ iterativo (gCO₂eq) | Tiempo recursivo (s) | Tiempo iterativo (s) |
|---|----------------------|----------------------|---------------------|---------------------|
| 30 | | | | |
| 33 | | | | |
| 35 | | | | |

> **Resultados de referencia (ejecución real, macOS, España 2023, modelo 15 W CPU × 0,233 gCO₂eq/Wh):**
>
> | n | CO₂ recursivo (gCO₂eq) | CO₂ iterativo (gCO₂eq) | Tiempo rec. (s) | Tiempo ite. (s) | Reducción CO₂ |
> |---|---|---|---|---|---|
> | 30 | 0,099785 | 0,00000210 | 0,1028 | 0,000002 | ~100 % |
> | 33 | 0,400582 | 0,00000093 | 0,4126 | 0,000001 | ~100 % |
> | 35 | 1,046311 | 0,00000085 | 1,0777 | 0,000001 | ~100 % |
>
> **Perfil CPU — Fibonacci recursivo (n=35):**
> ```
> 29 860 704 llamadas a función (2 llamadas primitivas) en 4,853 s
> ```
> Fibonacci(35) iterativo: **35 iteraciones**, < 1 µs.
>
> **Extrapolación 10 M peticiones/día:**
> Ahorro ~10 484 kg CO₂eq/día = **~3 827 toneladas CO₂eq/año**
>
> Si CodeCarbon devuelve `0.000000` para el iterativo (demasiado rápido para medirse),
> ejecuta 100 000 repeticiones y divide entre 100 000.

---

## Sesión 2 — Reflexión y conceptualización (50 min)

### Calcula la reducción de CO₂ (15 min)
Para cada valor de n:
```
Reducción (%) = (CO₂_recursivo - CO₂_iterativo) / CO₂_recursivo × 100
```

### Extrapola a producción (15 min)
El servicio procesa 10 millones de peticiones al día.
```
Ahorro_diario = CO₂_recursivo(n=35) × 10_000_000 - CO₂_iterativo(n=35) × 10_000_000
```
Expresa el resultado en kg y en toneladas CO₂eq/año.

### Puesta en común (10 min)
El docente recoge los datos de toda la clase en la pizarra.
- ¿Los resultados son iguales en todos los equipos? ¿Por qué pueden variar?
- ¿Qué conclusión extraes sobre la variabilidad de la medición energética?

### Ejecuta el perfil de CPU (10 min)
El script ya incluye `cProfile`. Revisa la salida:
- ¿Cuántas llamadas a función hace la versión recursiva para n=35?
- ¿Y la iterativa?
- Anota ambos números en tu informe.

---

## Sesión 3 — Tu propio experimento (50 min)

Ahora diseña **tu propia hipótesis** comparando:
- Ordenación burbuja (O(n²)) vs. `sorted()` de Python (Timsort, O(n log n))

Pasos:
1. Escribe la hipótesis: *"Creo que el algoritmo X consumirá más porque..."*
2. Implementa ambas versiones en `mi_experimento.py` (esqueleto disponible)
3. Mide con CodeCarbon para una lista de 1 000, 5 000 y 10 000 elementos
4. Verifica tu hipótesis con los datos
5. Redacta la conclusión en el informe

---

## Entregable

Informe en PDF con:
1. Hipótesis inicial (antes de medir)
2. Tabla 1 con los datos medidos
3. Cálculo de reducción porcentual
4. Extrapolación a 10 M peticiones/día
5. Gráfico de barras (CO₂ recursivo vs. iterativo para n=30, 33, 35)
6. Resultado del experimento propio con conclusión
7. Reflexión final: *¿Cambiaría esto tu forma de programar? ¿Por qué?*

---

## Criterio de evaluación Green IT ✅
> Consigues y justificas una reducción **> 90 %** en gCO₂eq entre la versión
> recursiva y la iterativa para n=35, y extrapolasas correctamente el ahorro
> a escala de 10 M peticiones/día.
