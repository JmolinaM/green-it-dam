"""
P4 — La cola verde (RA9)
Demostración de una cola carbon-aware con tres ciclos de ejecución.

Uso:
    python main.py
"""

from __future__ import annotations

import platform
import time
from pathlib import Path

from cola_verde import ColaVerde

CPU_POWER_W = 15.0
CARBON_INTENSITY_G_PER_WH = 0.233
_USE_CODECARBON = platform.system() != "Darwin"
if _USE_CODECARBON:
    try:
        from codecarbon import EmissionsTracker
    except ImportError:
        _USE_CODECARBON = False


def estimar_co2(tiempo_s: float) -> float:
    energia_wh = CPU_POWER_W * (tiempo_s / 3600)
    return energia_wh * CARBON_INTENSITY_G_PER_WH


def simular_ciclos() -> dict[str, object]:
    cola = ColaVerde()
    cola.encolar("Backup de informes", urgente=False, umbral_co2=180)
    cola.encolar("Entrenar modelo", urgente=False, umbral_co2=140)
    cola.encolar("Parche de seguridad", urgente=True, umbral_co2=999)
    cola.encolar("Reindexar búsquedas", urgente=False, umbral_co2=160)
    cola.encolar("Enviar nóminas", urgente=True, umbral_co2=999)

    intensidades = [150.0, 280.0, 120.0]
    historial: list[dict[str, object]] = []

    for ciclo, intensidad in enumerate(intensidades, start=1):
        ejecutadas = cola.ejecutar_pendientes(intensidad)
        historial.append(
            {
                "ciclo": ciclo,
                "intensidad": intensidad,
                "ejecutadas": [tarea.nombre for tarea in ejecutadas],
                "pendientes": cola.estadisticas["pendientes"],
            }
        )

    return {"historial": historial, "estadisticas": cola.estadisticas}


def main() -> None:
    tracker = None
    fuente = "modelo estimado"
    salida_emisiones = Path(__file__).resolve().parent / "emisiones"
    salida_emisiones.mkdir(exist_ok=True)

    t0 = time.perf_counter()
    if _USE_CODECARBON:
        try:
            tracker = EmissionsTracker(project_name="p4_demo", output_dir=str(salida_emisiones), log_level="error")
            tracker.start()
            fuente = "CodeCarbon"
        except Exception:
            tracker = None
            fuente = "modelo estimado"

    resultado = simular_ciclos()
    t1 = time.perf_counter()

    if tracker is not None:
        try:
            emisiones_g = float(tracker.stop() or 0.0) * 1000
        except Exception:
            emisiones_g = estimar_co2(t1 - t0)
            fuente = "modelo estimado"
    else:
        emisiones_g = estimar_co2(t1 - t0)

    print("\nP4 — Demo de ColaVerde")
    print("=" * 60)
    for ciclo in resultado["historial"]:
        print(
            f"Ciclo {ciclo['ciclo']}: intensidad={ciclo['intensidad']:.0f} gCO₂eq/kWh | "
            f"ejecutadas={ciclo['ejecutadas']} | pendientes={ciclo['pendientes']}"
        )
    print("-" * 60)
    print(f"Estadísticas finales: {resultado['estadisticas']}")
    print(f"Tiempo total: {t1 - t0:.4f} s")
    print(f"CO₂eq estimado: {emisiones_g:.6f} g ({fuente})")


if __name__ == "__main__":
    main()
