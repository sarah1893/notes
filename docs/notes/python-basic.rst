.. meta::
    :description lang=en: Collect useful snippets of Python
    :keywords: Python, Python Cheat Sheet

=======================
Python Basic Cheatsheet
=======================

.. contents:: Table of Contents
    :backlinks: none


Backport Features
------------------

**New in Python 2.1**

- PEP `236 <https://www.python.org/dev/peps/pep-0236>`_ - Back to the __future__

``from __future__ import feature`` is a `future statement`__.
It uses for backporting features from other python versions to current
python version, not like original import.

.. _future: https://docs.python.org/2/reference/simple_stmts.html#future
__ future_

Backport python3 print_function to python2

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

Backport python3 unicode_literals to python2

.. code-block:: python

    >>> type("Guido") # string type is str in python2
    <type 'str'>
    >>> from __future__ import unicode_literals
    >>> type("Guido") # string type become unicode
    <type 'unicode'>

Backport PEP `238 <https://www.python.org/dev/peps/pep-0238>`_ - Changing the Division Operator

.. code-block:: python

    >>> 1/2
    0
    >>> from __future__ import division
    >>> 1/2   # return a float (classic division)
    0.5
    >>> 1//2  # return a int (floor division)
    0

Check Python Version
--------------------

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

Check Object Attributes
-----------------------

.. code-block:: python

    >>> dir(list)  # check all attr of list
    ['__add__', '__class__', ...]

Document Functions
-------------------

Define a function document

.. code-block:: python

    >>> def example():
    ...   """ This is an example function """
    ...   print("Example function")
    ...
    >>> example.__doc__
    ' This is an example function '

Or using help function

.. code-block:: python

    >>> help(example)

Check Instance Type
-------------------

.. code-block:: python

    >>> ex = 10
    >>> isinstance(ex,int)
    True

Check, Get, Set Attribute
-------------------------

.. code-block:: python

    >>> class Example(object):
    ...   def __init__(self):
    ...     self.name = "ex"
    ...   def printex(self):
    ...     print("This is an example")
    ...
    >>> ex = Example()

Check an object has attributes

.. code-block:: python

    >>> # hasattr(obj, 'attr')
    >>> hasattr(ex,"name")
    True
    >>> hasattr(ex,"printex")
    True
    >>> hasattr(ex,"print")
    False

Get an object's attribute

.. code-block:: python

    >>> # getattr(obj, 'attr')
    >>> getattr(ex,'name')
    'ex'

Set an object's attribute

.. code-block:: python

    >>> # setattr(obj, 'attr', value)
    >>> setattr(ex,'name','example')
    >>> ex.name
    'example'

Check Inheritance
-----------------

.. code-block:: python

    >>> class Example(object):
    ...   def __init__(self):
    ...     self.name = "ex"
    ...   def printex(self):
    ...     print("This is an Example")
    ...
    >>> issubclass(Example, object)
    True

Check Global Variables
-----------------------

.. code-block:: python

    >>> globals()
    {'args': (1, 2, 3, 4, 5), ...}

Check Callable
---------------

.. code-block:: python

    >>> a = 10
    >>> def fun():
    ...   print("I am callable")
    ...
    >>> callable(a)
    False
    >>> callable(fun)
    True

Get Function/Class Name
-----------------------

.. code-block:: python

    >>> class ExampleClass(object):
    ...   pass
    ...
    >>> def example_function():
    ...   pass
    ...
    >>> ex = ExampleClass()
    >>> ex.__class__.__name__
    'ExampleClass'
    >>> example_function.__name__
    'example_function'


New and Init
-------------

``__init__`` will be invoked

.. code-block:: python

    >>> class ClassA(object):
    ...     def __new__(cls, arg):
    ...         print('__new__ ' + arg)
    ...         return object.__new__(cls, arg)
    ...     def __init__(self, arg):
    ...         print('__init__ ' + arg)
    ...
    >>> o = ClassA("Hello")
    __new__ Hello
    __init__ Hello

``__init__`` won't be invoked

.. code-block:: python

    >>> class ClassB(object):
    ...     def __new__(cls, arg):
    ...         print('__new__ ' + arg)
    ...         return object
    ...     def __init__(self, arg):
    ...         print('__init__ ' + arg)
    ...
    >>> o = ClassB("Hello")
    __new__ Hello


