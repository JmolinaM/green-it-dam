"""
medicion.py — P1: ¿Cuánto pesa tu algoritmo?

Mide el consumo energético de dos implementaciones de Fibonacci y lo traduce
a equivalencias cotidianas para que la diferencia sea visible e intuitiva.

Uso:
    pip install codecarbon
    python medicion.py

NOTA macOS: CodeCarbon usa 'powermetrics' que requiere contraseña de admin.
Si no está disponible, el script calcula las emisiones con un modelo de potencia
estimada (CPU 15 W × tiempo × factor de emisión España 2023: 0,233 gCO₂eq/Wh).
Los valores relativos (porcentaje de reducción) son igualmente válidos.
"""

import cProfile
import io
import os
import platform
import pstats
import time

from fib_recursivo import fibonacci_recursivo
from fib_iterativo import fibonacci_iterativo

# CodeCarbon usa 'powermetrics' en macOS, que requiere contraseña de admin (sudo).
# Lo desactivamos en macOS y usamos siempre el modelo de estimación.
_USE_CODECARBON = platform.system() != "Darwin"
if _USE_CODECARBON:
    try:
        from codecarbon import EmissionsTracker
    except ImportError:
        _USE_CODECARBON = False


os.makedirs("emisiones", exist_ok=True)

CPU_POWER_W = 15.0
CARBON_INTENSITY_gCO2_PER_Wh = 0.233   # España 2023 (REE, kgCO₂eq/kWh)

# ── Equivalencias cotidianas ──────────────────────────────────────────────────
# Fuentes: Carbon Trust, IEA, Carbonfootprint.com (2023)
gCO2_POR_BUSQUEDA_GOOGLE   = 0.2     # gCO₂eq por búsqueda en Google
gCO2_POR_WHATSAPP          = 0.014   # gCO₂eq por mensaje de WhatsApp
gCO2_POR_KM_COCHE_GASOLINA = 170     # gCO₂eq por km en coche de gasolina
gCO2_POR_MIN_NETFLIX_HD    = 0.6     # gCO₂eq por minuto de Netflix HD


def equivalencias(g: float) -> str:
    """Traduce gramos de CO₂eq a acciones cotidianas comprensibles."""
    busquedas = g / gCO2_POR_BUSQUEDA_GOOGLE
    whatsapps = g / gCO2_POR_WHATSAPP
    metros_coche = (g / gCO2_POR_KM_COCHE_GASOLINA) * 1000
    segundos_netflix = (g / gCO2_POR_MIN_NETFLIX_HD) * 60

    lineas = []
    if busquedas >= 0.01:
        lineas.append(f"  🔍 {busquedas:>8.2f} búsquedas en Google")
    if whatsapps >= 0.01:
        lineas.append(f"  💬 {whatsapps:>8.2f} mensajes de WhatsApp")
    if metros_coche >= 0.001:
        lineas.append(f"  🚗 {metros_coche:>8.4f} metros en coche de gasolina")
    if segundos_netflix >= 0.001:
        lineas.append(f"  📺 {segundos_netflix:>8.4f} segundos de Netflix HD")
    return "\n".join(lineas) if lineas else "  < 0,001 gCO₂eq (prácticamente cero)"


def fmt_co2(g: float) -> str:
    """Formatea gramos de CO₂eq con precisión adaptativa (nunca muestra 0)."""
    if g == 0:
        return "0.000000000 gCO₂eq"
    if g >= 0.001:
        return f"{g:.6f} gCO₂eq"
    if g >= 1e-9:
        return f"{g:.2e} gCO₂eq"
    return f"{g:.3e} gCO₂eq"


def barra_ascii(valor: float, maximo: float, ancho: int = 40) -> str:
    """Genera una barra de progreso ASCII proporcional al valor."""
    if maximo == 0:
        return "░" * ancho
    llenas = int((valor / maximo) * ancho)
    return "█" * llenas + "░" * (ancho - llenas)


def medir(func, n: int, nombre: str) -> dict:
    """Mide emisiones CO₂ y tiempo. Usa CodeCarbon (Linux/Windows) o modelo estimado (macOS)."""
    if _USE_CODECARBON:
        t0 = time.perf_counter()
        try:
            tracker = EmissionsTracker(
                project_name=nombre,
                output_dir="./emisiones",
                log_level="error",
            )
            tracker.start()
            resultado = func(n)
            emisiones_kg = tracker.stop()
            t1 = time.perf_counter()
            fuente = "CodeCarbon"
        except Exception:
            resultado = func(n)
            t1 = time.perf_counter()
            energia_Wh = CPU_POWER_W * ((t1 - t0) / 3600)
            emisiones_kg = energia_Wh * CARBON_INTENSITY_gCO2_PER_Wh / 1000
            fuente = "modelo estimado"
    else:
        t0 = time.perf_counter()
        resultado = func(n)
        t1 = time.perf_counter()
        energia_Wh = CPU_POWER_W * ((t1 - t0) / 3600)
        emisiones_kg = energia_Wh * CARBON_INTENSITY_gCO2_PER_Wh / 1000
        fuente = "modelo estimado"

    return {
        "nombre": nombre,
        "n": n,
        "resultado": resultado,
        "emisiones_gCO2eq": emisiones_kg * 1_000,
        "tiempo_s": t1 - t0,
        "fuente": fuente,
    }


