# P2 — El objeto que viaja (Analizar · RA4)

Diagnóstico y optimización del crecimiento de memoria en un sistema de envíos con POO.  
El alumnado mide el impacto del patrón **Singleton** con `tracemalloc` y CodeCarbon.

## Duración

3 sesiones × 50 min

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `sin_patron.py` | Sistema sin Singleton — cada operación crea instancias nuevas |
| `con_singleton.py` | Sistema con Singleton — una única instancia compartida |
| `medicion.py` | Script de medición: memoria RAM y CO₂ para n ∈ {100, 500, 1000} operaciones |

## Instalación

```
pip install codecarbon==2.3.4
```

## Uso

```
python medicion.py
```
