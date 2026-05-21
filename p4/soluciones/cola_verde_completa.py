"""
P4 — La cola verde (RA9)
Solución docente completa de la cola carbon-aware con heapq.

Uso:
    python soluciones/cola_verde_completa.py
"""

from __future__ import annotations

import heapq
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TareaProgramada:
    nombre: str
    urgente: bool
    umbral_co2: float
    metadatos: dict[str, Any] | None = None


class ColaVerde:
    """Implementación completa de una cola green-aware."""

    def __init__(self) -> None:
        self._cola: list[tuple[int, int, TareaProgramada]] = []
        self.counter = 0
        self._ejecutadas = 0
        self._diferidas = 0
        self._ciclos = 0

    def encolar(
        self,
        tarea: str,
        urgente: bool = False,
        umbral_co2: float = 200.0,
        metadatos: dict[str, Any] | None = None,
    ) -> None:
        prioridad = 0 if urgente else 1
        programada = TareaProgramada(
            nombre=tarea,
            urgente=urgente,
            umbral_co2=umbral_co2,
            metadatos=metadatos,
        )
        heapq.heappush(self._cola, (prioridad, self.counter, programada))
        self.counter += 1

    def ejecutar_pendientes(self, intensidad_actual: float) -> list[TareaProgramada]:
        ejecutadas: list[TareaProgramada] = []
        diferidas: list[tuple[int, int, TareaProgramada]] = []
        self._ciclos += 1

        while self._cola:
            prioridad, ticket, tarea = heapq.heappop(self._cola)
            if tarea.urgente or intensidad_actual < tarea.umbral_co2:
                ejecutadas.append(tarea)
            else:
                diferidas.append((prioridad, ticket, tarea))

        for elemento in diferidas:
            heapq.heappush(self._cola, elemento)

        self._ejecutadas += len(ejecutadas)
        self._diferidas += len(diferidas)
        return ejecutadas

    @property
    def estadisticas(self) -> dict[str, int]:
        return {
            "pendientes": len(self._cola),
            "ejecutadas": self._ejecutadas,
            "diferidas": self._diferidas,
            "ciclos": self._ciclos,
        }


if __name__ == "__main__":
    cola = ColaVerde()
    cola.encolar("copias de seguridad", urgente=False, umbral_co2=180.0)
    cola.encolar("parche crítico", urgente=True, umbral_co2=999.0)
    print([t.nombre for t in cola.ejecutar_pendientes(250.0)])
    print(cola.estadisticas)
