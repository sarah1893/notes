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
provides many “debug commands” to inspect programs’ runtime status, its
non-intuitive usages impede programmers to use it to solve problems. Indeed,
mastering GDB is a long-term process. However, a quick start is not complicated;
you must unlearn what you have learned like Yoda. To better understand how to
use Python in GDB, the following sections will focus on discussing Python
interpreter in GDB.

Interacting with Python
-----------------------

GDB supports customizing commands by using ``define``. It is useful to run a
batch of commands to troubleshoot at the same time. For example, a developer
can display the current frame information by defining a ``sf`` command.

.. code-block:: bash

    # define in .gdbinit
    define sf
      where        # find out where the program is
      info args    # show arguments
      info locals  # show local variables
    end

However, writing a user-defined command may be inconvenient due to limited APIs.
Fortunately, by interacting with Python interpreter in GDB, developers can
utilize Python libraries to establish their debugging tool kits readily. The
following examples show how to use Python to simplify debugging processes.


Dump memory
~~~~~~~~~~~

Inspecting a process’s memory information is an effective way to troubleshoot
memory issues. Developers check memory address and dump information by

.. code-block:: python

    (gdb) info proc mapping
    process 4967
    Mapped address spaces:

          Start Addr           End Addr       Size     Offset objfile
    ...
      0x7ffffffde000     0x7ffffffff000    0x21000        0x0 [stack]
    ...
    (gdb) # dump stack
    (gdb) dump memory a.bin 0x7ffffffde000 0x7ffffffff000



.. code-block:: python

    import gdb
    import re

    class DumpMemory(gdb.Command):
        """Dump memory info into a file."""

        def __init__(self):
            super().__init__("dm", gdb.COMMAND_USER)

        def invoke(self, args, tty):
            try:
                pat, f = args.split()
                # cat /proc/self/maps
                out = gdb.execute("info proc mappings", tty, True)
                for l in out.split("\n"):
                    if re.match(f".*{pat}*", l.strip()):
                        # dump memory
                        s, e, *_ = l.split()
                        gdb.execute(f"dump memory {f} {s} {e}")
                        break
            except Exception as e:
                print("Usage: dm [pattern] [filename]")

    DumpMemory()

.. code-block:: bash

    (gdb) start
    ...
    (gdb) source mem.py        # source commands
    ...
    (gdb) dm heap a.bin        # dump heap to a.bin
    (gdb) shell strings a.bin  # display heap strings

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
2. `GNU GDB Debugger Command Cheat Sheet`_

.. _Extending GDB using Python: https://sourceware.org/gdb/onlinedocs/gdb/Python.html#Python
.. _GDB Text User Interface (TUI): https://sourceware.org/gdb/onlinedocs/gdb/TUI.html
.. _GNU GDB Debugger Command Cheat Sheet: http://www.yolinux.com/TUTORIALS/GDB-Commands.html
