.. meta::
    :description lang=en: Design philosophy of pep 572, the walrus operator
    :keywords: Python3, PEP 572, walrus operator


PEP 572 and The Walrus Operator
===============================

.. contents:: table of Contents
    :backlinks: none

Abstract
--------

PEP 572 is one of the most contentious proposals in Python3 history because
assigning a value within an expression seems unnecessary. Also, it is ambiguous
for developers to distinguish the difference between **the walrus operator**
(``:=``) and the equal operator (``=``). Even though sophisticated developers
can use ``:=`` smoothly, they may concern the readability of their code. To
better understand the usage of ``:=``, this article discusses its design
philosophy and what kind of problems it tries to solve.


Introduction
------------

For C/C++ developer, assigning a function return to a variable is common due
to error code style handling. Managing function errors includes two steps;
one is to check the return value; another is to check ``errno``. For example,

.. code-block:: c

    #include <stdio.h>
    #include <unistd.h>
    #include <string.h>
    #include <errno.h>

    int main(int argc, char *argv[]) {
        int rc = -1;

        // assign access return to rc and check its value
        if ((rc = access("hello_walrus", R_OK)) == -1) {
            fprintf(stderr, "%s", strerror(errno));
            goto end;
        }
        rc = 0;
    end:
        return rc;
    }

In this case, ``access`` will assign its return value to the variable ``rc``
first. Then, the program will compare the ``rc`` value with ``-1`` to check
whether the execution of ``access`` is successful or not. However, Python did
not allow assigning values to variables within an expression before 3.8. To fix
this problem, therefore, PEP 572 introduced the walrus operator for developers.
The following Python snippet is equal to the previous C example.

.. code-block:: python

    >>> import os
    >>> from ctypes import *
    >>> libc = CDLL("libc.dylib", use_errno=True)
    >>> access = libc.access
    >>> path = create_string_buffer(b"hello_walrus")
    >>> if (rc := access(path, os.R_OK)) == -1:
    ...     errno = get_errno()
    ...     print(os.strerror(errno), file=sys.stderr)
    ...
    No such file or directory


Why ``:=`` ?
------------

Developers may confuse the difference between ``:=`` and  ``=``. In fact, they
serve the same purpose, assigning somethings to variables. Why Python introduced
``:=`` instead of using ``=``? What is the benefit of using ``:=``? One
reason is from a common mistake made by C/C++ developers. For instance,

.. code-block:: c

    int rc = access("hello_walrus", R_OK);

    // rc is unintentionally assigned to -1
    if (rc = -1) {
        fprintf(stderr, "%s", strerror(errno));
        goto end;
    }

Rather than comparison, the variable, ``rc``, is mistakenly assigned to -1. To
prevent this error, some people advocate using `Yoda conditions`_ within an
expression.

.. code-block:: c

    int rc = access("hello_walrus", R_OK);

    // -1 = rc will raise a compile error
    if (-1 == rc) {
        fprintf(stderr, "%s", strerror(errno));
        goto end;
    }

However, Yoda style is not readable enough like Yoda speaks non-standardized
English. Also, unlike C/C++ can detect assigning error during the compile-time
via compiler options (e.g., -Wparentheses), it is difficult for Python interpreter
to distinguish such mistakes throughout the runtime. Thus, the final result
of PEP 572 was to use a new syntax as a solution to implement *assignment
expressions*.

The walrus operator was not the first solution for PEP 572. The original proposal
used ``EXPR as NAME`` to assign values to variables. Unfortunately, there are
some flaws in this solution and other solutions as well. After intense debates,
the final decision was ``:=``.


.. _Yoda conditions: https://en.wikipedia.org/wiki/Yoda_conditions

