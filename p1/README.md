# P1 — ¿Cuánto pesa tu algoritmo? (Medir · RA3)

Gamificación de retos algorítmicos con medición de CO₂ usando **CodeCarbon**.

## Duración

2 sesiones × 50 min

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `fib_recursivo.py` | Fibonacci recursivo O(2ⁿ) — versión inicial |
| `fib_iterativo.py` | Fibonacci iterativo O(n) — versión optimizada |
| `medicion.py` | Script de medición con CodeCarbon para ambas versiones |

## Instalación

```
pip install codecarbon==2.3.4
```

## Uso

```
python medicion.py
```

El script genera una tabla comparativa de emisiones (gCO₂eq) para n ∈ {10, 20, 30}.
