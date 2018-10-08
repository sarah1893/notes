=======================
Python C API cheatsheet
=======================

.. contents:: Table of Contents
    :backlinks: none


Simple setup.py for c extension
----------------------------------

.. code-block:: python

    from distutils.core import setup, Extension

    ext = Extension('foo', sources=['foo.c'])
    setup(name="Foo", version="1.0", ext_modules=[ext])


Customize CFLAGS
-----------------

.. code-block:: python

    import sysconfig
    from distutils.core import setup, Extension

    cflags = sysconfig.get_config_var("CFLAGS")

    extra_compile_args = cflags.split()
    extra_compile_args += ["-Wextra"]

    ext = Extension(
        "foo", ["foo.c"],
        extra_compile_args=extra_compile_args
    )

    setup(name="foo", version="1.0", ext_modules=[ext])

Doc string
----------

.. code-block:: c

    PyDoc_STRVAR(doc_mod, "Module document\n");
    PyDoc_STRVAR(doc_foo, "foo() -> None\n\nFoo doc");

    static PyMethodDef methods[] = {
        {"foo", (PyCFunction)foo, METH_NOARGS, doc_foo},
        {NULL, NULL, 0, NULL}
    };

    static struct PyModuleDef module = {
        .m_base    = PyModuleDef_HEAD_INIT,
        .m_name    = "Foo",
        .m_doc     = doc_mod,
        .m_size    = -1,
        .m_methods = methods
    };


Simple C Extension
-------------------

foo.c

.. code-block:: c

    #include <Python.h>

    PyDoc_STRVAR(doc_mod, "Module document\n");
    PyDoc_STRVAR(doc_foo, "foo() -> None\n\nFoo doc");

    static PyObject* foo(PyObject* self)
    {
        PyObject* s = PyUnicode_FromString("foo");
        PyObject_Print(s, stdout, 0);
        Py_RETURN_NONE;
    }

    static PyMethodDef methods[] = {
        {"foo", (PyCFunction)foo, METH_NOARGS, doc_foo},
        {NULL, NULL, 0, NULL}
    };

    static struct PyModuleDef module = {
        PyModuleDef_HEAD_INIT, "Foo", doc_mod, -1, methods
    };

    PyMODINIT_FUNC PyInit_foo(void)
    {
        return PyModule_Create(&module);
    }

output:

.. code-block:: bash

    $ python setup.py -q build
    $ python setup.py -q install
    $ python -c "import foo; foo.foo()"
    'foo'

Get Reference Count
--------------------

.. code-block:: c

    #include <Python.h>

    static PyObject *
    getrefcount(PyObject *self, PyObject *a)
    {
        return PyLong_FromSsize_t(Py_REFCNT(a));
    }

    static PyMethodDef methods[] = {
        {"getrefcount", (PyCFunction)getrefcount, METH_O, NULL},
        {NULL, NULL, 0, NULL}
    };

    static struct PyModuleDef module = {
        PyModuleDef_HEAD_INIT, "foo", NULL, -1, methods
    };

    PyMODINIT_FUNC PyInit_foo(void)
    {
        return PyModule_Create(&module);
    }

output:

.. code-block:: bash

    $ python setup.py -q build
    $ python setup.py -q install
    $ python -q
    >>> import sys
    >>> import foo
    >>> l = [1, 2, 3]
    >>> sys.getrefcount(l[0])
    104
    >>> foo.getrefcount(l[0])
    104
    >>> i = l[0]
    >>> sys.getrefcount(l[0])
    105
    >>> foo.getrefcount(l[0])
    105

Parse Arguments
----------------

.. code-block:: c

    #include <Python.h>

    static PyObject *
    foo(PyObject *self)
    {
        return PyUnicode_FromString("no args");
    }

    static PyObject *
    bar(PyObject *self, PyObject *args)
    {
        int i = -1;
        const char *s = NULL;
        if (!PyArg_ParseTuple(args, "is", &i, &s)) return NULL;
        return PyUnicode_FromFormat("args(%d, %s)", i, s);
    }

    static PyMethodDef methods[] = {
        {"foo", (PyCFunction)foo, METH_NOARGS, NULL},
        {"bar", (PyCFunction)bar, METH_VARARGS, NULL},
        {NULL, NULL, 0, NULL}
    };

    static struct PyModuleDef module = {
        PyModuleDef_HEAD_INIT, "foo", NULL, -1, methods
    };

    PyMODINIT_FUNC PyInit_foo(void)
    {
        return PyModule_Create(&module);
    }

