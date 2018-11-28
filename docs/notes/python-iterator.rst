.. meta::
    :description lang=en: Collect useful snippets of Python Iterator
    :keywords: Python, Python Cheat Sheet, Python Iterator

========
Iterator
========

Set Items to a List/Dictionary
-------------------------------

Get a list with init value

.. code-block:: python

    >>> ex = [0] * 10
    >>> ex
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

Extend two lists

.. code-block:: python

    >>> a = [1, 2, 3]; b = ['a', 'b']
    >>> a + b
    [1, 2, 3, 'a', 'b']

Using builtin function ``map``

.. code-block:: python

    >>> map(fn, range(5))
    [0, 1, 4, 9, 16]

NamedTuple
----------

.. code-block:: python

    # namedtuple(typename, field_names)
    # replace define class without method
    >>> from collections import namedtuple
    >>> Example = namedtuple("Example",'a b c')
    >>> e = Example(1, 2, 3)
    >>> print(e.a, e[1], e[1] + e.b)
    1 2 4

Delegating Iteration
---------------------

.. code-block:: python

    # __iter__ return an iterator object
    # Be careful: list is an "iterable" object not an "iterator"
    >>> class Iter(object):
    ...     def __init__(self, list_):
    ...         self._list = list_
    ...     def __iter__(self):
    ...         return iter(self._list)
    ...
    >>> it = Iter([1, 2, 3])
    >>> for i in it:
    ...     print(i)
    ...
    1
    2
    3
