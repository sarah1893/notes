.. meta::
    :description lang=en: Collect useful snippets of Python
    :keywords: Python, Python Cheat Sheet

======
Basics
======

.. contents:: Table of Contents
    :backlinks: none


Python Version
--------------

.. code-block:: python

    >>> import sys
    >>> print(sys.version)
    3.6.5 (default, Apr 24 2018, 10:37:34)
    [GCC 4.2.1 Compatible Apple LLVM 7.3.0 (clang-703.0.31)]
    >>> py36 = sys.version_info >= (3, 6)
    >>> py36
    True
    >>> py37 = sys.version_info >= (3, 7)
    >>> py37
    False

List Global Variables
---------------------

.. code-block:: python

    >>> globals()
    {'args': (1, 2, 3, 4, 5), ...}

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

Loop with Else Clause
---------------------

See document: `More Control Flow Tools <https://docs.python.org/3/tutorial/controlflow.html>`_

For loop's else clause runs when no break occurs

.. code-block:: python

    >>> for x in range(5):
    ...     print(x, end=' ')
    ... else:
    ...     print("\nno break occurred")
    ...
    0 1 2 3 4
    no break occurred
    >>> for x in range(5):
    ...     if x % 2 == 0:
    ...         print("break occurred")
    ...         break
    ... else:
    ...     print("no break occurred")
    ...
    break occurred

Above example equals to

.. code-block:: python

    >>> flag = False
    >>> for x in range(5):
    ...     if x % 2 == 0:
    ...         flag = True
    ...         print("break occurred")
    ...         break
    ...
    ... if flag == False:
    ...     print("no break occurred")
    ...
    break occurred

Exception with Else
-------------------

.. code-block:: python

    >>> try:
    ...     print("No exception")
    ... except:
    ...     pass
    ... else:
    ...     print("No exception occurred")
    ...
    No exception
    No exception occurred