output:

.. code-block:: bash

    $ python setup.py -q build
    $ python setup.py -q install
    $ python -c 'import foo; print(foo.foo())'
    no args
    $ python -c 'import foo; print(foo.bar(1, "s"))'
    args(1, s)

Calling Python Functions from C
--------------------------------

.. code-block:: c

    #include <Python.h>

    static PyObject *
    foo(PyObject *self, PyObject *args)
    {
        PyObject *py_callback = NULL;
        PyObject *rv = NULL;

        if (!PyArg_ParseTuple(args, "O:callback", &py_callback))
            return NULL;

        if (!PyCallable_Check(py_callback)) {
            PyErr_SetString(PyExc_TypeError, "should be callable");
            return NULL;
        }

        // similar to py_callback("Awesome Python!")
        rv = PyObject_CallFunction(py_callback, "s", "Awesome Python!");
        return rv;
    }

    static PyMethodDef methods[] = {
        {"foo", (PyCFunction)foo, METH_VARARGS, NULL},
        {NULL, NULL, 0, NULL}
    };

    static struct PyModuleDef module = {
        PyModuleDef_HEAD_INIT, "foo", NULL, -1, methods
    };

    PyMODINIT_FUNC PyInit_foo(void)
    {
        return PyModule_Create(&module);
    }

output:

.. code-block:: bash

    $ python setup.py -q build
    $ python setup.py -q install
    $ python -c "import foo; foo.foo(print)"
    Awesome Python!

Raise Exception
----------------

.. code-block:: c

    #include <Python.h>

    PyDoc_STRVAR(doc_mod, "Module document\n");
    PyDoc_STRVAR(doc_foo, "foo() -> None\n\nFoo doc");

    static PyObject*
    foo(PyObject* self)
    {
        // raise NotImplementedError
        PyErr_SetString(PyExc_NotImplementedError, "Not implemented");
        return NULL;
    }

    static PyMethodDef methods[] = {
        {"foo", (PyCFunction)foo, METH_NOARGS, doc_foo},
        {NULL, NULL, 0, NULL}
    };

    static struct PyModuleDef module = {
        PyModuleDef_HEAD_INIT, "Foo", doc_mod, -1, methods
    };

    PyMODINIT_FUNC PyInit_foo(void)
    {
        return PyModule_Create(&module);
    }

output:

.. code-block::

    $ python setup.py -q build
    $ python setup.py -q install
    $ python -c "import foo; foo.foo(print)"
    $ python -c "import foo; foo.foo()"
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
    NotImplementedError: Not implemented

Customize Exception
--------------------

.. code-block:: c

    #include <stdio.h>
    #include <Python.h>

    static PyObject *FooError;

    PyDoc_STRVAR(doc_foo, "foo() -> void\n\n"
        "Equal to the following example:\n\n"
        "def foo():\n"
        "    raise FooError(\"Raise exception in C\")"
    );

    static PyObject *
    foo(PyObject *self __attribute__((unused)))
    {
        PyErr_SetString(FooError, "Raise exception in C");
        return NULL;
    }

    static PyMethodDef methods[] = {
        {"foo", (PyCFunction)foo, METH_NOARGS, doc_foo},
        {NULL, NULL, 0, NULL}
    };

    static struct PyModuleDef module = {
        PyModuleDef_HEAD_INIT, "foo", "doc", -1, methods
    };

    PyMODINIT_FUNC PyInit_foo(void)
    {
        PyObject *m = NULL;
        m = PyModule_Create(&module);
        if (!m) return NULL;

        FooError = PyErr_NewException("foo.FooError", NULL, NULL);
        Py_INCREF(FooError);
        PyModule_AddObject(m, "FooError", FooError);
        return m;
    }


output:

.. code-block:: bash

    $ python setup.py -q build
    $ python setup.py -q install
    $ python -c "import foo; foo.foo()"
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
    foo.FooError: Raise exception in C

Iterate a List
---------------