def contar_llamadas(func, n: int) -> int:
    """Cuenta el número total de llamadas a función con cProfile (incluye recursión)."""
    pr = cProfile.Profile()
    pr.enable()
    func(n)
    pr.disable()
    stats = pstats.Stats(pr, stream=io.StringIO())
    # v[1] = ncalls (total incluido recursión); v[0] = pcalls (primitivas solamente)
    return sum(v[1] for v in stats.stats.values())


if __name__ == "__main__":
    WIDTH = 62

    print()
    print("╔" + "═" * WIDTH + "╗")
    print("║" + "  🌿 P1 — ¿CUÁNTO PESA TU ALGORITMO?".center(WIDTH) + "║")
    print("║" + f"  CPU {CPU_POWER_W}W  ·  Factor emisión ES 2023: {CARBON_INTENSITY_gCO2_PER_Wh} gCO₂eq/Wh".center(WIDTH) + "║")
    print("╚" + "═" * WIDTH + "╝")

    for N in [30, 33, 35]:
        d_rec = medir(fibonacci_recursivo, N, f"fib_recursivo_n{N}")
        d_ite = medir(fibonacci_iterativo,  N, f"fib_iterativo_n{N}")

        co2_rec = d_rec["emisiones_gCO2eq"]
        co2_ite = d_ite["emisiones_gCO2eq"]
        t_rec   = d_rec["tiempo_s"]
        t_ite   = d_ite["tiempo_s"]

        reduccion_co2 = (co2_rec - co2_ite) / co2_rec * 100 if co2_rec > 0 else 0
        reduccion_t   = (t_rec   - t_ite)   / t_rec   * 100 if t_rec   > 0 else 0

        print(f"\n  ┌── Fibonacci({N}) ──────────────────────────────────────────")
        print(f"  │  Fuente de medición: {d_rec['fuente']}")
        print(f"  │")
        print(f"  │  CO₂ emitido:")
        print(f"  │    Recursivo  [{barra_ascii(co2_rec, co2_rec, 35)}]  {fmt_co2(co2_rec)}")
        print(f"  │    Iterativo  [{barra_ascii(co2_ite, co2_rec, 35)}]  {fmt_co2(co2_ite)}")
        print(f"  │    → Reducción: {reduccion_co2:.1f}%")
        print(f"  │")
        print(f"  │  Tiempo de ejecución:")
        print(f"  │    Recursivo  [{barra_ascii(t_rec, t_rec, 35)}]  {t_rec:.4f} s")
        print(f"  │    Iterativo  [{barra_ascii(t_ite, t_rec, 35)}]  {t_ite:.6f} s")
        print(f"  │    → Reducción: {reduccion_t:.1f}%")
        print(f"  │")
        print(f"  │  ¿Qué significa {fmt_co2(co2_rec)}?")
        print(equivalencias(co2_rec))
        print(f"  └──────────────────────────────────────────────────────────")

    # Extrapolación a producción
    d_rec35 = medir(fibonacci_recursivo, 35, "extrapol_rec")
    d_ite35 = medir(fibonacci_iterativo,  35, "extrapol_ite")
    ahorro_dia_g  = (d_rec35["emisiones_gCO2eq"] - d_ite35["emisiones_gCO2eq"]) * 10_000_000
    ahorro_dia_kg = ahorro_dia_g / 1_000
    ahorro_ano_t  = ahorro_dia_g * 365 / 1_000_000

    print()
    print("╔" + "═" * WIDTH + "╗")
    print("║" + "  📊 EXTRAPOLACIÓN: 10 MILLONES DE PETICIONES/DÍA (n=35)".center(WIDTH) + "║")
    print("╠" + "═" * WIDTH + "╣")
    print(f"║  Ahorro diario:   {ahorro_dia_kg:>10.1f} kg CO₂eq".ljust(WIDTH + 1) + "║")
    print(f"║  Ahorro anual:    {ahorro_ano_t:>10.1f} toneladas CO₂eq/año".ljust(WIDTH + 1) + "║")
    print("╠" + "═" * WIDTH + "╣")
    print(f"║  ¿Qué es {ahorro_ano_t:.0f} toneladas CO₂eq/año?".ljust(WIDTH + 1) + "║")
    coches_km = ahorro_dia_g * 365 / gCO2_POR_KM_COCHE_GASOLINA / 1000
    busquedas_ano = ahorro_dia_g * 365 / gCO2_POR_BUSQUEDA_GOOGLE
    print(f"║  🚗  Equivale a {coches_km:>10,.0f} km en coche al año".ljust(WIDTH + 1) + "║")
    print(f"║  🔍  O a       {busquedas_ano:>10,.0f} búsquedas en Google al año".ljust(WIDTH + 1) + "║")
    print("╠" + "═" * WIDTH + "╣")

    # Llamadas a función
    calls_rec = contar_llamadas(fibonacci_recursivo, 35)
    calls_ite = contar_llamadas(fibonacci_iterativo,  35)
    print(f"║  🔁 Fibonacci(35) recursivo: {calls_rec:>12,} llamadas a función".ljust(WIDTH + 1) + "║")
    print(f"║  ✅ Fibonacci(35) iterativo: {calls_ite - 1:>12,} iteraciones del bucle".ljust(WIDTH + 1) + "║")
    print(f"║  → Factor de diferencia:     {calls_rec//(calls_ite-1):>12,}×".ljust(WIDTH + 1) + "║")
    print("╚" + "═" * WIDTH + "╝")
    print()
    print("  💡 Reflexión: ¿Cambiaría esto tu forma de elegir un algoritmo?")
    print("     Escribe tu respuesta en el diario de práctica.")
    print()
