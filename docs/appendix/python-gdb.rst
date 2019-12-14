.. meta::
    :description lang=en: Python interpreter in GNU Debugger (GDB)
    :keywords: Python, Python3, GDB

=========================
Python Interpreter in GDB
=========================

.. contents:: Table of Contents
    :backlinks: none

Abstract
--------

The GNU Debugger (GDB) is the most powerful debugging tool for developers to
troubleshoot errors in their code. However, it is hard for beginners to learn.
Fortunately, `GDB Text User Interface (TUI)`_ provides a way for developers to
review their source code and debug simultaneously. More excitingly, In GDB 7,
**Python Interpreter** was built into GDB. This feature offers more straightforward
ways to customize GDB printers and commands through the Python library. By
discussing examples, this article tries to explore advanced debugging techniques
via Python to develop tool kits for GDB.


Customize GDB print
-------------------

.. code-block:: cpp

    #include <string>

    namespace foo {

    class Foo {
    public:
        Foo(const std::string &s) : msg(s) {}
    private:
        const std::string msg;
    };

    }

    int main(int argc, char *argv[])
    {
        foo::Foo f("Hello GDB!");
        return 0;
    }

.. code-block:: python3

    import gdb

    class FooPrinter(object):
        def __init__(self, val):
            self.val = val

        def to_string(self):
            return f"message: {self.val['msg']}"

    # create a customized pretty printer
    pp = gdb.printing.RegexpCollectionPrettyPrinter('foo')

    # add foo printer to pretty printer
    pp.add_printer('foo', '^foo::Foo$', FooPrinter);

    # register customized pretty printer
    obj = gdb.current_objfile()
    gdb.printing.register_pretty_printer(obj, pp)


.. code-block:: bash

    $ g++ -g foo.cpp
    $ gdb ./a.out
    ...
    (gdb) p f
    $1 = {msg = "Hello GDB!"}
    (gdb) set print pretty on
    (gdb) p f
    $2 = {
      msg = "Hello GDB!"
    }
    (gdb) source foo.py
    (gdb) p f
    $3 = message: "Hello GDB!"


Customize Commands
------------------

.. code-block:: cpp

    #include <string>

    int main(int argc, char *argv[])
    {
        std::string json = R"({"foo": "FOO","bar": "BAR"})";
        return 0;
    }


.. code-block:: python3

    import gdb
    import json


    class JsonPrinter(gdb.Command):
        """Json Pretty Printer"""

        def __init__(self):
            super().__init__("print-json", gdb.COMMAND_USER)

        def invoke(self, s, from_tty):
            try:
                ret = gdb.parse_and_eval(s).string()
                js = json.loads(ret)
                print(json.dumps(js, indent=4))
            except Exception as e:
                print(f"Parse json error! {e}")


    JsonPrinter()

.. code-block:: bash

    $ g++ -g -std=c++14 foo.cpp
    $ gdb ./a.out
    $ ...
    (gdb) p json.c_str()
    $2 = 0x555555768e70 "{\"foo\": \"FOO\",\"bar\": \"BAR\"}"
    (gdb) set print pretty on
    (gdb) p json.c_str()
    $3 = 0x555555768e70 "{\"foo\": \"FOO\",\"bar\": \"BAR\"}"
    (gdb) source pretty-json.py
    (gdb) print-json json.c_str()
    {
        "foo": "FOO",
        "bar": "BAR"
    }


Reference
---------

1. `Extending GDB using Python`_

.. _Extending GDB using Python: https://sourceware.org/gdb/onlinedocs/gdb/Python.html#Python
.. _GDB Text User Interface (TUI): https://sourceware.org/gdb/onlinedocs/gdb/TUI.html
