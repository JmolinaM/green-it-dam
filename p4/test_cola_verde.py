"""
P4 — La cola verde (RA9)
Tests de comportamiento para la cola carbon-aware.

Uso:
    pytest test_cola_verde.py
"""

from __future__ import annotations

from unittest.mock import patch

from cola_verde import ColaVerde


@patch("electricity_maps.obtener_intensidad_carbono", return_value=120.0)
def test_ejecuta_si_la_intensidad_es_menor_que_el_umbral(mock_intensidad) -> None:
    cola = ColaVerde()
    cola.encolar("informe batch", urgente=False, umbral_co2=180.0)

    ejecutadas = cola.ejecutar_pendientes(mock_intensidad())

    assert [tarea.nombre for tarea in ejecutadas] == ["informe batch"]
    assert cola.estadisticas["pendientes"] == 0


@patch("electricity_maps.obtener_intensidad_carbono", return_value=280.0)
def test_difiere_si_la_intensidad_supera_el_umbral(mock_intensidad) -> None:
    cola = ColaVerde()
    cola.encolar("analítica nocturna", urgente=False, umbral_co2=200.0)

    ejecutadas = cola.ejecutar_pendientes(mock_intensidad())

    assert ejecutadas == []
    assert cola.estadisticas["pendientes"] == 1


@patch("electricity_maps.obtener_intensidad_carbono", side_effect=[180.0, 90.0])
def test_la_tarea_diferida_mantiene_su_prioridad_original(mock_intensidad) -> None:
    cola = ColaVerde()
    cola.encolar("A", urgente=False, umbral_co2=100.0)
    cola.encolar("B", urgente=False, umbral_co2=250.0)

    primera_vuelta = cola.ejecutar_pendientes(mock_intensidad())
    cola.encolar("C", urgente=False, umbral_co2=250.0)
    segunda_vuelta = cola.ejecutar_pendientes(mock_intensidad())

    assert [t.nombre for t in primera_vuelta] == ["B"]
    assert [t.nombre for t in segunda_vuelta] == ["A", "C"]


@patch("electricity_maps.obtener_intensidad_carbono", return_value=999.0)
def test_las_tareas_urgentes_se_ejecutan_siempre(mock_intensidad) -> None:
    cola = ColaVerde()
    cola.encolar("parche crítico", urgente=True, umbral_co2=0.0)
    cola.encolar("tarea flexible", urgente=False, umbral_co2=100.0)

    ejecutadas = cola.ejecutar_pendientes(mock_intensidad())

    assert [t.nombre for t in ejecutadas] == ["parche crítico"]
    assert cola.estadisticas["pendientes"] == 1


@patch("electricity_maps.obtener_intensidad_carbono", return_value=100.0)
def test_se_preserva_el_orden_fifo_en_misma_prioridad(mock_intensidad) -> None:
    cola = ColaVerde()
    cola.encolar("tarea 1", urgente=False, umbral_co2=300.0)
    cola.encolar("tarea 2", urgente=False, umbral_co2=300.0)
    cola.encolar("tarea 3", urgente=False, umbral_co2=300.0)

    ejecutadas = cola.ejecutar_pendientes(mock_intensidad())

    assert [tarea.nombre for tarea in ejecutadas] == ["tarea 1", "tarea 2", "tarea 3"]
