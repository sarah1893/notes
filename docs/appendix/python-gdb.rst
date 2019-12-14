.. meta::
    :description lang=en: Python interpreter in GNU Debugger (GDB)
    :keywords: Python, Python3, GDB

=========================
Python Interpreter in GDB
=========================

.. contents:: Table of Contents
    :backlinks: none

Customize GDB print
-------------------

.. code-block:: cpp

    #include <iostream>
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
    (gdb) start
    Temporary breakpoint 1 at 0xaea: file foo.cpp, line 16.
    Starting program: /root/a.out

    Temporary breakpoint 1, main (argc=1, argv=0x7fffffffe788) at foo.cpp:16
    16	{
    (gdb) list
    11	};
    12
    13	}
    14
    15	int main(int argc, char *argv[])
    16	{
    17		foo::Foo f("Hello GDB!");
    18		return 0;
    19	}
    (gdb) break 18
    Breakpoint 2 at 0x555555554b47: file foo.cpp, line 18.
    (gdb) continue
    Continuing.

    Breakpoint 2, main (argc=1, argv=0x7fffffffe788) at foo.cpp:18
    18		return 0;
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


Reference
---------

1. `Extending GDB using Python`_

.. _Extending GDB using Python: https://sourceware.org/gdb/onlinedocs/gdb/Python.html#Python

