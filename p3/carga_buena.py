"""
P3 — Datos que cuestan energía (RA5)
Versión eficiente: procesa el CSV por streaming en una sola pasada lógica.

Uso:
    python carga_buena.py
"""

from __future__ import annotations

import math
import platform
import time
import tracemalloc
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import pandas as pd

from carga_mala import calcular_estadisticas_completas

CPU_POWER_W = 15.0
CARBON_INTENSITY_G_PER_WH = 0.233
DATASET = Path(__file__).resolve().parent / "datos_sensores.csv"
CHUNK_SIZE = 10_000
TOLERANCIA = 0.001
_USE_CODECARBON = platform.system() != "Darwin"
if _USE_CODECARBON:
    try:
        from codecarbon import EmissionsTracker
    except ImportError:
        _USE_CODECARBON = False


@dataclass
class AcumuladorColumna:
    """Acumuladores online para media, desviación típica, mínimo y máximo."""

    total: int = 0
    suma: float = 0.0
    suma_cuadrados: float = 0.0
    minimo: float = float("inf")
    maximo: float = float("-inf")

    def actualizar(self, valores) -> None:
        if len(valores) == 0:
            return
        self.total += int(len(valores))
        self.suma += float(valores.sum())
        self.suma_cuadrados += float((valores * valores).sum())
        self.minimo = min(self.minimo, float(valores.min()))
        self.maximo = max(self.maximo, float(valores.max()))

    def resumen(self) -> dict[str, float]:
        media = self.suma / self.total
        varianza_muestral = 0.0
        if self.total > 1:
            numerador = self.suma_cuadrados - ((self.suma**2) / self.total)
            varianza_muestral = max(numerador / (self.total - 1), 0.0)
        return {
            "mean": media,
            "std": math.sqrt(varianza_muestral),
            "min": self.minimo,
            "max": self.maximo,
        }


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


def calcular_estadisticas_streaming(ruta_csv: Path = DATASET, chunksize: int = CHUNK_SIZE) -> dict[str, dict[str, float]]:
    if not ruta_csv.exists():
        raise FileNotFoundError(f"No existe {ruta_csv}. Ejecuta antes: python generar_dataset.py")

    acumuladores = {
        "temperatura": AcumuladorColumna(),
        "co2_ppm": AcumuladorColumna(),
    }

    for chunk in pd.read_csv(ruta_csv, chunksize=chunksize, usecols=["temperatura", "co2_ppm"]):
        for columna, acumulador in acumuladores.items():
            acumulador.actualizar(chunk[columna].to_numpy(dtype="float64", copy=False))

    return {columna: acumulador.resumen() for columna, acumulador in acumuladores.items()}


def verificar_resultados(streaming: dict[str, dict[str, float]], referencia: dict[str, dict[str, float]]) -> None:
    for columna in streaming:
        for estadistico in streaming[columna]:
            diferencia = abs(streaming[columna][estadistico] - referencia[columna][estadistico])
            if diferencia > TOLERANCIA:
                raise AssertionError(
                    f"La verificación ha fallado en {columna}.{estadistico}: "
                    f"diferencia {diferencia:.6f} > {TOLERANCIA}"
                )
    print(f"Verificación correcta: streaming ≈ carga completa (tolerancia {TOLERANCIA}).")


def imprimir_resultados(estadisticas: dict[str, dict[str, float]], metadatos: dict[str, float | str]) -> None:
    print("\nP3 — Carga por streaming (O(k) en memoria)")
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
    estadisticas, metadatos = medir("p3_carga_buena", lambda: calcular_estadisticas_streaming(DATASET))
    imprimir_resultados(estadisticas, metadatos)
    referencia = calcular_estadisticas_completas(DATASET)
    verificar_resultados(estadisticas, referencia)


if __name__ == "__main__":
    main()
