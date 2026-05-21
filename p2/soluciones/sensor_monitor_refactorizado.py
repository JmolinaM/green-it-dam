"""
P2 — El servidor que no para de crecer (RA4)
Solución docente con una combinación de estrategias de refactorización.

Uso:
    python soluciones/sensor_monitor_refactorizado.py
"""

from __future__ import annotations

import random
import time
from collections import deque
from typing import Any


class ConfiguracionApp:
    """Singleton: una única configuración compartida por todo el proceso."""

    _instancia: "ConfiguracionApp | None" = None

    def __new__(cls) -> "ConfiguracionApp":
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def __init__(self) -> None:
        if getattr(self, "_inicializada", False):
            return
        self._parametros: dict[str, Any] = {
            "umbral_alerta": 30.0,
            "factor_calibracion": 1.015,
            "ventana_promedio": 5,
            "equipo": "SensorStream S.L.",
            "modo": "produccion",
        }
        self._bloque_datos = bytearray(50 * 1024)
        self._inicializada = True


class ProcesadorDatos:
    """Mantiene un historial acotado para evitar crecimiento lineal."""

    def __init__(self, config: ConfiguracionApp, max_historial: int = 200) -> None:
        self._config = config
        self._historial: deque[dict[str, float | str]] = deque(maxlen=max_historial)

    def procesar(self, lectura: float) -> dict[str, float | str]:
        lectura_calibrada = lectura * float(self._config._parametros["factor_calibracion"])
        registro = {
            "timestamp": time.time(),
            "temperatura": round(lectura_calibrada, 3),
            "promedio_local": round(self._media_reciente(lectura_calibrada), 3),
            "estado": "ok" if lectura_calibrada < 35 else "revisar",
        }
        self._historial.append(registro)
        return registro

    def _media_reciente(self, lectura_actual: float) -> float:
        if not self._historial:
            return lectura_actual
        suma = sum(float(item["temperatura"]) for item in self._historial) + lectura_actual
        return suma / (len(self._historial) + 1)

    @property
    def tamano_historial(self) -> int:
        return len(self._historial)


class GestorAlertas:
    """Genera alertas sin almacenar copias crecientes de la configuración."""

    def __init__(self, config: ConfiguracionApp) -> None:
        self._config = config
        self._alertas: list[str] = []

    def evaluar(self, registro: dict[str, float | str]) -> None:
        if float(registro["temperatura"]) >= float(self._config._parametros["umbral_alerta"]):
            mensaje = (
                f"Alerta: {registro['temperatura']} °C detectados en "
                f"{time.strftime('%H:%M:%S', time.localtime(float(registro['timestamp'])))}"
            )
            self._alertas.append(mensaje)

    @property
    def total_alertas(self) -> int:
        return len(self._alertas)


def procesar_lectura(lectura: float, n_lecturas: int) -> dict[str, int | float]:
    """Versión refactorizada: Singleton + deque + eliminación del registro duplicado."""
    config = ConfiguracionApp()
    procesador = ProcesadorDatos(config=config, max_historial=200)
    alertas = GestorAlertas(config=config)

    for _ in range(n_lecturas):
        lectura_actual = lectura + random.uniform(-3.0, 6.0)
        registro = procesador.procesar(lectura_actual)
        alertas.evaluar(registro)

    return {
        "lecturas": n_lecturas,
        "historial": procesador.tamano_historial,
        "alertas": alertas.total_alertas,
        "configuracion_singleton": 1,
    }


if __name__ == "__main__":
    resumen = procesar_lectura(26.0, 1000)
    print("Resumen de la solución refactorizada:")
    for clave, valor in resumen.items():
        print(f"  - {clave}: {valor}")
