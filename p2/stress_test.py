"""
P2 — El servidor que no para de crecer (RA4)
Ejecuta una prueba de estrés con tracemalloc y estima las emisiones asociadas.

Uso:
    python stress_test.py
"""

from __future__ import annotations

import csv
import os
import platform
import time
import tracemalloc
from pathlib import Path
from typing import Callable

from sensor_monitor import procesar_lectura

CPU_POWER_W = 15.0
CARBON_INTENSITY_G_PER_WH = 0.233
ESCENARIOS = [100, 500, 1000]
EMISIONES_DIR = Path(__file__).resolve().parent / "emisiones"
CSV_SALIDA = EMISIONES_DIR / "stress_results.csv"

_USE_CODECARBON = platform.system() != "Darwin"
if _USE_CODECARBON:
    try:
        from codecarbon import EmissionsTracker
    except ImportError:
        _USE_CODECARBON = False


def estimar_co2(tiempo_s: float) -> float:
    """Convierte tiempo de CPU estimado a gramos de CO₂eq."""
    energia_wh = CPU_POWER_W * (tiempo_s / 3600)
    return energia_wh * CARBON_INTENSITY_G_PER_WH


def medir_emisiones(nombre: str, funcion: Callable[[], dict[str, int | float]]) -> dict[str, object]:
    """Mide tiempo, RAM y emisiones con CodeCarbon o con el modelo estimado."""
    tracker = None
    fuente = "modelo estimado"
    emisiones_g = 0.0

    tracemalloc.start()
    t0 = time.perf_counter()
    try:
        if _USE_CODECARBON:
            tracker = EmissionsTracker(
                project_name=nombre,
                output_dir=str(EMISIONES_DIR),
                log_level="error",
            )
            tracker.start()
            fuente = "CodeCarbon"
        resumen = funcion()
    finally:
        t1 = time.perf_counter()
        actual, pico = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        if tracker is not None:
            try:
                emisiones_g = float(tracker.stop() or 0.0) * 1000
            except Exception:
                emisiones_g = estimar_co2(t1 - t0)
                fuente = "modelo estimado"
        else:
            emisiones_g = estimar_co2(t1 - t0)

    return {
        "tiempo_s": t1 - t0,
        "memoria_actual_mb": actual / (1024 * 1024),
        "pico_ram_mb": pico / (1024 * 1024),
        "emisiones_gco2eq": emisiones_g,
        "fuente": fuente,
        **resumen,
    }


def exportar_csv(resultados: list[dict[str, object]]) -> None:
    EMISIONES_DIR.mkdir(exist_ok=True)
    with CSV_SALIDA.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "n",
                "lecturas",
                "historial",
                "alertas",
                "configuraciones_creadas",
                "configuraciones_registradas",
                "tiempo_s",
                "memoria_actual_mb",
                "pico_ram_mb",
                "emisiones_gco2eq",
                "fuente",
            ],
        )
        writer.writeheader()
        for resultado in resultados:
            writer.writerow(resultado)


def imprimir_tabla(resultados: list[dict[str, object]]) -> None:
    ancho = 88
    print("\n" + "═" * ancho)
    print("P2 — Estrés del servidor con tracemalloc".center(ancho))
    print("═" * ancho)
    print(f"{'n':>8} | {'Pico RAM (MB)':>14} | {'Tiempo (s)':>10} | {'CO₂eq (g)':>11} | {'Config.':>8}")
    print("-" * ancho)
    for fila in resultados:
        print(
            f"{int(fila['n']):>8} | {float(fila['pico_ram_mb']):>14.3f} | "
            f"{float(fila['tiempo_s']):>10.4f} | {float(fila['emisiones_gco2eq']):>11.6f} | "
            f"{int(fila['configuraciones_creadas']):>8}"
        )
    print("-" * ancho)
    print("Modelo CO₂: 15 W × tiempo × 0,233 gCO₂eq/Wh (fallback automático en macOS).")
    print(f"CSV exportado en: {CSV_SALIDA}")


def main() -> None:
    os.makedirs(EMISIONES_DIR, exist_ok=True)
    resultados: list[dict[str, object]] = []

    for n in ESCENARIOS:
        medicion = medir_emisiones(
            nombre=f"sensor_stream_n{n}",
            funcion=lambda n=n: procesar_lectura(26.5, n),
        )
        medicion["n"] = n
        resultados.append(medicion)

    imprimir_tabla(resultados)
    exportar_csv(resultados)


if __name__ == "__main__":
    main()
