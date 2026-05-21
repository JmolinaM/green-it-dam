# P3 — Datos que cuestan energía (Optimizar · RA5)

Comparación de estrategias de E/S: **carga completa** vs. **streaming por chunks** sobre un dataset IoT de ~80 MB.

## Duración

3 sesiones × 50 min

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `generar_dataset.py` | Genera el CSV sintético de sensores IoT (~80 MB con 1 M filas) |
| `carga_mala.py` | Carga completa con `pd.read_csv()` — alto consumo de RAM |
| `carga_buena.py` | Lectura en chunks con `pd.read_csv(chunksize=...)` — O(k) en memoria |
| `carga_streaming_stats.py` | Streaming que calcula 4 estadísticas en un único paso |
| `medicion.py` | Compara las tres variantes: pico RAM, tiempo y CO₂eq |

## Instalación

```
pip install codecarbon==2.3.4 pandas==2.2.0
```

## Uso

```
python generar_dataset.py     # genera datos.csv (~80 MB)
python medicion.py            # ejecuta y compara las tres estrategias
```