.. code-block:: c

    #include <Python.h>

    #define PY_PRINTF(o) \
        PyObject_Print(o, stdout, 0); printf("\n");

    static PyObject *
    iter_list(PyObject *self, PyObject *args)
    {
        PyObject *list = NULL, *item = NULL, *iter = NULL;
        PyObject *result = NULL;

        if (!PyArg_ParseTuple(args, "O", &list))
            goto error;

        if (!PyList_Check(list))
            goto error;

        // Get iterator
        iter = PyObject_GetIter(list);
        if (!iter)
            goto error;

        // Display items (using PyIter_Next)
        //
        // Similar to
        //
        // for i in arr: print(i)
        //
        while ((item = PyIter_Next(iter)) != NULL) {
            PY_PRINTF(item);
            Py_XDECREF(item);
        }

        Py_XINCREF(Py_None);
        result = Py_None;
    error:
        Py_XDECREF(iter);
        return result;
    }

    static PyMethodDef methods[] = {
        {"iter_list", (PyCFunction)iter_list, METH_VARARGS, NULL},
        {NULL, NULL, 0, NULL}
    };

    static struct PyModuleDef module = {
        PyModuleDef_HEAD_INIT, "foo", NULL, -1, methods
    };

    PyMODINIT_FUNC PyInit_foo(void)
    {
        return PyModule_Create(&module);
    }

output:

.. code-block:: bash

    $ python setup.py -q build
    $ python setup.py -q install
    $ python -c "import foo; foo.iter_list([1,2,3])"
    1
    2
    3

Iterate a Dictionary
---------------------

.. code-block:: c

    #include <Python.h>

    #define PY_PRINTF(o) \
        PyObject_Print(o, stdout, 0); printf("\n");

    static PyObject *
    iter_dict(PyObject *self, PyObject *args)
    {
        PyObject *dict = NULL;
        PyObject *key = NULL, *val = NULL;
        PyObject *o = NULL, *result = NULL;
        Py_ssize_t pos = 0;

        if (!PyArg_ParseTuple(args, "O", &dict))
            goto error;

        // Display keys and values (using PyDict_Next)
        //
        // Similar to
        //
        // for k, v in d.items():
        //     print(f"({k}, {v})")
        //
        while (PyDict_Next(dict, &pos, &key, &val)) {
            o = PyUnicode_FromFormat("(%S, %S)", key, val);
            if (!o) continue;
            PY_PRINTF(o);
            Py_XDECREF(o);
        }

        Py_INCREF(Py_None);
        result = Py_None;
    error:
        return result;
    }

    static PyMethodDef methods[] = {
        {"iter_dict", (PyCFunction)iter_dict, METH_VARARGS, NULL},
        {NULL, NULL, 0, NULL}
    };

    static struct PyModuleDef module = {
        PyModuleDef_HEAD_INIT, "foo", NULL, -1, methods
    };

    PyMODINIT_FUNC PyInit_foo(void)
    {
        return PyModule_Create(&module);
    }

output:

.. code-block:: bash

    $ python setup.py -q build
    $ python setup.py -q install
    $ python -c "import foo; foo.iter_dict({'k': 'v'})"
    '(k, v)'

Run a Python command from C
----------------------------

.. code-block:: c

    #include <stdio.h>
    #include <Python.h>

    int
    main(int argc, char *argv[])
    {
        int rc = -1;
        Py_Initialize();
        rc = PyRun_SimpleString(argv[1]);
        Py_Finalize();
        return rc;
    }

output:

.. code-block:: bash

    $ clang `python3-config --cflags` -c foo.c -o foo.o
    $ clang `python3-config --ldflags` foo.o -o foo
    $ ./foo "print('Hello Python')"
    Hello Python

Run a Python file from C
-------------------------

