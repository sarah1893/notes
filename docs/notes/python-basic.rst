.. meta::
    :description lang=en: Collect useful snippets of Python
    :keywords: Python, Python Cheat Sheet

======
Basics
======

This cheat sheet focus on some basic and common semantics or snippets which we
**GOOGLE** them many time.


.. contents:: Table of Contents
    :backlinks: none


Get Python Version
------------------

We can use module ``sys`` or ``platform`` to get the current Python version.

.. code-block:: python

    >>> import sys
    >>> sys.version_info
    >>> print(sys.version)
    3.7.1 (default, Nov  6 2018, 18:46:03)
    [Clang 10.0.0 (clang-1000.11.45.5)]

Using ``platform.python_version`` to get Python version.

.. code-block:: python

    >>> import platform
    >>> platform.python_version()
    '3.7.1'

Check Python Version
--------------------

.. code-block:: python

    >>> import sys
    >>> print(sys.version)
    3.6.5 (default, Apr 24 2018, 10:37:34)
    [GCC 4.2.1 Compatible Apple LLVM 7.3.0 (clang-703.0.31)]
    >>> sys.version_info >= (3, 6)
    True
    >>> sys.version_info >= (3, 7)
    False

Ellipsis
--------

Ellipsis is a built-in constant. After Python 3.0, we can use ``...`` as
``Ellipsis``.

.. code-block:: python

    >>> ...
    Ellipsis
    >>> ... == Ellipsis
    True
    >>> type(...)
    <class 'ellipsis'>

We can use it to represent a function or a class which has not implemented yet.

.. code-block:: python

    >>> class Foo: ...
    ...
    >>> def foo(): ...
    ...

Other constants can be found in `Built-in Constants <https://docs.python.org/3/library/constants.html>`_.

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
