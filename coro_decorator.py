"""
Contains a decorator used for automatically priming courotines when
instantiated.
"""
from functools import wraps


def coroutine_primer(func):
    """
    Decorator that primes a coroutine when instantiated.
    """
    @wraps(func)
    def wrap(*args, **kwargs):
        coro = func(*args, **kwargs)
        next(coro)

        return coro

    return wrap
