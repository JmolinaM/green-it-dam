# P2 — El servidor que no para de crecer (Analizar · RA4)

SensorStream S.L. tiene un servidor Python que **funciona**, pero su consumo de RAM crece de forma progresiva hasta que el sistema operativo termina el proceso. El reto del alumnado consiste en analizar decisiones de diseño orientado a objetos, medir su impacto con `tracemalloc` y proponer una refactorización razonada.

## Escenario

- **Resultado de aprendizaje:** RA4
- **Metodología:** ABP en grupos de 3
- **Herramienta principal:** `tracemalloc` + modelo estimado de CO₂
- **Pregunta guía:** ¿qué decisiones de diseño hacen que el servidor no deje de crecer?

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `sensor_monitor.py` | Servidor base con crecimiento progresivo de memoria: `ProcesadorDatos`, `GestorAlertas` y `ConfiguracionApp` |
| `stress_test.py` | Prueba de estrés para `n = 100, 500, 1000` con `tracemalloc` y exportación a CSV |
| `soluciones/sensor_monitor_refactorizado.py` | Solución docente con estrategia D (combinación de mejoras) |

## Decisiones de diseño a investigar

| # | Pista en el código | Qué provoca |
|---|--------------------|-------------|
| 1 | `ProcesadorDatos._historial` | El historial crece sin límite: cada lectura queda guardada para siempre |
| 2 | `ConfiguracionApp()` por lectura | Se crean muchas configuraciones con un bloque de datos de ~50 KB |
| 3 | `GestorAlertas._registro_config.append(dict(...))` | Se acumulan copias de configuración en memoria |

## Estrategias de refactorización propuestas

- **Estrategia A:** convertir `ConfiguracionApp` en Singleton y evitar `dict(config._parametros)` en el registro.
- **Estrategia B:** sustituir `_historial` por `collections.deque(maxlen=X)` para conservar solo una ventana circular.
- **Estrategia C:** eliminar completamente `_registro_config` si no aporta valor real al sistema.
- **Estrategia D:** combinar varias estrategias para estabilizar la memoria del servidor.

## Instalación

```bash
pip install codecarbon
```

> En macOS, `CodeCarbon` puede requerir permisos de administrador. Los scripts incluyen un **fallback automático** con el modelo `15 W × tiempo × 0,233 gCO₂eq/Wh`.

## Uso

```bash
python stress_test.py
```

El script imprime una tabla con el **pico de RAM**, el **tiempo de ejecución** y una **estimación de CO₂eq** para cada escenario (`100`, `500`, `1000`). Además, exporta los resultados a `emisiones/stress_results.csv`.

## Preguntas socráticas para la puesta en común

- ¿Qué pasa con el tamaño de `_historial` cuando doblas `n`?
- ¿Cuántos objetos `ConfiguracionApp` se crean para `n = 1000`?
- ¿Qué estructura de datos sería más adecuada si solo necesitamos las últimas lecturas?

## Carpeta `soluciones/`

La carpeta `soluciones/` es **solo para el profesorado**. Contiene una versión refactorizada que aplica la estrategia **D**: Singleton para la configuración, buffer circular con `deque` y eliminación del registro redundante de configuraciones.