The Diamond Problem
--------------------

The problem of multiple inheritance in searching a method

.. code-block:: python

    >>> def foo_a(self):
    ...     print("This is ClsA")
    ...
    >>> def foo_b(self):
    ...     print("This is ClsB")
    ...
    >>> def foo_c(self):
    ...     print("This is ClsC")
    ...
    >>> class Type(type):
    ...     def __repr__(cls):
    ...         return cls.__name__
    ...
    >>> ClsA = Type("ClsA", (object,), {'foo': foo_a})
    >>> ClsB = Type("ClsB", (ClsA,), {'foo': foo_b})
    >>> ClsC = Type("ClsC", (ClsA,), {'foo': foo_c})
    >>> ClsD = Type("ClsD", (ClsB, ClsC), {})
    >>> ClsD.mro()
    [ClsD, ClsB, ClsC, ClsA, <type 'object'>]
    >>> ClsD().foo()
    This is ClsB


Representation of Class
------------------------

.. code-block:: python

    >>> class Example(object):
    ...    def __str__(self):
    ...       return "Example __str__"
    ...    def __repr__(self):
    ...       return "Example __repr__"
    ...
    >>> print(str(Example()))
    Example __str__
    >>> Example()
    Example __repr__

Break Up a Long String
-----------------------

Original long string

.. code-block:: python

    # original long string
    >>> s = 'This is a very very very long python string'
    >>> s
    'This is a very very very long python string'

Single quote with an escaping backslash

.. code-block:: python

    >>> s = "This is a very very very " \
    ...     "long python string"
    >>> s
    'This is a very very very long python string'

Using brackets

.. code-block:: python

    >>> s = ("This is a very very very "
    ...      "long python string")
    >>> s
    'This is a very very very long python string'

Using ``+``

.. code-block:: python

    >>> s = ("This is a very very very " +
    ...      "long python string")
    >>> s
    'This is a very very very long python string'

Using triple-quote with an escaping backslash

.. code-block:: python

    >>> s = '''This is a very very very \
    ... long python string'''
    >>> s
    'This is a very very very long python string'

Using Generator as Iterator
---------------------------

.. code-block:: python

    # see: PEP289
    >>> for x in g:
    ...     print(x, end=' ')
    ... else:
    ...     print()
    ...
    0 1 2 3 4 5 6 7 8 9

    # equivalent to
    >>> def generator():
    ...     for x in range(10):
    ...         yield x
    ...
    >>> g = generator()
    >>> for x in g:
    ...     print(x, end=' ')
    ... else:
    ...     print()
    ...
    0 1 2 3 4 5 6 7 8 9

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

Loop with Else Clause
----------------------

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

Exception with Else Clause
---------------------------

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

Lambda
-------

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

Multiline lambda example

.. code-block:: python

    >>> (lambda x:
    ... True
    ... if x>0
    ... else
    ... False)(3)
    True

Option arguments
-----------------

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

Declare a Class
----------------

.. code-block:: python

    >>> def fib(self, n):
    ...     if n <= 2:
    ...         return 1
    ...     return fib(self, n-1) + fib(self, n-2)
    ...
    >>> Fib = type('Fib', (object,), {'val': 10,
    ...                               'fib': fib})
    >>> f = Fib()
    >>> f.val
    10
    >>> f.fib(f.val)
    55

Equals to

.. code-block:: python

    >>> class Fib(object):
    ...     val = 10
    ...     def fib(self, n):
    ...         if n <=2:
    ...             return 1
    ...         return self.fib(n-1)+self.fib(n-2)
    ...
    >>> f = Fib()
    >>> f.val
    10
    >>> f.fib(f.val)
    55


Callable Object
---------------

.. code-block:: python

    >>> class CallableObject(object):
    ...   def example(self, *args, **kwargs):
    ...     print("I am callable!")
    ...   def __call__(self, *args, **kwargs):
    ...     self.example(*args, **kwargs)
    ...
    >>> ex = CallableObject()
    >>> ex()
    I am callable!

Context Manager
----------------

