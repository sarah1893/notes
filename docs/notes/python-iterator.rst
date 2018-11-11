.. meta::
    :description lang=en: Collect useful snippets of Python Iterator
    :keywords: Python, Python Cheat Sheet, Python Iterator

==========================
Python Iterator Cheatsheet
==========================

Get Items from List
-------------------

.. code-block:: python

    >>> a = [1, 2, 3, 4, 5]
    >>> a[0]
    1
    >>> a[-1]
    5
    >>> a[0:]
    [1, 2, 3, 4, 5]
    >>> a[:-1]
    [1, 2, 3, 4]
    >>> a[0:-1:2] # a[start:end:step]
    [1, 3]

Get Index and Item
-------------------

.. code-block:: python

    >>> for i, v in enumerate(range(3)):
    ...     print((i, v))
    ...
    (0, 0)
    (1, 1)
    (2, 2)

Slice
-----

.. code-block:: python

    >>> # slice(start,end,step)
    >>> s = slice(0, -1, 2)
    >>> a[s]
    [1, 3]

Zip
---

.. code-block:: python

    >>> a = [1, 2, 3, 4, 5]
    >>> b = [2, 4, 5, 6, 8]
    >>> zip(a, b)
    [(1, 2), (2, 4), (3, 5), (4, 6), (5, 8)]

Filter
------

.. code-block:: python

    >>> [x for x in range(5) if x > 1]
    [2, 3, 4]
    >>> l = ['1', '2', 3, 'Hello', 4]
    >>> predicate = lambda x: isinstance(x, int)
    >>> filter(predicate, l)
    [3, 4]

Reverse
-------

.. code-block:: python

    >>> a = [1, 2, 3, 4, 5]
    >>> a[::-1]
    [5, 4, 3, 2, 1]

Collect Distinct Items
-----------------------

.. code-block:: python

    >>> a = [1, 2, 3, 3, 3]
    >>> list({_ for _ in a})
    [1, 2, 3]
    >>> # or
    >>> list(set(a))
    [1, 2, 3]

Watch Out
---------

.. code-block:: python

    >>> a = [[]] * 3
    >>> b = [[] for _ in range(3)]
    >>> a[0].append("Hello")
    >>> a
    [['Hello'], ['Hello'], ['Hello']]
    >>> b[0].append("Python")
    >>> b
    [['Python'], [], []]


Get Dictionary All Keys
------------------------

.. code-block:: python

    >>> a = {"1":1, "2":2, "3":3}
    >>> b = {"2":2, "3":3, "4":4}
    >>> a.keys()
    ['1', '3', '2']

Get Dictionary Key and Value
-----------------------------

.. code-block:: python

    >>> a = {"1":1, "2":2, "3":3}
    >>> a.items()

Find Dictionaries Same Keys
----------------------------

.. code-block:: python

    >>> a = {"1":1, "2":2, "3":3}
    >>> [_ for _ in a.keys() if _ in b.keys()]
    ['3', '2']
    >>> # better way
    >>> c = set(a).intersection(set(b))
    >>> list(c)
    ['3', '2']
    >>> # or
    >>> [_ for _ in a if _ in b]
    ['3', '2']
    [('1', 1), ('3', 3), ('2', 2)]

Update Dictionary
-----------------

.. code-block:: python

    >>> a = {"1":1, "2":2, "3":3}
    >>> b = {"2":2, "3":3, "4":4}
    >>> a.update(b)
    >>> a
    {'1': 1, '3': 3, '2': 2, '4': 4}

Merge Two Dictionaries
-----------------------

Python 3.4 or lower

.. code-block:: python

    >>> a = {"x": 55, "y": 66}
    >>> b = {"a": "foo", "b": "bar"}
    >>> c = a.copy()
    >>> c.update(b)
    >>> c
    {'y': 66, 'x': 55, 'b': 'bar', 'a': 'foo'}


Python 3.5 or above

.. code-block:: python

    >>> a = {"x": 55, "y": 66}
    >>> b = {"a": "foo", "b": "bar"}
    >>> c = {**a, **b}
    >>> c
    {'x': 55, 'y': 66, 'a': 'foo', 'b': 'bar'}

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


Python Set
-----------

Set comprehension

.. code-block:: python

    >>> a = [1, 2, 5, 6, 6, 6, 7]
    >>> s = {x for x in a}
    >>> s
    set([1, 2, 5, 6, 7])
    >>> s = {x for x in a if x > 3}
    >>> s
    set([5, 6, 7])
    >>> s = {x if x > 3 else -1 for x in a}
    >>> s
    set([6, 5, -1, 7])

Uniquify a list

.. code-block:: python

    >>> a = [1, 2, 2, 2, 3, 4, 5, 5]
    >>> a
    [1, 2, 2, 2, 3, 4, 5, 5]
    >>> ua = list(set(a))
    >>> ua
    [1, 2, 3, 4, 5]

Union two sets

.. code-block:: python

    >>> a = set([1, 2, 2, 2, 3])
    >>> b = set([5, 5, 6, 6, 7])
    >>> a | b
    set([1, 2, 3, 5, 6, 7])
    >>> # or
    >>> a = [1, 2, 2, 2, 3]
    >>> b = [5, 5, 6, 6, 7]
    >>> set(a + b)
    set([1, 2, 3, 5, 6, 7])

Append items to a set

