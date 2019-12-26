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
use Python in GDB, this article will focus on discussing Python interpreter in
GDB.

Define Commands
---------------

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
following sections show how to use Python to simplify debugging processes.

Highlight Syntax
----------------

Syntax highlighting is useful for developers to trace source code or to
troubleshoot issues. By using ``pygents``, applying color to the source is easy
without defining ANSI escape code manually. The following example shows how to
apply color to the ``list`` command output.

.. code-block:: python

    import gdb

    from pygments import highlight
    from pygments.lexers import CLexer
    from pygments.formatters import TerminalFormatter

    class PrettyList(gdb.Command):
        """Print source code with color."""

        def __init__(self):
            super().__init__("pl", gdb.COMMAND_USER)
            self.lex = CLexer()
            self.fmt = TerminalFormatter()

        def invoke(self, args, tty):
            try:
                out = gdb.execute(f"l {args}", tty, True)
                print(highlight(out, self.lex, self.fmt))
            except Exception as e:
                print(e)

    PrettyList()

Dump JSON
---------

Parsing JSON is helpful when a developer is inspecting a JSON string in a
running program. GDB can parse a ``std::string`` via ``gdb.parse_and_eval``
and return it as a ``gdb.Value``. By processing ``gdb.Value``, developers can
pass a JSON string into Python ``json`` API and print it in a pretty format.

.. code-block:: python

    # dj.py
    import gdb
    import re
    import json

    class DumpJson(gdb.Command):
        """Dump std::string as a styled JSON."""

        def __init__(self):
            super().__init__("dj", gdb.COMMAND_USER)

        def get_json(self, args):
            """Parse std::string to JSON string."""
            ret = gdb.parse_and_eval(args)
            typ = str(ret.type)
            if re.match("^std::.*::string", typ):
                return json.loads(str(ret))
            return None

        def invoke(self, args, tty):
            try:
                # string to json string
                s = self.get_json(args)
                # json string to object
                o = json.loads(s)
                print(json.dumps(o, indent=2))
            except Exception as e:
                print(f"Parse json error! {args}")

    DumpJson()

The command ``dj`` displays a more readable JSON format in GDB. This command
helps improve visual recognization when a JSON string large. Also, by using
this command, it can detect or monitor whether a ``std::string`` is JSON or
not.

.. code-block:: bash

    (gdb) start
    (gdb) list
    1       #include <string>
    2
    3       int main(int argc, char *argv[])
    4       {
    5           std::string json = R"({"foo": "FOO","bar": "BAR"})";
    6           return 0;
    7       }
    ...
    (gdb) ptype json
    type = std::string
    (gdb) p json
    $1 = "{\"foo\": \"FOO\",\"bar\": \"BAR\"}"
    (gdb) source dj.py
    (gdb) dj json
    {
      "foo": "FOO",
      "bar": "BAR"
    }

Dump Memory
-----------

Inspecting a process’s memory information is an effective way to troubleshoot
memory issues. Developers can acquire memory contents by ``info proc mappings``
and ``dump memory``. To simplify these steps, defining a customized command is
useful. However, the implementation is not straightforward by using pure GDB
syntax. Even though GDB supports conditions, processing output is not intuitive.
To solve this problem, using Python API in GDB would be helpful because Python
contains many useful operations for handling strings.

.. code-block:: python

    # mem.py
    import gdb
    import time
    import re

    class DumpMemory(gdb.Command):
        """Dump memory info into a file."""

        def __init__(self):
            super().__init__("dm", gdb.COMMAND_USER)

        def get_addr(self, p, tty):
            """Get memory addresses."""
            cmd = "info proc mappings"
            out = gdb.execute(cmd, tty, True)
            addrs = []
            for l in out.split("\n"):
                if re.match(f".*{p}*", l):
                    s, e, *_ = l.split()
                    addrs.append((s, e))
            return addrs

        def dump(self, addrs):
            """Dump memory result."""
            if not addrs:
                return

            for s, e in addrs:
                f = int(time.time() * 1000)
                gdb.execute(f"dump memory {f}.bin {s} {e}")

        def invoke(self, args, tty):
            try:
                # cat /proc/self/maps
                addrs = self.get_addr(args, tty)
                # dump memory
                self.dump(addrs)
            except Exception as e:
                print("Usage: dm [pattern]")

    DumpMemory()


Running the ``dm`` command will invoke ``DumpMemory.invoke``. By sourcing
or implementing Python scripts in *.gdbinit*, developers can utilize
user-defined commands to trace bugs when a program is running. For example, the
following steps show how to invoke ``DumpMemory`` in GDB.

.. code-block:: bash

    (gdb) start
    ...
    (gdb) source mem.py  # source commands
    (gdb) dm stack       # dump stack to ${timestamp}.bin
    (gdb) shell ls       # ls current dir
    1577283091687.bin  a.cpp  a.out  mem.py

Inspect a Function
------------------

.. code-block:: cpp


    #include <iostream>

    int fib(int n)
    {
        if (n < 2) {
            return 1;
        }
        return fib(n-1) + fib(n-2);
    }

    int main(int argc, char *argv[])
    {
        std::cout << fib(3) << std::endl;
        return 0;
    }


.. code-block:: bash

    (gdb) break fib
    Breakpoint 3 at 0x555555554896: file a.cpp, line 5.
    (gdb) commands
    Type commands for breakpoint(s) 3, one per line.
    End with a line saying just "end".
    >  silent
    >  backtrace
    >  continue
    >end

Reference
---------

1. `Extending GDB using Python`_
2. `GNU GDB Debugger Command Cheat Sheet`_

.. _Extending GDB using Python: https://sourceware.org/gdb/onlinedocs/gdb/Python.html#Python
.. _GDB Text User Interface (TUI): https://sourceware.org/gdb/onlinedocs/gdb/TUI.html
.. _GNU GDB Debugger Command Cheat Sheet: http://www.yolinux.com/TUTORIALS/GDB-Commands.html
