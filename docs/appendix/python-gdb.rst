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

Troubleshooting software bugs is a big challenge for developers. While GDB
provides many "debug commands" to inspect programs' runtime status, its
non-intuitive usages impede programmers to use it to solve problems. Before
discussing how to interact with Python interpreter in GDB, this article lists
some common GDB commands in the following sections. Although mastering GDB is a
long-term process, a quickstart is not complicated; you must unlearn what you
have learned like Yoda.

Load an Executable
------------------

Using GDB to debug requires it recognizes a program's debug symbols. By
compiling with ``-g`` option, GDB will understand what source code looks like
after loading an executable file:

.. code-block:: bash

    $ gcc -g -Wall -Werror foo.c # compile with -g option
    $ gdb ./a.out  # load all symbols of a.out into GDB


Text User Interface
-------------------

Text User Interface (TUI) allows developers to visualize source code and to
debug like using the Integrated Development Environment (IDE) to trace problems.
For a beginner, entering the TUI mode is more understandable than the command
line mode. The following key bindings are the most common usages for interacting
with TUI.

1. Ctrl x + a - Enter or leave the TUI mode
2. Ctrl x + o - Switch the active window
3. Ctrl x + 1 - Display one window (e.g., source code + GDB shell)
4. Ctrl x + 2 - Display two windows (e.g., source code + GDB shell + assembly)
5. Ctrl l - Refresh window


Basic Commands
--------------

**Start/Stop a program**

1. start - Run an executable file and stop at the beginning
2. run / r - Run an executable file until finish or stop at a breakpoint
3. step / s - Run a program step by step with entering a function
4. next / n - Run a program step by step without entering a function
5. continue / c - Run a program until finish or stop at a breakpoint
6. finish - Step out of the current function

**Set Breakpoints**

1. b line - Set a breakpoint at the given line in the current file
2. b file: line - Set a breakpoint at the given line in a given file
3. b ... if cond - Set a breakpoint when the condition is true
4. clear line - Delete a breakpoint at the given line in the current file
5. clear file: line - Delete a breakpoint at giving a line in a given file
6. info breakpoints - Display breakpoints status
7. enable breakpoints - Enable breakpoints
8. disable breakpoints - Disable breakpoints
9. watch cond - Set a watchpoint for inspecting a value


**Display Stack**

1. backtrace / bt - Display current stack
2. frame / f framenum - Select a frame and inspect its status
3. where - Display the current stack and the line

**Print Variables**

1. print / p var - Print value of the given variable
2. ptype var - Print type info of the given variable
3. info args - Print function arguments
4. info locals - Print all local variables

**Reverse Run**

1. record - Start recording each instruction step
2. record stop - Stop recording
3. rn - Reverse next
4. rs - Reverse step

**Define a Function**

GDB provides an original way for developers to define a customized function.
The following snippet shows how to define a function to display the information
of the current stack.

.. code-block:: bash

    (gdb) define sf
    Type commands for definition of "sf".
    End with a line saying just "end".
    >where
    >info args
    >info locals
    >end

Interacting with Python
-----------------------

Customize Print
~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~

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
