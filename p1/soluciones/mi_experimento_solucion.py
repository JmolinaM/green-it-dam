"""
mi_experimento_solucion.py — P1: Solución de referencia (sesión 3)

Versión completa del experimento burbuja vs. Timsort con hipótesis,
medición y conclusión redactadas.
"""

import random
import time
import os

from codecarbon import EmissionsTracker

os.makedirs("emisiones", exist_ok=True)


# ── Implementaciones ──────────────────────────────────────────────────────────

def ordenacion_burbuja(lista: list) -> list:
    """Ordenación burbuja. Complejidad: O(n²)."""
    resultado = lista.copy()
    n = len(resultado)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if resultado[j] > resultado[j + 1]:
                resultado[j], resultado[j + 1] = resultado[j + 1], resultado[j]
    return resultado


def ordenacion_python(lista: list) -> list:
    """Ordenación con sorted() de Python (Timsort). Complejidad: O(n log n)."""
    return sorted(lista)


# ── Medición ──────────────────────────────────────────────────────────────────

def medir(func, datos: list, nombre: str) -> dict:
    tracker = EmissionsTracker(
        project_name=nombre,
        output_dir="./emisiones",
        country_iso_code="ESP",
        log_level="warning",
        offline=True,
    )
    t0 = time.perf_counter()
    tracker.start()
    resultado = func(datos)
    emisiones_kg = tracker.stop()
    t1 = time.perf_counter()

    return {
        "n": len(datos),
        "emisiones_gCO2eq": emisiones_kg * 1_000,
        "tiempo_s": t1 - t0,
        "correcto": resultado == sorted(datos),
    }


# ── Hipótesis ─────────────────────────────────────────────────────────────────

HIPOTESIS = """
La ordenación burbuja consumirá más CO₂ y tardará más tiempo que sorted() de Python
porque su complejidad es O(n²): para n=10 000, hace ~50 millones de comparaciones,
mientras que Timsort hace como máximo ~130 000 (n log₂n ≈ 13,3 × 10 000).
La diferencia debería ser especialmente visible para n=10 000.
"""

if __name__ == "__main__":
    print("HIPÓTESIS INICIAL:")
    print(HIPOTESIS)
    print()

    for N in [1_000, 5_000, 10_000]:
        datos = random.sample(range(N * 10), N)

        d_burbuja = medir(ordenacion_burbuja, datos, f"burbuja_n{N}")
        d_python  = medir(ordenacion_python,  datos, f"timsort_n{N}")

        if d_burbuja["emisiones_gCO2eq"] > 0:
            reduccion_co2 = (
                (d_burbuja["emisiones_gCO2eq"] - d_python["emisiones_gCO2eq"])
                / d_burbuja["emisiones_gCO2eq"] * 100
            )
        else:
            reduccion_co2 = 0.0

        reduccion_t = (
            (d_burbuja["tiempo_s"] - d_python["tiempo_s"])
            / d_burbuja["tiempo_s"] * 100
        )

        print(f"n = {N:>6}  |  Burbuja: {d_burbuja['tiempo_s']:.4f}s "
              f"{d_burbuja['emisiones_gCO2eq']:.6f} gCO₂  |  "
              f"Timsort: {d_python['tiempo_s']:.6f}s "
              f"{d_python['emisiones_gCO2eq']:.6f} gCO₂  |  "
              f"Reducción tiempo: {reduccion_t:.1f}%  CO₂: {reduccion_co2:.1f}%")
        print(f"         Resultados correctos — burbuja: {d_burbuja['correcto']}, "
              f"timsort: {d_python['correcto']}")

    print("""
CONCLUSIÓN:
La hipótesis se cumple. Para n=10 000, la ordenación burbuja es ~100-1000× más lenta
que Timsort y genera proporcionalmente más emisiones de CO₂. La diferencia de complejidad
algorítmica se traduce directamente en impacto ambiental medible.
Un servicio que procesa 1 M de ordenaciones al día con burbuja en lugar de Timsort
podría generar varias toneladas de CO₂eq extra al año.
""")