.. code-block:: c

    #include <stdio.h>
    #include <Python.h>

    int
    main(int argc, char *argv[])
    {
        int rc = -1, i = 0;
        wchar_t **argv_copy = NULL;
        const char *filename = NULL;
        FILE *fp = NULL;
        PyCompilerFlags cf = {.cf_flags = 0};

        filename = argv[1];
        fp = fopen(filename, "r");
        if (!fp)
            goto error;

        // copy argv
        argv_copy = PyMem_RawMalloc(sizeof(wchar_t*) * argc);
        if (!argv_copy)
            goto error;

        for (i = 0; i < argc; i++) {
            argv_copy[i] = Py_DecodeLocale(argv[i], NULL);
            if (argv_copy[i]) continue;
            fprintf(stderr, "Unable to decode the argument");
            goto error;
        }

        Py_Initialize();
        Py_SetProgramName(argv_copy[0]);
        PySys_SetArgv(argc, argv_copy);
        rc = PyRun_AnyFileExFlags(fp, filename, 0, &cf);

    error:
        if (argv_copy) {
            for (i = 0; i < argc; i++)
                PyMem_RawFree(argv_copy[i]);
            PyMem_RawFree(argv_copy);
        }
        if (fp) fclose(fp);
        Py_Finalize();
        return rc;
    }

output:

.. code-block:: bash

    $ clang `python3-config --cflags` -c foo.c -o foo.o
    $ clang `python3-config --ldflags` foo.o -o foo
    $ echo "import sys; print(sys.argv)" > foo.py
    $ ./foo foo.py arg1 arg2 arg3
    ['./foo', 'foo.py', 'arg1', 'arg2', 'arg3']

Import Python Module in C
--------------------------

.. code-block:: c

    #include <stdio.h>
    #include <Python.h>

    #define PYOBJECT_CHECK(obj, label) \
        if (!obj) { \
            PyErr_Print(); \
            goto label; \
        }

    int
    main(int argc, char *argv[])
    {
        int rc = -1;
        wchar_t *program = NULL;
        PyObject *json_module = NULL, *json_dict = NULL;
        PyObject *json_dumps = NULL;
        PyObject *dict = NULL;
        PyObject *result = NULL;

        program = Py_DecodeLocale(argv[0], NULL);
        if (!program) {
            fprintf(stderr, "unable to decode the program name");
            goto error;
        }

        Py_SetProgramName(program);
        Py_Initialize();

        // import json
        json_module = PyImport_ImportModule("json");
        PYOBJECT_CHECK(json_module, error);

        // get json.__dict__
        json_dict = PyModule_GetDict(json_module);
        PYOBJECT_CHECK(json_dict, error);

        // get json.__dict__['dumps']
        json_dumps = PyDict_GetItemString(json_dict, "dumps");
        PYOBJECT_CHECK(json_dumps, error);

        // dict = {'foo': 'Foo', 'bar': 123}
        dict = Py_BuildValue("({sssi})", "foo", "Foo", "bar", 123);
        PYOBJECT_CHECK(dict, error);

        // json.dumps(dict)
        result = PyObject_CallObject(json_dumps, dict);
        PYOBJECT_CHECK(result, error);
        PyObject_Print(result, stdout, 0);
        printf("\n");
    error:
        Py_XDECREF(result);
        Py_XDECREF(dict);
        Py_XDECREF(json_dumps);
        Py_XDECREF(json_dict);
        Py_XDECREF(json_module);

        PyMem_RawFree(program);
        Py_Finalize();
        return rc;
    }

output:

.. code-block:: bash

    $ clang `python3-config --cflags` -c foo.c -o foo.o
    $ clang `python3-config --ldflags` foo.o -o foo
    $ ./foo
    '{"foo": "Foo", "bar": 123}'

Performance of c api
---------------------

.. code-block:: c

    #include <Python.h>

    static unsigned long
    fib(unsigned long n)
    {
        if (n < 2) return n;
        return fib(n - 1) + fib(n - 2);
    }

    static PyObject *
    fibonacci(PyObject *self, PyObject *args)
    {
        unsigned long n = 0;
        if (!PyArg_ParseTuple(args, "k", &n)) return NULL;
        return PyLong_FromUnsignedLong(fib(n));
    }

    static PyMethodDef methods[] = {
        {"fib", (PyCFunction)fibonacci, METH_VARARGS, NULL},
        {NULL, NULL, 0, NULL}
    };

    static struct PyModuleDef module = {
        PyModuleDef_HEAD_INIT, "foo", NULL, -1, methods
    };

    PyMODINIT_FUNC PyInit_foo(void)
    {
        return PyModule_Create(&module);
    }


Compare the performance with pure Python