.. code-block:: python

    # replace try: ... finally: ...
    # see: PEP343
    # common use in open and close

    import socket

    class Socket(object):
        def __init__(self,host,port):
            self.host = host
            self.port = port

        def __enter__(self):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((self.host,self.port))
            sock.listen(5)
            self.sock = sock
            return self.sock

        def __exit__(self,*exc_info):
            if exc_info[0] is not None:
                import traceback
                traceback.print_exception(*exc_info)
            self.sock.close()

    if __name__=="__main__":
        host = 'localhost'
        port = 5566
        with Socket(host, port) as s:
            while True:
                conn, addr = s.accept()
                msg = conn.recv(1024)
                print(msg)
                conn.send(msg)
                conn.close()

Using contextlib
-----------------

.. code-block:: python

    from contextlib import contextmanager

    @contextmanager
    def opening(filename, mode='r'):
       f = open(filename, mode)
       try:
          yield f
       finally:
          f.close()

    with opening('example.txt') as fd:
       fd.read()

Open a File
------------

.. code-block:: python

    >>> with open("/etc/passwd",'r') as f:
    ...    content = f.read()

Reading File Chunks
-------------------

.. code-block:: python


    >>> chunk_size = 16
    >>> content = ''
    >>> with open('/etc/hosts') as f:
    ...     for c in iter(lambda: f.read(chunk_size), ''):
    ...         content += c
    ...
    >>> print(content)
    127.0.0.1	localhost
    255.255.255.255	broadcasthost
    ::1             localhost

    10.245.1.3  www.registry.io

Property
--------

.. code-block:: python

    >>> class Example(object):
    ...     def __init__(self, value):
    ...        self._val = value
    ...     @property
    ...     def val(self):
    ...         return self._val
    ...     @val.setter
    ...     def val(self, value):
    ...         if not isinstance(value, int):
    ...             raise TypeError("Expected int")
    ...         self._val = value
    ...     @val.deleter
    ...     def val(self):
    ...         del self._val
    ...
    >>> ex = Example(123)
    >>> ex.val = "str"
    Traceback (most recent call last):
      File "", line 1, in
      File "test.py", line 12, in val
        raise TypeError("Expected int")
    TypeError: Expected int

Equals to

.. code-block:: python

    >>> class Example(object):
    ...     def __init__(self, value):
    ...        self._val = value
    ...
    ...     def _val_getter(self):
    ...         return self._val
    ...
    ...     def _val_setter(self, value):
    ...         if not isinstance(value, int):
    ...             raise TypeError("Expected int")
    ...         self._val = value
    ...
    ...     def _val_deleter(self):
    ...         del self._val
    ...
    ...     val = property(fget=_val_getter, fset=_val_setter, fdel=_val_deleter, doc=None)
    ...

Computed Attributes
--------------------

``@property`` computes a value of a attribute only when we need. Not store in
memory previously.

.. code-block:: python

    >>> class Example(object):
    ...   @property
    ...   def square3(self):
    ...     return 2**3
    ...
    >>> ex = Example()
    >>> ex.square3
    8

Descriptor
----------

.. code-block:: python

    >>> class Integer(object):
    ...   def __init__(self, name):
    ...     self._name = name
    ...   def __get__(self, inst, cls):
    ...     if inst is None:
    ...       return self
    ...     else:
    ...       return inst.__dict__[self._name]
    ...   def __set__(self, inst, value):
    ...     if not isinstance(value, int):
    ...       raise TypeError("Expected int")
    ...     inst.__dict__[self._name] = value
    ...   def __delete__(self,inst):
    ...     del inst.__dict__[self._name]
    ...
    >>> class Example(object):
    ...   x = Integer('x')
    ...   def __init__(self, val):
    ...     self.x = val
    ...
    >>> ex1 = Example(1)
    >>> ex1.x
    1
    >>> ex2 = Example("str")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 4, in __init__
      File "<stdin>", line 11, in __set__
    TypeError: Expected an int
    >>> ex3 = Example(3)
    >>> hasattr(ex3, 'x')
    True
    >>> del ex3.x
    >>> hasattr(ex3, 'x')
    False

Static and Class Methond
-------------------------

``@classmethod`` is bound to a class. ``@staticmethod`` is similar to a python
function but define in a class.

.. code-block:: python

    >>> class example(object):
    ...   @classmethod
    ...   def clsmethod(cls):
    ...     print("I am classmethod")
    ...   @staticmethod
    ...   def stmethod():
    ...     print("I am staticmethod")
    ...   def instmethod(self):
    ...     print("I am instancemethod")
    ...
    >>> ex = example()
    >>> ex.clsmethod()
    I am classmethod
    >>> ex.stmethod()
    I am staticmethod
    >>> ex.instmethod()
    I am instancemethod
    >>> example.clsmethod()
    I am classmethod
    >>> example.stmethod()
    I am staticmethod
    >>> example.instmethod()
    Traceback (most recent call last):
      File "", line 1, in
    TypeError: unbound method instmethod() ...

