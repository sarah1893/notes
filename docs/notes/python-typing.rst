Python typing cheatsheet
========================

.. contents:: Table of Contents
    :backlinks: none

Without type check
-------------------

.. code-block:: python

    def fib(n):
        a, b = 0, 1
        for _ in range(n):
            yield a
            b, a = a + b, b

    print([n for n in fib(3.6)])


output:

.. code-block:: bash

    # errors will not be detected until runtime

    $ python fib.py
    Traceback (most recent call last):
      File "ty.py", line 8, in <module>
        print([n for n in fib(3.5)])
      File "ty.py", line 8, in <listcomp>
        print([n for n in fib(3.5)])
      File "ty.py", line 3, in fib
        for _ in range(n):
    TypeError: 'float' object cannot be interpreted as an integer


With type check
----------------

.. code-block:: python

    # give a type hint
    from typing import Generator

    def fib(n: int) -> Generator:
        a: int = 0
        b: int = 1
        for _ in range(n):
            yield a
            b, a = a + b, b

    print([n for n in fib(3.6)])

output:

.. code-block:: bash

    # errors will be detected before running

    $ mypy --strict fib.py
    fib.py:12: error: Argument 1 to "fib" has incompatible type "float"; expected "int"


Avoid ``None`` access
----------------------

.. code-block:: python

    import re

    from typing import Pattern, Dict, Optional

    # like c++
    # std::regex url("(https?)://([^/\r\n]+)(/[^\r\n]*)?");
    # std::regex color("^#?([a-f0-9]{6}|[a-f0-9]{3})$");

    url: Pattern = re.compile("(https?)://([^/\r\n]+)(/[^\r\n]*)?")
    color: Pattern = re.compile("^#?([a-f0-9]{6}|[a-f0-9]{3})$")

    x: Dict[str, Pattern] = {"url": url, "color": color}
    y: Optional[Pattern] = x.get("baz", None)

    print(y.match("https://www.python.org/"))

output:

.. code-block:: bash

    $ mypy --strict foo.py
    foo.py:15: error: Item "None" of "Optional[Pattern[Any]]" has no attribute "match"


Becareful ``Optional``
-----------------------

.. code-block:: python

    from typing import cast, Optional

    def fib(n):
        a, b = 0, 1
        for _ in range(n):
            b, a = a + b, b
        return a

    def cal(n: Optional[int]) -> None:
        print(fib(n))

    cal(None)

output:

.. code-block:: bash

    # mypy will not detect errors
    $ mypy foo.py

Explicitly declare

.. code-block:: python

    from typing import Optional

    def fib(n: int) -> int:
        a, b = 0, 1
        for _ in range(n):
            b, a = a + b, b
        return a

    def cal(n: Optional[int]) -> None:
        print(fib(n))

output:

.. code-block:: bash

    # mypy can detect errors even we do not check None
    $ mypy --strict foo.py
    foo.py:11: error: Argument 1 to "fib" has incompatible type "Optional[int]"; expected "int"

Becareful cast
---------------

.. code-block:: python

    from typing import cast, Optional

    def gcd(a: int, b: int) -> int:
        while b:
            a, b = b, a % b
        return a

    def cal(a: Optional[int], b: Optional[int]) -> None:
        # XXX: Avoid casting
        ca, cb = cast(int, a), cast(int, b)
        print(gcd(ca, cb))

    cal(None, None)

output:

.. code-block:: bash

    # mypy will not detect type errors
    $ mypy --strict foo.py
