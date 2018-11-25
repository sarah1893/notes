======
Future
======


`Future statements <https://docs.python.org/3/reference/simple_stmts.html#future>`_
tell the interpreter to compile some semantics as the semantics which will be
available in the future Python version. In other words, Python uses ``from __future__ import feature``
to backport features from other higher Python versions to the current interpreter.

Future statements are **NOT** import statements. Future statements change how
Python interprets the code. They **MUST** be at the top of the file. Otherwise,
Python interpreter will raise ``SyntaxError``.

If you're interested in future statements and want to acquire more explanation,
further information can be found on `PEP 236 <https://www.python.org/dev/peps/pep-0236>`_.


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

Annotations
-----------

Before Python 3.7, we cannot assign annotations in a class or a function if
it is not available in the current scope. A common situation is the definition of
a container class.

.. code-block:: python

    class Tree(object):

        def insert(self, tree: Tree): ...

Example

.. code-block:: bash

    $ python3 foo.py
    Traceback (most recent call last):
      File "foo.py", line 1, in <module>
        class Tree(object):
      File "foo.py", line 3, in Tree
        def insert(self, tree: Tree): ...
    NameError: name 'Tree' is not defined

In this case, the definition of the class is not available yet. Python interpreter
cannot parse the annotation during their definition time. To solve this issue,
Python uses string literals to replace the class.

.. code-block:: python

    class Tree(object):

        def insert(self, tree: 'Tree'): ...

After version 3.7, Python introduces the future statement, ``annotations``, to
perform postponed evaluation. It will become the default feature in Python 4.
For further information please refer to `PEP 563 <https://www.python.org/dev/peps/pep-0563>`_.


.. code-block:: python

    from __future__ import annotations

    class Tree(object):

        def insert(self, tree: Tree): ...
