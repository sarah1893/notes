========
Function
========

Document Functions
------------------

Define a function document

.. code-block:: python

    >>> def example():
    ...   """ This is an example function """
    ...   print("Example function")
    ...
    >>> example.__doc__
    ' This is an example function '
    >>> help(example)

Option arguments
----------------

.. code-block:: python

    >>> def example(a, b=None, *args, **kwargs):
    ...     print(a, b)
    ...     print(args)
    ...     print(kwargs)
    ...
    >>> example(1, "var", 2, 3, word="hello")
    1 var
    (2, 3)
    {'word': 'hello'}
    >>> a_tuple = (1, 2, 3, 4, 5)
    >>> a_dict = {"1":1, "2":2, "3":3}
    >>> example(1, "var", *a_tuple, **a_dict)
    1 var
    (1, 2, 3, 4, 5)
    {'1': 1, '2': 2, '3': 3}

Callable
--------

.. code-block:: python

    >>> a = 10
    >>> def fun():
    ...   print("I am callable")
    ...
    >>> callable(a)
    False
    >>> callable(fun)
    True

Get Function Name
-----------------

.. code-block:: python

    >>> def example_function():
    ...   pass
    ...
    >>> example_function.__name__
    'example_function'

Lambda
------

.. code-block:: python

    >>> fn = lambda x: x**2
    >>> fn(3)
    9
    >>> (lambda x: x**2)(3)
    9
    >>> (lambda x: [x*_ for _ in range(5)])(2)
    [0, 2, 4, 6, 8]
    >>> (lambda x: x if x>3 else 3)(5)
    5

Generator
---------

.. code-block:: python

    >>> def fib(n):
    ...     a, b = 0, 1
    ...     for _ in range(n):
    ...         yield a
    ...         b, a = a + b, b
    ...
    >>> [f for f in fib(10)]
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

Decorator
---------

**New in Python 2.4**

- PEP `318 <https://www.python.org/dev/peps/pep-0318/>`_ - Decorators for Functions and Methods

.. code-block:: python

    >>> from functools import wraps
    >>> def decorator(func):
    ...   @wraps(func)
    ...   def wrapper(*args, **kwargs):
    ...     print("Before calling {}.".format(func.__name__))
    ...     ret = func(*args, **kwargs)
    ...     print("After calling {}.".format(func.__name__))
    ...     return ret
    ...   return wrapper
    ...
    >>> @decorator
    ... def example():
    ...   print("Inside example function.")
    ...
    >>> example()
    Before calling example.
    Inside example function.
    After calling example.

Equals to

.. code-block:: python

    ... def example():
    ...   print("Inside example function.")
    ...
    >>> example = decorator(example)
    >>> example()
    Before calling example.
    Inside example function.
    After calling example.


``@wraps`` preserve attributes of the original function, otherwise attributes
of the decorated function will be replaced by **wrapper function**. For example

Without ``@wraps``

.. code-block:: python

    >>> def decorator(func):
    ...     def wrapper(*args, **kwargs):
    ...         print('wrap function')
    ...         return func(*args, **kwargs)
    ...     return wrapper
    ...
    >>> @decorator
    ... def example(*a, **kw):
    ...     pass
    ...
    >>> example.__name__  # attr of function lose
    'wrapper'

With ``@wraps``

.. code-block:: python

    >>> from functools import wraps
    >>> def decorator(func):
    ...     @wraps(func)
    ...     def wrapper(*args, **kwargs):
    ...         print('wrap function')
    ...         return func(*args, **kwargs)
    ...     return wrapper
    ...
    >>> @decorator
    ... def example(*a, **kw):
    ...     pass
    ...
    >>> example.__name__  # attr of function preserve
    'example'

Decorator with Arguments
------------------------

.. code-block:: python

    >>> from functools import wraps
    >>> def decorator_with_argument(val):
    ...   def decorator(func):
    ...     @wraps(func)
    ...     def wrapper(*args, **kwargs):
    ...       print("Val is {0}".format(val))
    ...       return func(*args, **kwargs)
    ...     return wrapper
    ...   return decorator
    ...
    >>> @decorator_with_argument(10)
    ... def example():
    ...   print("This is example function.")
    ...
    >>> example()
    Val is 10
    This is example function.

Equals to

.. code-block:: python

    >>> def example():
    ...   print("This is example function.")
    ...
    >>> example = decorator_with_argument(10)(example)
    >>> example()
    Val is 10
    This is example function.

Cache
-----

**New in Python 3.2**

Without Cache

.. code-block:: python

    >>> import time
    >>> def fib(n):
    ...     if n < 2:
    ...         return n
    ...     return fib(n - 1) + fib(n - 2)
    ...
    >>> s = time.time(); _ = fib(32); e = time.time(); e - s
    1.1562161445617676

With Cache (dynamic programming)

.. code-block:: python

    >>> from functools import lru_cache
    >>> @lru_cache(maxsize=None)
    ... def fib(n):
    ...     if n < 2:
    ...         return n
    ...     return fib(n - 1) + fib(n - 2)
    ...
    >>> s = time.time(); _ = fib(32); e = time.time(); e - s
    2.9087066650390625e-05
    >>> fib.cache_info()
    CacheInfo(hits=30, misses=33, maxsize=None, currsize=33)
