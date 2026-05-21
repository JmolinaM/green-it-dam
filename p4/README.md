# P4 — La cola verde (Actuar · RA9)

La práctica introduce una arquitectura de **Carbon-Aware Computing**: un sistema decide **cuándo ejecutar** tareas diferibles según la intensidad de carbono de la red eléctrica. Si la intensidad supera el umbral de una tarea, la cola la pospone; si no, la ejecuta. Las tareas urgentes tienen prioridad y siempre se lanzan.

## Escenario

- **Resultado de aprendizaje:** RA9
- **Metodología:** ABP en grupos de 3
- **Herramientas:** `heapq`, `pytest`, Electricity Maps API y `CodeCarbon` con fallback automático en macOS.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `cola_verde.py` | Esqueleto guiado de la clase `ColaVerde` con marcadores `TODO` |
| `electricity_maps.py` | Consulta la API real o usa `_simular_intensidad()` si no hay token o no hay conexión |
| `main.py` | Demo con 5 tareas y 3 ciclos de ejecución (`150`, `280`, `120` gCO₂eq/kWh) |
| `test_cola_verde.py` | Tests con `pytest` y `unittest.mock.patch` |
| `soluciones/cola_verde_completa.py` | Implementación completa de referencia para el profesorado |

## Instalación

```bash
pip install codecarbon pytest requests
```

## Uso

```bash
python main.py
pytest test_cola_verde.py
```

## Configuración de la API key

```bash
export ELECTRICITY_MAPS_TOKEN="tu_token"
```

La consulta se realiza contra:

```text
https://api.electricitymap.org/v3/carbon-intensity/latest?zone=ES
```

## Modo offline

Si no hay token, la API falla o se trabaja en el aula sin internet, `electricity_maps.py` utiliza automáticamente `_simular_intensidad(hora=None)`, un modelo horario sencillo: menor intensidad por la noche y en el mediodía solar, mayor en el pico de tarde.

## Qué debe hacer el alumnado

- Completar o comentar el esqueleto de `ColaVerde`.
- Justificar por qué `heapq` permite priorizar urgencia y preservar FIFO mediante un contador.
- Medir la simulación con `CodeCarbon` (o con el fallback `15 W × tiempo × 0,233 gCO₂eq/Wh` en macOS).
- Añadir o adaptar tests para cubrir nuevos casos de uso.
