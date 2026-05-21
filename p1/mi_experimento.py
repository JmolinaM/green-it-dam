"""
mi_experimento.py — P1: Sesión 3 (experimento propio)

Esqueleto para comparar burbuja O(n²) vs. Timsort O(n log n).
Completa las partes marcadas con TODO.
"""

import random
import time
import os

from codecarbon import EmissionsTracker

os.makedirs("emisiones", exist_ok=True)


# ── Implementaciones ──────────────────────────────────────────────────────────

def ordenacion_burbuja(lista: list) -> list:
    """
    Ordenación burbuja. Complejidad: O(n²).
    TODO: implementa el algoritmo de burbuja aquí.
    """
    resultado = lista.copy()
    # TODO: escribe aquí el bucle de burbuja
    return resultado


def ordenacion_python(lista: list) -> list:
    """
    Ordenación con sorted() de Python (Timsort). Complejidad: O(n log n).
    No modificar: ya está implementada.
    """
    return sorted(lista)


# ── Medición ──────────────────────────────────────────────────────────────────

def medir(func, datos: list, nombre: str) -> dict:
    """Mide tiempo y emisiones CO₂ de la función de ordenación."""
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
        "correcto": resultado == sorted(datos),   # verificación de corrección
    }


# ── Hipótesis (rellena antes de ejecutar) ─────────────────────────────────────

HIPOTESIS = """
TODO: escribe aquí tu hipótesis antes de ejecutar el experimento.

Ejemplo: "Creo que la ordenación burbuja consumirá más CO₂ porque..."
"""


# ── Ejecución principal ───────────────────────────────────────────────────────

if __name__ == "__main__":
    print("HIPÓTESIS INICIAL:")
    print(HIPOTESIS)
    print()

    for N in [1_000, 5_000, 10_000]:
        datos = random.sample(range(N * 10), N)   # lista de N enteros únicos

        d_burbuja = medir(ordenacion_burbuja, datos, f"burbuja_n{N}")
        d_python  = medir(ordenacion_python,  datos, f"timsort_n{N}")

        if d_burbuja["emisiones_gCO2eq"] > 0:
            reduccion = (
                (d_burbuja["emisiones_gCO2eq"] - d_python["emisiones_gCO2eq"])
                / d_burbuja["emisiones_gCO2eq"] * 100
            )
        else:
            reduccion = 0.0

        print(f"n = {N:>6}  |  Burbuja: {d_burbuja['tiempo_s']:.4f}s "
              f"{d_burbuja['emisiones_gCO2eq']:.6f} gCO₂  |  "
              f"Timsort: {d_python['tiempo_s']:.4f}s "
              f"{d_python['emisiones_gCO2eq']:.6f} gCO₂  |  "
              f"Reducción: {reduccion:.1f}%")
        print(f"         Resultados correctos — burbuja: {d_burbuja['correcto']}, "
              f"timsort: {d_python['correcto']}")

    print()
    print("TODO: escribe aquí tu conclusión. ¿Se cumplió la hipótesis?")
