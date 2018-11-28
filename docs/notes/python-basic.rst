.. meta::
    :description lang=en: Collect useful snippets of Python
    :keywords: Python, Python Cheat Sheet

======
Basics
======

The main goal of this cheat sheet is to collect some common and basic semantics
or snippets. The cheat sheet includes some syntax, which we have already known
but still ambiguous in our mind, or some snippets, which we google them again
and again. In addition, because **the end Of life date for Python 2** is coming.
Most of the snippets are mainly based on **Python 3**'s syntax.


.. contents:: Table of Contents
    :backlinks: none

Hello world!
------------

When we start to learn a new language, we usually learn from printing
**Hello world!**. In Python, we can use another way to print the  message by
importing ``__hello__`` module.  The source code can be found on
`frozen.c <https://github.com/python/cpython/blob/master/Python/frozen.c>`_.

.. code-block:: python

    >>> print("Hello world!")
    Hello world!
    >>> import __hello__
    Hello world!
    >>> import __phello__
    Hello world!
    >>> import __phello__.spam
    Hello world!


Python Version
--------------

It is important for a programmer to know current Python version because
not every syntax will work in the current version. In this case, we can get the
Python version by ``python -V`` or using the module, ``sys``.

.. code-block:: python

    >>> import sys
    >>> print(sys.version)
    3.7.1 (default, Nov  6 2018, 18:46:03)
    [Clang 10.0.0 (clang-1000.11.45.5)]

We can also use ``platform.python_version`` to get Python version.

.. code-block:: python

    >>> import platform
    >>> platform.python_version()
    '3.7.1'

Sometimes, checking the current Python version is important because we may want
to enable some features in some specific versions. ``sys.version_info`` provides more
detail information about the interpreter. We can use it to compare with the
version we want.

.. code-block:: python

    >>> import sys
    >>> sys.version_info >= (3, 6)
    True
    >>> sys.version_info >= (3, 7)
    False

Ellipsis
--------

`Ellipsis <https://docs.python.org/3/library/constants.html#Ellipsis>`_ is a
built-in constant. After Python 3.0, we case use ``...`` as ``Ellipsis``. It
may be the most enigmatic constant in Python. Based on the official document,
we can use it to extend slicing syntax. Nevertheless, there are some other
conventions in type hinting, stub files, or function expressions.

.. code-block:: python

    >>> ...
    Ellipsis
    >>> ... == Ellipsis
    True
    >>> type(...)
    <class 'ellipsis'>

The following snippet shows that we can use the ellipsis to represent a function
or a class which has not implemented yet.

.. code-block:: python

    >>> class Foo: ...
    ...
    >>> def foo(): ...
    ...

For Loop
--------

In Python, we can access iterable object's items directly through the
**for statement**. If we need to get indexes and items of an iterable object
such as list or tuple at the same time, using ``enumerate`` is better than
``range(len(iterable))``.

.. code-block:: python

    >>> for idx, val in enumerate(["foo", "bar", "baz"]):
    ...     print(idx, val)
    ...
    (0, 'foo')
    (1, 'bar')
    (2, 'baz')

For Loop Has Else Clause
------------------------

The else part runs when the break does not occur.

.. code-block:: python

    >>> for _ in range(5):
    ...     pass
    ... else:
    ...     print("no break")
    ...
    no break

Skip else part when the break occurs.

.. code-block:: python

    >>> for x in range(5):
    ...     if x % 2 == 0:
    ...         print("break")
    ...         break
    ... else:
    ...     print("no break")
    ...
    break

While Loop Has Else Clause
--------------------------

.. code-block:: python

    >>> n = 0
    >>> while n < 5:
    ...     if n == 3:
    ...         break
    ...     n += 1
    ... else:
    ...     print("no break")
    ...

While Loop Emulate do while
---------------------------

In Python, there is no ``do while`` statement because it is unnecessary. We
can place conditions at the final line of a ``while`` loop to achieve the
same thing.

.. code-block:: python

    >>> n = 0
    >>> while True:
    ...     n += 1
    ...     if n == 5:
    ...         break
    ...
    >>> n
    5

Exception Has Else Clause
-------------------------

.. code-block:: python

    >>> try:
    ...     print("No exception")
    ... except:
    ...     pass
    ... else:
    ...     print("Success")
    ...
    No exception
    Success

Dynamic Execute Python Code
---------------------------

.. code-block:: python

    >>> py = '''
    ... def fib(n):
    ...     a, b = 0, 1
    ...     for _ in range(n):
    ...         b, a = b + a, b
    ...     return a
    ... print(fib(10))
    ... '''
    >>> exec(py, globals(), locals())
    55
