"""
P4 — La cola verde (RA9)
Esqueleto guiado de una cola de prioridad carbon-aware basada en heapq.

Uso:
    python main.py
    pytest test_cola_verde.py
"""

from __future__ import annotations

import heapq
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TareaProgramada:
    """Representa una tarea pendiente de ejecución."""

    nombre: str
    urgente: bool
    umbral_co2: float
    metadatos: dict[str, Any] | None = None


class ColaVerde:
    """Cola de prioridad que combina urgencia, umbral de CO₂ y orden FIFO."""

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
        """Añade una tarea a la cola priorizando urgencia y preservando FIFO."""
        # TODO alumnado: justificar por qué usamos tuplas (prioridad, contador, tarea)
        # en lugar de almacenar directamente los objetos en heapq.
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
        """Ejecuta tareas urgentes y solo lanza las diferibles si la red está por debajo del umbral."""
        # TODO alumnado: completar el razonamiento de negocio que decide cuándo una tarea
        # se ejecuta y cuándo vuelve a la cola manteniendo su prioridad original.
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
        """Devuelve un resumen del estado de la cola."""
        # TODO alumnado: extender estas métricas con indicadores útiles para el informe.
        return {
            "pendientes": len(self._cola),
            "ejecutadas": self._ejecutadas,
            "diferidas": self._diferidas,
            "ciclos": self._ciclos,
        }
