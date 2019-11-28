.. meta::
    :description lang=en: Design philosophy of pep 572, the walrus operator
    :keywords: Python3, PEP 572, walrus operator


PEP 572 and The Walrus Operator
===============================

PEP 572 is one of the most significant proposals in Python3 history. After
finishing this proposal, Guido van Rossum decided to resign as a Python leader.
This article tries to discuss what kind of problems that the walrus operator
(``:=``) is to try to solve.

.. contents:: table of Contents
    :backlinks: none


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
