__version__ = '0.1.0a0'


from functools import wraps
from typing import Callable, Optional


def repeat(_func: Optional[Callable] = None, *, n: int = 2) -> Callable:
    """Execute a function repeatedly n times.

    Parameters
    ----------
        _func : Function to be decorated
        n : Number of repetitions

    Returns
    -------
        If `repeated` is invoked without any arguments (that is, `@repeat`),
        return the decorated version of the original function; else, return
        a closure with `n` stored in the enclosing scope

    Examples
    --------
    >>> @repeat
    ... def hello(name):
    ...     print(f'Hello, {name}')
    >>> hello('Allyson')
    Hello, Allyson
    Hello, Allyson

    >>> @repeat(n=5)
    ... def hello(name):
    ...     print(f'Hello, {name}')
    >>> hello('Allyson')
    Hello, Allyson
    Hello, Allyson
    Hello, Allyson
    Hello, Allyson
    Hello, Allyson
    """
    def _repeat(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                value = func(*args, **kwargs)
            return value
        return wrapper
    return _repeat(_func) if _func else _repeat
