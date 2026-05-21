"""
fibonacci_lento.py — P1: ¿Cuánto pesa tu algoritmo?  (Sesión 2)

Versión LENTA e ineficiente de Fibonacci para la práctica de optimización.
Contiene TRES ineficiencias deliberadas que el alumnado debe identificar y corregir:

  1. time.sleep(0.0001) en cada llamada   → simula un log mal implementado
  2. int(str(n)) en cada llamada          → conversión de cadena inútil
  3. Recursividad sin memoización O(2^n)  → el problema principal

ESCENARIO (empresa ficticia GreenCalc S.L.):
  "Nuestro servicio ejecuta este cálculo 5 millones de veces al día.
   Medidlo, identificad los problemas y corregidlos."

Uso:
    pip install codecarbon
    python fibonacci_lento.py        # ejecuta con n=35
    python fibonacci_lento.py 30     # ejecuta con n=30
"""

import sys
import time
import platform
import os

os.makedirs("emisiones", exist_ok=True)

CPU_POWER_W = 15.0
CARBON_INTENSITY_gCO2_PER_Wh = 0.233   # España 2023 (REE)

_USE_CODECARBON = platform.system() != "Darwin"
if _USE_CODECARBON:
    try:
        from codecarbon import EmissionsTracker
    except ImportError:
        _USE_CODECARBON = False


def fibonacci_lento(n: int) -> int:
    """
    Calcula el n-ésimo número de Fibonacci.

    ⚠️  Esta implementación contiene ineficiencias deliberadas.
        Identifícalas con cProfile antes de corregirlas.
    """
    # Bug 1: pausa en cada llamada (simula un log por llamada mal implementado)
    time.sleep(0.0001)

    # Bug 2: conversión de cadena innecesaria en cada llamada
    n = int(str(n))

    # Bug 3: recursividad sin memoización → O(2^n)
    if n <= 1:
        return n
    return fibonacci_lento(n - 1) + fibonacci_lento(n - 2)


def medir_fibonacci(n: int) -> dict:
    """Mide tiempo y emisiones de fibonacci_lento(n)."""
    if _USE_CODECARBON:
        t0 = time.perf_counter()
        try:
            tracker = EmissionsTracker(
                project_name=f"fib_lento_n{n}",
                output_dir="./emisiones",
                log_level="error",
            )
            tracker.start()
            resultado = fibonacci_lento(n)
            emisiones_kg = tracker.stop()
            t1 = time.perf_counter()
            fuente = "CodeCarbon"
        except Exception:
            t0 = time.perf_counter()
            resultado = fibonacci_lento(n)
            t1 = time.perf_counter()
            energia_Wh = CPU_POWER_W * ((t1 - t0) / 3600)
            emisiones_kg = energia_Wh * CARBON_INTENSITY_gCO2_PER_Wh / 1000
            fuente = "modelo estimado"
    else:
        t0 = time.perf_counter()
        resultado = fibonacci_lento(n)
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

    print(f"\n  🐢 fibonacci_lento({n}) — versión con ineficiencias deliberadas")
    print(f"  Midiendo... (puede tardar varios segundos)\n")

    datos = medir_fibonacci(n)

    print(f"  Resultado      : fibonacci({n}) = {datos['resultado']}")
    print(f"  Tiempo         : {datos['tiempo_s']:.4f} s")
    co2 = datos['emisiones_gCO2eq']
    co2_str = f"{co2:.3e}" if co2 < 0.001 else f"{co2:.6f}"
    print(f"  Emisiones CO₂  : {co2_str} gCO₂eq  [{datos['fuente']}]")
    print()
    print("  → Anota estos valores como DATO BASE en la Ficha P1.")
    print("  → Ahora aplica las mejoras una a una y vuelve a medir.")
    print()
    print("  💡 Pista: usa 'python -m cProfile fibonacci_lento.py' para")
    print("     ver qué función acapara más tiempo.")
    print()
