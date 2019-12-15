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
troubleshoot errors in their code. However, it is hard for beginners to learn,
and that is why many programmers prefer to insert ``print`` to examine runtime
status. Fortunately, `GDB Text User Interface (TUI)`_ provides a way for
developers to review their source code and debug simultaneously. More
excitingly, In GDB 7, **Python Interpreter** was built into GDB. This feature
offers more straightforward ways to customize GDB printers and commands through
the Python library. By discussing examples, this article tries to explore
advanced debugging techniques via Python to develop tool kits for GDB.

Introduction
------------

Before troubleshooting a program’s errors, one of the most important things is
to recognize software problems to solve. For instance, there are some issues a
programmer usually meets.

1. Unexpected results (e.g., Logical errors)
2. Core dump (e.g., Segmentation fault)
3. Hang or freeze (e.g., Busy loop)
4. Memory usage is too high (e.g., Leak)

To solve previous problems, GDB provides many “debug procedures,” such as
``start``, ``step``, and ``break``, to inspect a program’s runtime status.
Also, GDB empowers developers to write their own GDB scripts to monitor and
trace programs’ status. By interacting with Python interpreter in GDB, writing
a GDB script will become more accessible and flexible for a developer to solve
software issues.

GDB Review
----------

Although mastering GDB is a long-term process, a quickstart is not complicated;
you must unlearn what you have learned like Yoda. The following sections discuss
some usage of GDB before interacting with Python Interpreter.

Load an Executable
~~~~~~~~~~~~~~~~~~

Allowing GDB to recognize a program’s debug symbols requires ``-g`` option with
GCC while compilation(e.g., ``gcc -g -Wall -Werror -o foo foo.c``). Also,
loading all symbols of an executable file for inspection will not invoke an
executable file to run at the same time. To run an executable file, please use
the command: ``run`` or ``start``.

The difference between ``run`` and ``start`` is whether a program will stop at
entrypoint or not. By using ``start``, programs will stop at beginning and
developers can review their code and set up breakpoints for debugging. For
example,

.. code-block:: bash

    $ gdb ./a.out
    ...
    (gdb) start
    Temporary breakpoint 1 at 0xc0a: file a.cpp, line 5.
    Starting program: /root/a.out

    Temporary breakpoint 1, main (argc=1, argv=0x7fffffffe788) at a.cpp:5
    5       {
    (gdb) l
    1       #include <iostream>
    2       #include <string>
    3
    4       int main(int argc, char *argv[])
    5       {
    6               std::string s{"Hello GDB"};
    7               std::cout << s << std::endl;
    8               return 0;
    9       }
    (gdb) c
    Continuing.
    Hello GDB
    [Inferior 1 (process 4526) exited normally]
    (gdb) run
    Starting program: /root/a.out
    Hello GDB
    [Inferior 1 (process 4530) exited normally]

Text User Interface
~~~~~~~~~~~~~~~~~~~

Text User Interface (TUI) allows developers to visualize source code and to
debug like using Integrated Devekionebt Environment (IDE) to trace problems.
For a beginner, entering the TUI mode is more understandable than the command
line mode. The following key bindings are the most common usage for interacting
with TUI.

1. Ctrl x + a: Enter or leave the TUI mode
2. Ctrl x + o: Switch the active window
3. Ctrl x + 1: Display one window (e.g., source code + command line)
4. Ctrl x + 2: Display two windows (e.g., source code + command line + assembly)


Basic Commands
~~~~~~~~~~~~~~

**Start/Stop a program**

1. start: Run an executable file and stop at beginning
2. run / r: Run an executable file until finish or stop at a breakpoint
3. step / s: Run a program step by step with entering a function
4. next / n: Run a program step by step without entering a function
5. continue / c: Run a program until finish or stop at a breakpoint
6. finish: Step out of the current function

**Set Breakpoints**

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
