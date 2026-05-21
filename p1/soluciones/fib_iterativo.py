# fib_iterativo.py — P1: ¿Cuánto pesa tu algoritmo?


def fibonacci_iterativo(n: int) -> int:
    """Implementación iterativa. Complejidad: O(n), espacio: O(1)."""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
