"""
P4 — La cola verde (RA9)
Cliente simple para Electricity Maps con modo offline automático.

Uso:
    python -c "from electricity_maps import obtener_intensidad_carbono; print(obtener_intensidad_carbono())"
"""

from __future__ import annotations

import os
from datetime import datetime

import requests

API_URL = "https://api.electricitymap.org/v3/carbon-intensity/latest"


def _simular_intensidad(hora: int | None = None) -> float:
    """Modelo simple de intensidad de carbono según la franja horaria."""
    hora = datetime.now().hour if hora is None else hora
    if 0 <= hora < 6:
        return 105.0
    if 6 <= hora < 10:
        return 180.0
    if 10 <= hora < 16:
        return 125.0
    if 16 <= hora < 19:
        return 210.0
    if 19 <= hora < 23:
        return 295.0
    return 160.0


def obtener_intensidad_carbono(zona: str = "ES") -> float:
    """Consulta la API real y, si falla, devuelve una intensidad simulada."""
    token = os.getenv("ELECTRICITY_MAPS_TOKEN")
    if not token:
        return _simular_intensidad()

    try:
        respuesta = requests.get(
            API_URL,
            params={"zone": zona},
            headers={"auth-token": token, "Authorization": f"Bearer {token}"},
            timeout=5,
        )
        respuesta.raise_for_status()
        datos = respuesta.json()
        intensidad = datos.get("carbonIntensity") or datos.get("carbonIntensityForecast")
        if intensidad is None:
            raise ValueError("Respuesta sin carbonIntensity")
        return float(intensidad)
    except Exception:
        return _simular_intensidad()


if __name__ == "__main__":
    print(f"Intensidad actual estimada para ES: {obtener_intensidad_carbono():.1f} gCO₂eq/kWh")