.. code-block:: python

    >>> a = set([1, 2, 3, 3, 3])
    >>> a.add(5)
    >>> a
    set([1, 2, 3, 5])
    >>> # or
    >>> a = set([1, 2, 3, 3, 3])
    >>> a |= set([1, 2, 3, 4, 5, 6])
    >>> a
    set([1, 2, 3, 4, 5, 6])

Intersection two sets

.. code-block:: python

    >>> a = set([1, 2, 2, 2, 3])
    >>> b = set([1, 5, 5, 6, 6, 7])
    >>> a & b
    set([1])

Get common items from sets

.. code-block:: python

    >>> a = [1, 1, 2, 3]
    >>> b = [1, 3, 5, 5, 6, 6]
    >>> com = list(set(a) & set(b))
    >>> com
    [1, 3]

b contains a

.. code-block:: python

    >>> a = set([1, 2])
    >>> b = set([1, 2, 5, 6])
    >>> a <=b
    True

a contains b

.. code-block:: python

    >>> a = set([1, 2, 5, 6])
    >>> b = set([1, 5, 6])
    >>> a >= b
    True

Set diff

.. code-block:: python

    >>> a = set([1, 2, 3])
    >>> b = set([1, 5, 6, 7, 7])
    >>> a - b
    set([2, 3])

Symmetric diff

.. code-block:: python

    >>> a = set([1,2,3])
    >>> b = set([1, 5, 6, 7, 7])
    >>> a ^ b
    set([2, 3, 5, 6, 7])

Python Set
-----------

Set comprehension

.. code-block:: python

    >>> a = [1, 2, 5, 6, 6, 6, 7]
    >>> s = {x for x in a}
    >>> s
    set([1, 2, 5, 6, 7])
    >>> s = {x for x in a if x > 3}
    >>> s
    set([5, 6, 7])
    >>> s = {x if x > 3 else -1 for x in a}
    >>> s
    set([6, 5, -1, 7])

Uniquify a list

.. code-block:: python

    >>> a = [1, 2, 2, 2, 3, 4, 5, 5]
    >>> a
    [1, 2, 2, 2, 3, 4, 5, 5]
    >>> ua = list(set(a))
    >>> ua
    [1, 2, 3, 4, 5]

Union two sets

.. code-block:: python

    >>> a = set([1, 2, 2, 2, 3])
    >>> b = set([5, 5, 6, 6, 7])
    >>> a | b
    set([1, 2, 3, 5, 6, 7])
    >>> # or
    >>> a = [1, 2, 2, 2, 3]
    >>> b = [5, 5, 6, 6, 7]
    >>> set(a + b)
    set([1, 2, 3, 5, 6, 7])

Append items to a set

.. code-block:: python

    >>> a = set([1, 2, 3, 3, 3])
    >>> a.add(5)
    >>> a
    set([1, 2, 3, 5])
    >>> # or
    >>> a = set([1, 2, 3, 3, 3])
    >>> a |= set([1, 2, 3, 4, 5, 6])
    >>> a
    set([1, 2, 3, 4, 5, 6])

Intersection two sets

.. code-block:: python

    >>> a = set([1, 2, 2, 2, 3])
    >>> b = set([1, 5, 5, 6, 6, 7])
    >>> a & b
    set([1])

Get common items from sets

.. code-block:: python

    >>> a = [1, 1, 2, 3]
    >>> b = [1, 3, 5, 5, 6, 6]
    >>> com = list(set(a) & set(b))
    >>> com
    [1, 3]

b contains a

.. code-block:: python

    >>> a = set([1, 2])
    >>> b = set([1, 2, 5, 6])
    >>> a <=b
    True

a contains b

.. code-block:: python

    >>> a = set([1, 2, 5, 6])
    >>> b = set([1, 5, 6])
    >>> a >= b
    True

Set diff

.. code-block:: python

    >>> a = set([1, 2, 3])
    >>> b = set([1, 5, 6, 7, 7])
    >>> a - b
    set([2, 3])

Symmetric diff

.. code-block:: python

    >>> a = set([1,2,3])
    >>> b = set([1, 5, 6, 7, 7])
    >>> a ^ b
    set([2, 3, 5, 6, 7])

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

Emulating a List
----------------

.. code-block:: python

    >>> class EmuList(object):
    ...   def __init__(self, list_):
    ...     self._list = list_
    ...   def __repr__(self):
    ...     return "EmuList: " + repr(self._list)
    ...   def append(self, item):
    ...     self._list.append(item)
    ...   def remove(self, item):
    ...     self._list.remove(item)
    ...   def __len__(self):
    ...     return len(self._list)
    ...   def __getitem__(self, sliced):
    ...     return self._list[sliced]
    ...   def __setitem__(self, sliced, val):
    ...     self._list[sliced] = val
    ...   def __delitem__(self, sliced):
    ...     del self._list[sliced]
    ...   def __contains__(self, item):
    ...     return item in self._list
    ...   def __iter__(self):
    ...     return iter(self._list)
    ...
    >>> emul = EmuList(range(5))
    >>> emul
    EmuList: [0, 1, 2, 3, 4]
    >>> emul[1:3]  # __getitem__
    [1, 2]
    >>> emul[0:4:2]  # __getitem__
    [0, 2]
    >>> len(emul)  # __len__
    5
    >>> emul.append(5)
    >>> emul
    EmuList: [0, 1, 2, 3, 4, 5]
    >>> emul.remove(2)
    >>> emul
    EmuList: [0, 1, 3, 4, 5]
    >>> emul[3] = 6  # __setitem__
    >>> emul
    EmuList: [0, 1, 3, 6, 5]
    >>> 0 in emul  # __contains__
    True


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
