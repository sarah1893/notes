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

Type alias
----------

Like ``typedef`` or ``using`` in c/c++

.. code-block:: cpp

    #include <iostream>
    #include <string>
    #include <regex>
    #include <vector>

    typedef std::string Url;
    template<typename T> using Vector = std::vector<T>;

    int main(int argc, char *argv[])
    {
        Url url = "https://python.org";
        std::regex p("(https?)://([^/\r\n]+)(/[^\r\n]*)?");
        bool m = std::regex_match(url, p);
        Vector<int> v = {1, 2};

        std::cout << m << std::endl;
        for (auto it : v) std::cout << it << std::endl;
        return 0;
    }

Type aliases are defined by simple variable assignments

.. code-block:: python

    import re

    from typing import Pattern, List

    # Like typedef, using in c/c++

    # PEP 484 recommend capitalizing alias names
    Url = str

    url: Url = "https://www.python.org/"

    p: Pattern = re.compile("(https?)://([^/\r\n]+)(/[^\r\n]*)?")
    m = p.match(url)

    Vector = List[int]
    v: Vector = [1., 2.]

Using ``TypeVar`` as template
------------------------------

Like c++ ``template <typename T>``

.. code-block:: cpp

    #include <iostream>

    template <typename T>
    T add(T x, T y) {
        return x + y;
    }

    int main(int argc, char *argv[])
    {
        std::cout << add(1, 2) << std::endl;
        std::cout << add(1., 2.) << std::endl;
        return 0;
    }

Python using ``Generic``

.. code-block:: python

    from typing import TypeVar

    T = TypeVar("T")

    def add(x: T, y: T) -> T:
        return x + y

    add(1, 2)
    add(1., 2.)

Using ``TypeVar`` and ``Generic`` as class template
----------------------------------------------------

Like c++ ``template <typename T> class``

.. code-block:: cpp

    #include <iostream>

    template<typename T>
    class Foo {
    public:
        Foo(T foo) {
            foo_ = foo;
        }
        T Get() {
            return foo_;
        }
    private:
        T foo_;
    };

    int main(int argc, char *argv[])
    {
        Foo<int> f(123);
        std::cout << f.Get() << std::endl;
        return 0;
    }

Define a generic class in Python

.. code-block:: python

    from typing import Generic, TypeVar

    T = TypeVar("T")

    class Foo(Generic[T]):
        def __init__(self, foo: T) -> None:
            self.foo = foo

        def get(self) -> T:
            return self.foo

    f: Foo[str] = Foo("Foo")
    v: int = f.get()

output:

.. code-block:: bash

    $ mypy --strict foo.py
    foo.py:13: error: Incompatible types in assignment (expression has type "str", variable has type "int")

Constraining to a fixed set of possible types
----------------------------------------------

.. code-block:: python

    from typing import TypeVar

    # restrict T = int or T = float
    T = TypeVar("T", int, float)

    def add(x: T, y: T) -> T:
        return x + y

    add(1, 2)
    add(1., 2.)
    add("1", 2)
    add("hello", "world")

output:

.. code-block:: bash

    # mypy can detect wrong type
    $ mypy --strict foo.py
    foo.py:10: error: Value of type variable "T" of "add" cannot be "object"
    foo.py:11: error: Value of type variable "T" of "add" cannot be "str"

Union[Any, None] == Optional[Any]
----------------------------------

.. code-block:: python

    from typing import List, Union

    def first(l: List[Union[int, None]]) -> Union[int, None]:
        return None if len(l) == 0 else l[0]

    first([None])

    # equal to

    from typing import List, Optional

    def first(l: List[Optional[int]]) -> Optional[int]:
        return None if len(l) == 0 else l[0]

    first([None])
