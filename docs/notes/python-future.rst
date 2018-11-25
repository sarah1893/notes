======
Future
======

.. contents:: Table of Contents
    :backlinks: none

``from __future__ import feature`` is a `future statement`__.
It uses for backporting features from other python versions to current
python version, not like original import.

- PEP `236 <https://www.python.org/dev/peps/pep-0236>`_ - Back to the __future__

.. _future: https://docs.python.org/2/reference/simple_stmts.html#future
__ future_

Print Function
--------------

- PEP `3105 <https://www.python.org/dev/peps/pep-3105>`_ - Make print a function

.. code-block:: python

    >>> print "Hello World"  # print is a statement
    Hello World
    >>> from __future__ import print_function
    >>> print "Hello World"
      File "<stdin>", line 1
        print "Hello World"
                          ^
    SyntaxError: invalid syntax
    >>> print("Hello World") # print become a function
    Hello World

Unicode
-------

- PEP `3112 <https://www.python.org/dev/peps/pep-3112>`_ - Bytes literals in Python 3000

.. code-block:: python

    >>> type("Guido") # string type is str in python2
    <type 'str'>
    >>> from __future__ import unicode_literals
    >>> type("Guido") # string type become unicode
    <type 'unicode'>

Division
--------

- PEP `238 <https://www.python.org/dev/peps/pep-0238>`_ - Changing the Division Operator

.. code-block:: python

    >>> 1/2
    0
    >>> from __future__ import division
    >>> 1/2   # return a float (classic division)
    0.5
    >>> 1//2  # return a int (floor division)
    0