Abstract Method
----------------

``abc`` is used to define methods but not implement

.. code-block:: python

    >>> from abc import ABCMeta, abstractmethod
    >>> class base(object):
    ...   __metaclass__ = ABCMeta
    ...   @abstractmethod
    ...   def absmethod(self):
    ...     """ Abstract method """
    ...
    >>> class example(base):
    ...   def absmethod(self):
    ...     print("abstract")
    ...
    >>> ex = example()
    >>> ex.absmethod()
    abstract

Another common way is to ``raise NotImplementedError``

.. code-block:: python

    >>> class base(object):
    ...   def absmethod(self):
    ...     raise NotImplementedError
    ...
    >>> class example(base):
    ...   def absmethod(self):
    ...     print("abstract")
    ...
    >>> ex = example()
    >>> ex.absmethod()
    abstract

Common Magic
-------------

.. code-block:: python

    # see python document: data model
    # For command class
    __main__
    __name__
    __file__
    __module__
    __all__
    __dict__
    __class__
    __doc__
    __init__(self, [...)
    __str__(self)
    __repr__(self)
    __del__(self)

    # For Descriptor
    __get__(self, instance, owner)
    __set__(self, instance, value)
    __delete__(self, instance)

    # For Context Manager
    __enter__(self)
    __exit__(self, exc_ty, exc_val, tb)

    # Emulating container types
    __len__(self)
    __getitem__(self, key)
    __setitem__(self, key, value)
    __delitem__(self, key)
    __iter__(self)
    __contains__(self, value)

    # Controlling Attribute Access
    __getattr__(self, name)
    __setattr__(self, name, value)
    __delattr__(self, name)
    __getattribute__(self, name)

    # Callable object
    __call__(self, [args...])

    # Compare related
    __cmp__(self, other)
    __eq__(self, other)
    __ne__(self, other)
    __lt__(self, other)
    __gt__(self, other)
    __le__(self, other)
    __ge__(self, other)

    # arithmetical operation related
    __add__(self, other)
    __sub__(self, other)
    __mul__(self, other)
    __div__(self, other)
    __mod__(self, other)
    __and__(self, other)
    __or__(self, other)
    __xor__(self, other)

Parsing CSV
------------

.. code-block:: python

    >>> try:
    ...     from StringIO import StringIO # for py2
    ... except ImportError:
    ...     from io import StringIO # for py3
    ...
    >>> import csv
    >>> s = "foo,bar,baz"
    >>> f = StringIO(s)
    >>> for x in csv.reader(f): print(x)
    ...
    ['foo', 'bar', 'baz']

Or

.. code-block:: python

    >>> import csv
    >>> s = "foo,bar,baz"
    >>> for x in csv.reader([s]): print(x)
    ...
    ['foo', 'bar', 'baz']

Using slot to Save Memory
--------------------------

.. code-block:: python

    #!/usr/bin/env python3

    import resource
    import platform
    import functools


    def profile_mem(func):
        @functools.wraps(func)
        def wrapper(*a, **k):
            s = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            ret = func(*a, **k)
            e = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

            uname = platform.system()
            if uname == "Linux":
                print(f"mem usage: {e - s} kByte")
            elif uname == "Darwin":
                print(f"mem usage: {e - s} Byte")
            else:
                raise Exception("not support")
            return ret
        return wrapper


    class S(object):
        __slots__ = ['attr1', 'attr2', 'attr3']

        def __init__(self):
            self.attr1 = "Foo"
            self.attr2 = "Bar"
            self.attr3 = "Baz"


    class D(object):

        def __init__(self):
            self.attr1 = "Foo"
            self.attr2 = "Bar"
            self.attr3 = "Baz"


    @profile_mem
    def alloc(cls):
        _ = [cls() for _ in range(1000000)]


    alloc(S)
    alloc(D)

output:

.. code-block:: console

    $ python3.6 s.py
    mem usage: 70922240 Byte
    mem usage: 100659200 Byte

Dynamic Execute Python Code
----------------------------

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
