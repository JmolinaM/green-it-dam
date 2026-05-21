"""
P3 — Datos que cuestan energía (RA5)
Genera un dataset IoT sintético de 1 000 000 de filas para comparar carga completa vs. streaming.

Uso:
    python generar_dataset.py
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd

TOTAL_FILAS = 1_000_000
CHUNK_SIZE = 100_000
TOTAL_SENSORES = 50
SALIDA = Path(__file__).resolve().parent / "datos_sensores.csv"
FECHA_BASE = np.datetime64("2025-01-01T00:00:00")


def generar_chunk(inicio: int, tamano: int, rng: np.random.Generator) -> pd.DataFrame:
    """Genera un bloque de datos apoyándose en NumPy para minimizar el tiempo de creación."""
    segundos = np.arange(inicio, inicio + tamano, dtype=np.int64)
    timestamps = np.char.add(
        np.datetime_as_string(
            FECHA_BASE + segundos.astype("timedelta64[s]"),
            unit="ms",
        ),
        "+00:00",
    )
    sensor_id = rng.integers(1, TOTAL_SENSORES + 1, size=tamano)
    temperatura = rng.uniform(15.0, 35.0, size=tamano).round(2)
    co2_ppm = rng.uniform(400.0, 2000.0, size=tamano).round(2)
    humedad = rng.uniform(30.0, 80.0, size=tamano).round(2)

    return pd.DataFrame(
        {
            "timestamp": timestamps,
            "sensor_id": sensor_id,
            "temperatura": temperatura,
            "co2_ppm": co2_ppm,
            "humedad": humedad,
        }
    )


def main() -> None:
    rng = np.random.default_rng(seed=42)
    SALIDA.parent.mkdir(exist_ok=True)
    if SALIDA.exists():
        SALIDA.unlink()

    total_chunks = math.ceil(TOTAL_FILAS / CHUNK_SIZE)
    print(f"Generando {TOTAL_FILAS:,} filas en {SALIDA.name}...")

    for indice, inicio in enumerate(range(0, TOTAL_FILAS, CHUNK_SIZE), start=1):
        tamano = min(CHUNK_SIZE, TOTAL_FILAS - inicio)
        chunk = generar_chunk(inicio=inicio, tamano=tamano, rng=rng)
        chunk.to_csv(
            SALIDA,
            mode="a",
            index=False,
            header=indice == 1,
            float_format="%.5f",
        )
        progreso = ((inicio + tamano) / TOTAL_FILAS) * 100
        print(
            f"  [{indice:>2}/{total_chunks}] {inicio + tamano:>9,}/{TOTAL_FILAS:,} filas "
            f"({progreso:5.1f} %)"
        )

    tamano_mb = SALIDA.stat().st_size / (1024 * 1024)
    print(f"\nDataset generado correctamente: {SALIDA}")
    print(f"Tamaño aproximado: {tamano_mb:.2f} MB")


if __name__ == "__main__":
    main()
