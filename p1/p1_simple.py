"""
p1_simple.py — P1: ¿Cuánto pesa tu algoritmo?  (Sesión 1)

Programa simple: suma los números del 1 al 1 000.
El alumnado lo instrumenta con CodeCarbon y anota las emisiones.

Uso:
    pip install codecarbon
    python p1_simple.py
"""

import time
import platform
import os

os.makedirs("emisiones", exist_ok=True)

# ── Constantes para el modelo de estimación (macOS no tiene powermetrics sin sudo) ──
CPU_POWER_W = 15.0
CARBON_INTENSITY_gCO2_PER_Wh = 0.233   # España 2023 (REE)

_USE_CODECARBON = platform.system() != "Darwin"
if _USE_CODECARBON:
    try:
        from codecarbon import EmissionsTracker
    except ImportError:
        _USE_CODECARBON = False


def suma_simple(n: int) -> int:
    """Suma los números del 1 al n con un bucle. Complejidad: O(n)."""
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


if __name__ == "__main__":
    N = 1_000

    if _USE_CODECARBON:
        tracker = EmissionsTracker(
            project_name="p1_simple",
            output_dir="./emisiones",
            log_level="error",
        )
        t0 = time.perf_counter()
        tracker.start()
        resultado = suma_simple(N)
        emisiones_kg = tracker.stop()
        t1 = time.perf_counter()
        fuente = "CodeCarbon"
    else:
        t0 = time.perf_counter()
        resultado = suma_simple(N)
        t1 = time.perf_counter()
        energia_Wh = CPU_POWER_W * ((t1 - t0) / 3600)
        emisiones_kg = energia_Wh * CARBON_INTENSITY_gCO2_PER_Wh / 1000
        fuente = "modelo estimado"

    emisiones_g = emisiones_kg * 1_000

    print(f"\n  🌿 p1_simple.py — Suma del 1 al {N}")
    print(f"  Resultado      : {resultado}")
    print(f"  Tiempo         : {t1 - t0:.6f} s")
    print(f"  Emisiones CO₂  : {emisiones_g:.8f} gCO₂eq  [{fuente}]")
    print()
    print("  → Anota estos valores en la Ficha P1 (columna 'Simple').")
    print("  → Después ejecuta p1_complejo.py y calcula el ratio complejo/simple.")
    print()
