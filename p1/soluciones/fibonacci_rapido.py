"""
fibonacci_rapido.py — P1: ¿Cuánto pesa tu algoritmo?  (Sesión 2 · Solución)

Versión optimizada de fibonacci_lento.py con las tres mejoras aplicadas:

  ✅  Mejora 1: eliminado time.sleep()       → sin log por llamada
  ✅  Mejora 2: eliminado int(str(n))        → sin conversión innecesaria
  ✅  Mejora 3: implementación iterativa     → O(n) en lugar de O(2^n)

Compara los resultados de la Ficha P1 con los de fibonacci_lento.py.
"""

import sys
import time
import platform
import os

os.makedirs("emisiones", exist_ok=True)

CPU_POWER_W = 15.0
CARBON_INTENSITY_gCO2_PER_Wh = 0.233

_USE_CODECARBON = platform.system() != "Darwin"
if _USE_CODECARBON:
    try:
        from codecarbon import EmissionsTracker
    except ImportError:
        _USE_CODECARBON = False


def fibonacci_rapido(n: int) -> int:
    """
    Implementación iterativa de Fibonacci. Complejidad: O(n), espacio: O(1).
    Sin sleep, sin conversión de cadena.
    """
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def medir_fibonacci(n: int) -> dict:
    if _USE_CODECARBON:
        t0 = time.perf_counter()
        try:
            tracker = EmissionsTracker(
                project_name=f"fib_rapido_n{n}",
                output_dir="./emisiones",
                log_level="error",
            )
            tracker.start()
            resultado = fibonacci_rapido(n)
            emisiones_kg = tracker.stop()
            t1 = time.perf_counter()
            fuente = "CodeCarbon"
        except Exception:
            t0 = time.perf_counter()
            resultado = fibonacci_rapido(n)
            t1 = time.perf_counter()
            energia_Wh = CPU_POWER_W * ((t1 - t0) / 3600)
            emisiones_kg = energia_Wh * CARBON_INTENSITY_gCO2_PER_Wh / 1000
            fuente = "modelo estimado"
    else:
        t0 = time.perf_counter()
        resultado = fibonacci_rapido(n)
        t1 = time.perf_counter()
        energia_Wh = CPU_POWER_W * ((t1 - t0) / 3600)
        emisiones_kg = energia_Wh * CARBON_INTENSITY_gCO2_PER_Wh / 1000
        fuente = "modelo estimado"

    return {
        "n": n,
        "resultado": resultado,
        "tiempo_s": t1 - t0,
        "emisiones_gCO2eq": emisiones_kg * 1_000,
        "fuente": fuente,
    }


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 35

    print(f"\n  🚀 fibonacci_rapido({n}) — versión optimizada (Mejora 3 completa)")

    datos = medir_fibonacci(n)

    print(f"  Resultado      : fibonacci({n}) = {datos['resultado']}")
    print(f"  Tiempo         : {datos['tiempo_s']:.6f} s")
    if datos['emisiones_gCO2eq'] < 0.001:
        print(f"  Emisiones CO₂  : {datos['emisiones_gCO2eq']:.3e} gCO₂eq  [{datos['fuente']}]")
    else:
        print(f"  Emisiones CO₂  : {datos['emisiones_gCO2eq']:.6f} gCO₂eq  [{datos['fuente']}]")
    print()
    print("  → Anota en la Ficha P1 (fila 'Mejora 3: versión iterativa').")
    print("  → Calcula la reducción total respecto al DATO BASE.")
    print()
