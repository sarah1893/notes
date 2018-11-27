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

Using list comprehension

.. code-block:: python

    >>> [x for x in range(10)]
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> fn = lambda x: x**2
    >>> [fn(x) for x in range(5)]
    [0, 1, 4, 9, 16]
    >>> {'{0}'.format(x): x for x in range(3)}
    {'1': 1, '0': 0, '2': 2}

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

Emulating a Dictionary
----------------------

.. code-block:: python

    >>> class EmuDict(object):
    ...   def __init__(self, dict_):
    ...     self._dict = dict_
    ...   def __repr__(self):
    ...     return "EmuDict: " + repr(self._dict)
    ...   def __getitem__(self, key):
    ...     return self._dict[key]
    ...   def __setitem__(self, key, val):
    ...     self._dict[key] = val
    ...   def __delitem__(self, key):
    ...     del self._dict[key]
    ...   def __contains__(self, key):
    ...     return key in self._dict
    ...   def __iter__(self):
    ...     return iter(self._dict.keys())
    ...
    >>> _ = {"1":1, "2":2, "3":3}
    >>> emud = EmuDict(_)
    >>> emud  # __repr__
    EmuDict: {'1': 1, '2': 2, '3': 3}
    >>> emud['1']  # __getitem__
    1
    >>> emud['5'] = 5  # __setitem__
    >>> emud
    EmuDict: {'1': 1, '2': 2, '3': 3, '5': 5}
    >>> del emud['2']  # __delitem__
    >>> emud
    EmuDict: {'1': 1, '3': 3, '5': 5}
    >>> for _ in emud:
    ...     print(emud[_], end=' ')  # __iter__
    ... else:
    ...     print()
    ...
    1 3 5
    >>> '1' in emud  # __contains__
    True
