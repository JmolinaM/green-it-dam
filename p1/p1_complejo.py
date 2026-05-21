"""
p1_complejo.py — P1: ¿Cuánto pesa tu algoritmo?  (Sesión 1)

Programa complejo: ordena listas grandes, calcula primos y opera cadenas
en bucle. Muestra que el tiempo de CPU activo es el factor clave en el consumo.

El alumnado lo instrumenta con CodeCarbon, anota tiempo y emisiones
en la Ficha P1 y calcula el ratio complejo/simple.

Uso:
    pip install codecarbon
    python p1_complejo.py
"""

import time
import platform
import os

os.makedirs("emisiones", exist_ok=True)

CPU_POWER_W = 15.0
CARBON_INTENSITY_gCO2_PER_Wh = 0.233   # España 2023 (REE)

_USE_CODECARBON = platform.system() != "Darwin"
if _USE_CODECARBON:
    try:
        from codecarbon import EmissionsTracker
    except ImportError:
        _USE_CODECARBON = False


def ordenar_listas(n: int) -> list:
    """Ordena n listas de 500 enteros aleatorios con burbuja. O(n × m²)."""
    import random
    resultados = []
    for _ in range(n):
        lista = [random.randint(0, 10_000) for _ in range(500)]
        # Ordenación burbuja (intencionalmente ineficiente)
        for i in range(len(lista) - 1):
            for j in range(len(lista) - 1 - i):
                if lista[j] > lista[j + 1]:
                    lista[j], lista[j + 1] = lista[j + 1], lista[j]
        resultados.append(lista[-1])
    return resultados


def calcular_primos(limite: int) -> list:
    """Calcula todos los primos hasta 'limite' con criba ingenua. O(n√n)."""
    primos = []
    for n in range(2, limite):
        es_primo = True
        for d in range(2, int(n ** 0.5) + 1):
            if n % d == 0:
                es_primo = False
                break
        if es_primo:
            primos.append(n)
    return primos


def operar_cadenas(n: int) -> str:
    """Concatena n cadenas en bucle con +. O(n²) en memoria."""
    resultado = ""
    for i in range(n):
        resultado = resultado + f"item_{i}_"   # concatenación ineficiente
    return resultado[:50] + "..."


def trabajo_complejo() -> dict:
    """Ejecuta las tres operaciones y devuelve un resumen."""
    r1 = ordenar_listas(30)
    r2 = calcular_primos(5_000)
    r3 = operar_cadenas(2_000)
    return {
        "max_ordenado": max(r1),
        "num_primos": len(r2),
        "cadena_muestra": r3,
    }


if __name__ == "__main__":
    if _USE_CODECARBON:
        tracker = EmissionsTracker(
            project_name="p1_complejo",
            output_dir="./emisiones",
            log_level="error",
        )
        t0 = time.perf_counter()
        tracker.start()
        resultado = trabajo_complejo()
        emisiones_kg = tracker.stop()
        t1 = time.perf_counter()
        fuente = "CodeCarbon"
    else:
        t0 = time.perf_counter()
        resultado = trabajo_complejo()
        t1 = time.perf_counter()
        energia_Wh = CPU_POWER_W * ((t1 - t0) / 3600)
        emisiones_kg = energia_Wh * CARBON_INTENSITY_gCO2_PER_Wh / 1000
        fuente = "modelo estimado"

    emisiones_g = emisiones_kg * 1_000

    print(f"\n  🌿 p1_complejo.py — Ordenación + primos + cadenas")
    print(f"  Primos encontrados : {resultado['num_primos']}")
    print(f"  Tiempo             : {t1 - t0:.4f} s")
    print(f"  Emisiones CO₂      : {emisiones_g:.6f} gCO₂eq  [{fuente}]")
    print()
    print("  → Anota estos valores en la Ficha P1 (columna 'Complejo').")
    print("  → Calcula el ratio: CO₂(complejo) / CO₂(simple)")
    print()
