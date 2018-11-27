====
List
====

The list is a common data structure which we use to store objects. Most of the
time, programmers concern about getting, setting, searching, filtering, and
sorting. Furthermore, sometimes, we waltz ourself into common pitfalls of
the memory management. Thus, the main goal of this cheat sheet is to collect
some common operations and pitfalls.


Get Items from a List
---------------------

Although getting data from a list is quite simple, we can retrieve data more
elegantly. Python provides a lot of ways to get data. Following example shows
how to get data via negative index and slice.

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

Unpacking a List
----------------

Sometimes, we want to unpack our list to variables in order to make our code
become more readable. In this case, we assign N elements to N variables as
following example.

.. code-block:: python

    >>> arr = [1, 2, 3]
    >>> a, b, c = arr
    >>> a, b, c
    (1, 2, 3)

Based on PEP `3132 <https://www.python.org/dev/peps/pep-3132>`_, we can use a
single asterisk to unpack N elements to the number of variables which is less
than N in Python 3.

.. code-block:: python

    >>> arr = [1, 2, 3, 4, 5]
    >>> a, b, *c, d = arr
    >>> a, b, d
    (1, 2, 5)
    >>> c
    [3, 4]

Get Index and Item
------------------

.. code-block:: python

    >>> for i, v in enumerate(range(3)):
    ...     print((i, v))
    ...
    (0, 0)
    (1, 1)
    (2, 2)

Using a Slice
-------------

Sometimes, our data may concatenate as a large segment. In this case, we will
represent the range of data by using ``slice`` objects as explaining variables
instead of using **slicing** expressions.

.. code-block:: python


    >>> record = "Hello world!"
    >>> hello = slice(0, 5)  # slice(start,end,step)
    >>> world = slice(6, -1)
    >>> record[hello]
    'Hello'
    >>> record[world]
    'world'

Zip Multiple Lists
------------------

.. code-block:: python

    >>> a = [1, 2, 3, 4, 5]
    >>> b = [2, 4, 5, 6, 8]
    >>> list(zip(a, b))
    [(1, 2), (2, 4), (3, 5), (4, 6), (5, 8)]
    >>> c = [5, 6, 7, 8]
    >>> list(zip(a, b, c))
    [(1, 2, 5), (2, 4, 6), (3, 5, 7), (4, 6, 8)]

Reverse a List
--------------

.. code-block:: python

    >>> a = [1, 2, 3, 4, 5]
    >>> a[::-1]
    [5, 4, 3, 2, 1]

Filter Unnecessary Items
------------------------

.. code-block:: python

    >>> [x for x in range(5) if x > 1]
    [2, 3, 4]
    >>> l = ['1', '2', 3, 'Hello', 4]
    >>> predicate = lambda x: isinstance(x, int)
    >>> filter(predicate, l)
    [3, 4]

Using Lists as Stacks
---------------------

.. code-block:: python

    >>> stack = []
    >>> stack.append(1)
    >>> stack.append(2)
    >>> stack.append(3)
    >>> stack
    [1, 2, 3]
    >>> stack.pop()
    3
    >>> stack.pop()
    2
    >>> stack
    [1]

Implement a List-like Object
----------------------------

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

Pitfall - Assign a List to Another Variable
-------------------------------------------

.. code-block:: python

    >>> a = [1, 2, 3]
    >>> b = a
    >>> a
    [1, 2, 3]
    >>> b
    [1, 2, 3]
    >>> b[2] = 123456  # a[2] = 123456
    >>> b
    [1, 2, 123456]
    >>> a
    [1, 2, 123456]

Pitfall - Init a List with Multiply
-----------------------------------

.. code-block:: python

    >>> a = [[]] * 3
    >>> b = [[] for _ in range(3)]
    >>> a[0].append("Hello")
    >>> a
    [['Hello'], ['Hello'], ['Hello']]
    >>> b[0].append("Python")
    >>> b
    [['Python'], [], []]
