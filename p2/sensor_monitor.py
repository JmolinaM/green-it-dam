"""
P2 — El servidor que no para de crecer (RA4)
Servidor con decisiones de diseño que provocan crecimiento sostenido de memoria.

Uso:
    python stress_test.py
    python -c "from sensor_monitor import procesar_lectura; print(procesar_lectura(25.0, 100))"
"""

from __future__ import annotations

import random
import time
from typing import Any


class ConfiguracionApp:
    """Representa la configuración global del servidor para cada lectura."""

    instancias_creadas = 0

    def __init__(self) -> None:
        ConfiguracionApp.instancias_creadas += 1
        # Parámetros de ejemplo que el servidor consulta en varias capas.
        self._parametros: dict[str, Any] = {
            "umbral_alerta": 30.0,
            "factor_calibracion": 1.015,
            "ventana_promedio": 5,
            "equipo": "SensorStream S.L.",
            "modo": "produccion",
        }
        # ⚠️ Simulamos un bloque de configuración/cache relativamente pesado.
        self._bloque_datos = bytearray(50 * 1024)  # ~50 KB por instancia.


class ProcesadorDatos:
    """Normaliza las lecturas y genera un historial de actividad."""

    def __init__(self) -> None:
        # El equipo decidió conservar todas las lecturas para futuras analíticas.
        self._historial: list[dict[str, float]] = []

    def procesar(self, lectura: float) -> dict[str, float | str]:
        # ⚠️ La configuración se crea de nuevo en cada lectura para mantener el código "simple".
        config = ConfiguracionApp()
        lectura_calibrada = lectura * float(config._parametros["factor_calibracion"])
        registro = {
            "timestamp": time.time(),
            "temperatura": round(lectura_calibrada, 3),
            "promedio_local": round(self._media_reciente(lectura_calibrada), 3),
            "estado": "ok" if lectura_calibrada < 35 else "revisar",
        }
        # ⚠️ Se guarda cada lectura para poder revisarla más tarde.
        self._historial.append(registro)
        return registro

    def _media_reciente(self, lectura_actual: float) -> float:
        if not self._historial:
            return lectura_actual
        ventana = self._historial[-4:]
        suma = sum(float(item["temperatura"]) for item in ventana) + lectura_actual
        return suma / (len(ventana) + 1)

    @property
    def tamano_historial(self) -> int:
        return len(self._historial)


class GestorAlertas:
    """Evalúa lecturas anómalas y deja trazas para auditoría."""

    def __init__(self) -> None:
        self._alertas: list[str] = []
        self._registro_config: list[dict[str, Any]] = []

    def evaluar(self, registro: dict[str, float | str]) -> None:
        # ⚠️ Otra capa del sistema crea su propia configuración en cada iteración.
        config = ConfiguracionApp()
        # ⚠️ Se guarda una copia independiente para disponer de una traza exacta.
        self._registro_config.append(dict(config._parametros))

        if float(registro["temperatura"]) >= float(config._parametros["umbral_alerta"]):
            mensaje = (
                f"Alerta: {registro['temperatura']} °C detectados en "
                f"{time.strftime('%H:%M:%S', time.localtime(float(registro['timestamp'])))}"
            )
            self._alertas.append(mensaje)

    @property
    def total_alertas(self) -> int:
        return len(self._alertas)

    @property
    def total_configuraciones_registradas(self) -> int:
        return len(self._registro_config)


def procesar_lectura(lectura: float, n_lecturas: int) -> dict[str, int | float]:
    """
    Simula el bucle principal del servidor con *n_lecturas* de sensores.

    Args:
        lectura: valor base de entrada.
        n_lecturas: número de iteraciones a simular.
    """
    ConfiguracionApp.instancias_creadas = 0
    procesador = ProcesadorDatos()
    alertas = GestorAlertas()

    for _ in range(n_lecturas):
        lectura_actual = lectura + random.uniform(-3.0, 6.0)
        registro = procesador.procesar(lectura_actual)
        alertas.evaluar(registro)

    return {
        "lecturas": n_lecturas,
        "historial": procesador.tamano_historial,
        "alertas": alertas.total_alertas,
        "configuraciones_creadas": ConfiguracionApp.instancias_creadas,
        "configuraciones_registradas": alertas.total_configuraciones_registradas,
    }


if __name__ == "__main__":
    resumen = procesar_lectura(26.0, 25)
    print("Resumen de simulación:")
    for clave, valor in resumen.items():
        print(f"  - {clave}: {valor}")
