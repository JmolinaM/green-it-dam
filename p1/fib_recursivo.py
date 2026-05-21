# fib_recursivo.py — P1: ¿Cuánto pesa tu algoritmo?


def fibonacci_recursivo(n: int) -> int:
    """Implementación recursiva sin memoización. Complejidad: O(2^n)."""
    if n <= 1:
        return n
    return fibonacci_recursivo(n - 1) + fibonacci_recursivo(n - 2)
