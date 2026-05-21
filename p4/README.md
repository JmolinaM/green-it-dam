# P4 — La cola verde (Actuar · RA9)

Sistema de **Carbon-Aware Computing**: cola de tareas que decide cuándo ejecutar trabajo diferible según la intensidad de carbono de la red eléctrica española.

## Duración

4 sesiones × 50 min (incluye Demo Day)

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `electricity_maps.py` | Cliente para la Electricity Maps API v3; incluye modo simulado offline |
| `cola_verde.py` | Implementación de `ColaVerde` con `heapq`; lógica de diferimiento por umbral CO₂ |
| `main.py` | Ejemplo de uso: simula una jornada de trabajo con el CSV histórico |
| `test_cola_verde.py` | Suite de tests con `pytest` y `unittest.mock` |
| `data/intensidad_es_historico.csv` | CSV histórico de intensidad de carbono de España (a añadir) |

## Instalación

```
pip install codecarbon==2.3.4 requests==2.31.0 pytest
```

## Uso

```
python main.py                # simulación con CSV histórico (sin internet)
pytest test_cola_verde.py     # ejecuta los tests unitarios
```

## API key (opcional)

Registro gratuito en [app.electricitymaps.com](https://app.electricitymaps.com) (50 req/mes en plan free).  
Sin API key, el script usa automáticamente `_simular_intensidad()`.
