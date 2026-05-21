# P1 — ¿Cuánto pesa tu algoritmo? (Medir · RA3)

Propuesta didáctica de 3 sesiones para medir y comparar el consumo energético
de algoritmos usando **CodeCarbon**. Módulo MP0485 · CFGS DAM · 1.º curso.

## Duración

3 sesiones × 50 min (individual)

## Estructura de archivos

| Archivo | Sesión | Descripción |
|---------|--------|-------------|
| `p1_simple.py` | 1 | Suma del 1 al 1 000 — programa de referencia simple |
| `p1_complejo.py` | 1 | Ordenación + primos + cadenas — programa de referencia complejo |
| `fibonacci_lento.py` | 2 | Fibonacci con **3 bugs deliberados** — dato base |
| `fib_recursivo.py` | — | Fibonacci recursivo limpio (sin bugs artificiales) |
| `fib_iterativo.py` | — | Fibonacci iterativo O(n) — referencia |
| `medicion.py` | — | Comparativa automatizada fib_recursivo vs fib_iterativo |
| `mi_experimento.py` | 3 | Esqueleto: burbuja vs. Timsort (alumno completa los TODO) |
| `GUION.md` | — | Guión completo para el alumnado |
| `soluciones/` | — | Soluciones de referencia (solo para el docente) |

## Los 3 bugs de `fibonacci_lento.py`

| # | Ineficiencia | Por qué está ahí |
|---|-------------|-----------------|
| 1 | `time.sleep(0.0001)` en cada llamada | Simula un log mal implementado |
| 2 | `int(str(n))` en cada llamada | Conversión de cadena inútil |
| 3 | Recursividad sin memoización O(2ⁿ) | El problema principal |

## Instalación

```bash
pip install codecarbon==2.3.4
```

## Flujo de sesiones

```
Sesión 1:  python p1_complejo.py   →  anota en Ficha P1 (columna Complejo)
           python p1_simple.py     →  anota en Ficha P1 (columna Simple)
                                       calcula ratio complejo/simple

Sesión 2:  python fibonacci_lento.py        →  dato base
           # aplica Mejora 1: elimina sleep →  mide de nuevo
           # aplica Mejora 2: elimina int(str(n)) →  mide de nuevo
           # aplica Mejora 3: reescribe iterativo  →  mide de nuevo

Sesión 3:  python mi_experimento.py   (completa los TODO primero)
```

## Soluciones (solo docente)

```
soluciones/fib_iterativo.py          # referencia iterativa limpia
soluciones/fibonacci_rapido.py       # fibonacci_lento con las 3 mejoras aplicadas
soluciones/mi_experimento_solucion.py
```
