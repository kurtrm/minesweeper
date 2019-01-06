"""
Contains a decorator used for automatically priming courotines when
instantiated.
"""
from functools import wraps


def coroutine_primer(func):
    """
    Decorator that primes a coroutine when instantiated.
    """
    @wraps
    def wrapper(*args, **kwargs):
        coro = func(*args, **kwargs)
        coro.next()

        return coro

    return wrapper
