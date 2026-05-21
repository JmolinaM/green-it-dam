"""
P3 — Datos que cuestan energía (RA5)
Versión ineficiente: carga el CSV completo en memoria con pandas.

Uso:
    python carga_mala.py
"""

from __future__ import annotations

import platform
import time
import tracemalloc
from pathlib import Path
from typing import Callable

import pandas as pd

CPU_POWER_W = 15.0
CARBON_INTENSITY_G_PER_WH = 0.233
DATASET = Path(__file__).resolve().parent / "datos_sensores.csv"
_USE_CODECARBON = platform.system() != "Darwin"
if _USE_CODECARBON:
    try:
        from codecarbon import EmissionsTracker
    except ImportError:
        _USE_CODECARBON = False


def estimar_co2(tiempo_s: float) -> float:
    energia_wh = CPU_POWER_W * (tiempo_s / 3600)
    return energia_wh * CARBON_INTENSITY_G_PER_WH


def medir(nombre: str, funcion: Callable[[], dict[str, dict[str, float]]]) -> tuple[dict[str, dict[str, float]], dict[str, float | str]]:
    tracker = None
    fuente = "modelo estimado"
    emisiones_g = 0.0

    tracemalloc.start()
    t0 = time.perf_counter()
    try:
        if _USE_CODECARBON:
            tracker = EmissionsTracker(
                project_name=nombre,
                output_dir=str(DATASET.parent / "emisiones"),
                log_level="error",
            )
            tracker.start()
            fuente = "CodeCarbon"
        resultado = funcion()
    finally:
        t1 = time.perf_counter()
        _, pico = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        if tracker is not None:
            try:
                emisiones_g = float(tracker.stop() or 0.0) * 1000
            except Exception:
                emisiones_g = estimar_co2(t1 - t0)
                fuente = "modelo estimado"
        else:
            emisiones_g = estimar_co2(t1 - t0)

    metadatos: dict[str, float | str] = {
        "tiempo_s": t1 - t0,
        "pico_ram_mb": pico / (1024 * 1024),
        "emisiones_gco2eq": emisiones_g,
        "fuente": fuente,
    }
    return resultado, metadatos


def calcular_estadisticas_completas(ruta_csv: Path = DATASET) -> dict[str, dict[str, float]]:
    """Carga el dataset completo y calcula media, desviación típica, mínimo y máximo."""
    if not ruta_csv.exists():
        raise FileNotFoundError(f"No existe {ruta_csv}. Ejecuta antes: python generar_dataset.py")

    df = pd.read_csv(ruta_csv)
    resultado: dict[str, dict[str, float]] = {}
    for columna in ["temperatura", "co2_ppm"]:
        serie = df[columna]
        resultado[columna] = {
            "mean": float(serie.mean()),
            "std": float(serie.std(ddof=1)),
            "min": float(serie.min()),
            "max": float(serie.max()),
        }
    return resultado


def imprimir_resultados(estadisticas: dict[str, dict[str, float]], metadatos: dict[str, float | str]) -> None:
    print("\nP3 — Carga completa (O(n) en memoria)")
    print("=" * 70)
    for columna, datos in estadisticas.items():
        print(
            f"{columna:<12} → media={datos['mean']:.3f} | std={datos['std']:.3f} | "
            f"mín={datos['min']:.3f} | máx={datos['max']:.3f}"
        )
    print("-" * 70)
    print(f"Tiempo:   {float(metadatos['tiempo_s']):.4f} s")
    print(f"Pico RAM: {float(metadatos['pico_ram_mb']):.3f} MB")
    print(f"CO₂eq:    {float(metadatos['emisiones_gco2eq']):.6f} g ({metadatos['fuente']})")


def main() -> None:
    estadisticas, metadatos = medir("p3_carga_mala", lambda: calcular_estadisticas_completas(DATASET))
    imprimir_resultados(estadisticas, metadatos)


if __name__ == "__main__":
    main()