.. code-block:: python

    >>> from time import time
    >>> import foo
    >>> def fib(n):
    ...     if n < 2: return n
    ...     return fib(n - 1) + fib(n - 2)
    ...
    >>> s = time(); _ = fib(35); e = time(); e - s
    4.953313112258911
    >>> s = time(); _ = foo.fib(35); e = time(); e - s
    0.04628586769104004

Performance of ctypes
----------------------

.. code-block:: c

    // Compile (Mac)
    // -------------
    //
    //   $ clang -Wall -Werror -shared -fPIC -o libfib.dylib fib.c
    //
    unsigned int fib(unsigned int n)
    {
        if ( n < 2) {
            return n;
        }
        return fib(n-1) + fib(n-2);
    }

Compare the performance with pure Python

.. code-block:: python

    >>> from time import time
    >>> from ctypes import CDLL
    >>> def fib(n):
    ...     if n < 2: return n
    ...     return fib(n - 1) + fib(n - 2)
    ...
    >>> cfib = CDLL("./libfib.dylib").fib
    >>> s = time(); _ = fib(35); e = time(); e - s
    4.918856859207153
    >>> s = time(); _ = cfib(35); e = time(); e - s
    0.07283687591552734

Error handling when using ctypes
---------------------------------

.. code-block:: python

    from __future__ import print_function

    import os

    from ctypes import *
    from sys import platform, maxsize

    is_64bits = maxsize > 2 ** 32

    if is_64bits and platform == "darwin":
        libc = CDLL("libc.dylib", use_errno=True)
    else:
        raise RuntimeError("Not support platform: {}".format(platform))

    stat = libc.stat

    class Stat(Structure):
        """
        From /usr/include/sys/stat.h

        struct stat {
            dev_t         st_dev;
            ino_t         st_ino;
            mode_t        st_mode;
            nlink_t       st_nlink;
            uid_t         st_uid;
            gid_t         st_gid;
            dev_t         st_rdev;
        #ifndef _POSIX_SOURCE
            struct      timespec st_atimespec;
            struct      timespec st_mtimespec;
            struct      timespec st_ctimespec;
        #else
            time_t        st_atime;
            long          st_atimensec;
            time_t        st_mtime;
            long          st_mtimensec;
            time_t        st_ctime;
            long          st_ctimensec;
        #endif
            off_t         st_size;
            int64_t       st_blocks;
            u_int32_t     st_blksize;
            u_int32_t     st_flags;
            u_int32_t     st_gen;
            int32_t       st_lspare;
            int64_t       st_qspare[2];
        };
        """
        _fields_ = [
            ("st_dev", c_ulong),
            ("st_ino", c_ulong),
            ("st_mode", c_ushort),
            ("st_nlink", c_uint),
            ("st_uid", c_uint),
            ("st_gid", c_uint),
            ("st_rdev", c_ulong),
            ("st_atime", c_longlong),
            ("st_atimendesc", c_long),
            ("st_mtime", c_longlong),
            ("st_mtimendesc", c_long),
            ("st_ctime", c_longlong),
            ("st_ctimendesc", c_long),
            ("st_size", c_ulonglong),
            ("st_blocks", c_int64),
            ("st_blksize", c_uint32),
            ("st_flags", c_uint32),
            ("st_gen", c_uint32),
            ("st_lspare", c_int32),
            ("st_qspare", POINTER(c_int64) * 2),
        ]

    # stat success
    path = create_string_buffer(b"/etc/passwd")
    st = Stat()
    ret = stat(path, byref(st))
    assert ret == 0

    # if stat fail, check errno
    path = create_string_buffer(b"&%$#@!")
    st = Stat()
    ret = stat(path, byref(st))
    if ret != 0:
        errno = get_errno()  # get errno
        errmsg = "stat({}) failed. {}".format(path.raw, os.strerror(errno))
        raise OSError(errno, errmsg)

output:

.. code-block:: console

    $ python err_handling.py   # python2
    Traceback (most recent call last):
      File "err_handling.py", line 85, in <module>
        raise OSError(errno_, errmsg)
    OSError: [Errno 2] stat(&%$#@!) failed. No such file or directory

    $ python3 err_handling.py  # python3
    Traceback (most recent call last):
      File "err_handling.py", line 85, in <module>
        raise OSError(errno_, errmsg)
    FileNotFoundError: [Errno 2] stat(b'&%$#@!\x00') failed. No such file or directory
