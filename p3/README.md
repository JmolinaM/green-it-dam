# P3 — Datos que cuestan energía (Optimizar · RA5)

Un sistema IoT con **50 sensores** genera un CSV con más de **1 millón de filas**. La primera versión del backend usa `pd.read_csv()` para cargar el fichero completo y termina agotando la RAM del servidor. El objetivo de la práctica es comparar esa estrategia con una lectura **por streaming** en chunks.

## Escenario

- **Resultado de aprendizaje:** RA5
- **Pregunta guía:** ¿qué cambia en memoria y emisiones cuando pasamos de carga completa a streaming?
- **Herramientas:** `pandas`, `numpy`, `tracemalloc` y `CodeCarbon` con fallback de CO₂ para macOS.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `generar_dataset.py` | Genera `datos_sensores.csv` con 1 000 000 de filas y columnas IoT realistas |
| `carga_mala.py` | Carga el CSV completo con `pd.read_csv()` y calcula 4 estadísticas |
| `carga_buena.py` | Lee el CSV con `chunksize=10_000` y calcula las mismas estadísticas en una sola pasada lógica |

## Instalación

```bash
pip install codecarbon pandas numpy matplotlib
```

> En macOS, los scripts usan automáticamente el modelo `15 W × tiempo × 0,233 gCO₂eq/Wh` si `CodeCarbon` no puede acceder a `powermetrics`.

## Uso

```bash
python generar_dataset.py
python carga_mala.py
python carga_buena.py
```

## Concepto clave: O(n) frente a O(k)

- **Carga completa (`carga_mala.py`)**: memoria **O(n)**, porque el fichero entero reside en RAM.
- **Streaming (`carga_buena.py`)**: memoria **O(k)**, donde `k` es el tamaño del chunk (`10 000` filas).
- La versión streaming calcula **media, desviación típica, mínimo y máximo** de `temperatura` y `co2_ppm` sin retener el dataset completo.

## Qué observar en el aula

- Diferencia de pico de RAM entre ambos enfoques.
- Relación entre tiempo total y emisiones estimadas.
- Cómo cambia el diseño del programa cuando se piensa en escalabilidad y sostenibilidad desde el principio.
