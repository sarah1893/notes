=======================
Python C API cheatsheet
=======================

.. contents:: Table of Contents
    :backlinks: none


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

Compare the performance

.. code-block:: python

    >>> import time
    >>> from ctypes import *
    >>> def fib(n):
    ...     if n < 2:
    ...         return n
    ...     return fib(n-1) + fib(n-2)
    ...
    >>> s = time.time(); fib(35); e = time.time()
    9227465
    >>> print("cost time: {} sec".format(e - s))
    cost time: 4.09563493729 sec
    >>> libfib = CDLL("./libfib.dylib")
    >>> s = time.time(); libfib.fib(35); e = time.time()
    9227465
    >>> print("cost time: {} sec".format(e - s))
    cost time: 0.0819959640503 sec

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
        PyModuleDef_HEAD_INIT,  /* m_base    */
        "Foo",                  /* m_name    */
        doc_mod,                /* m_doc     */
        -1,                     /* m_size    */
        methods                 /* m_methods */
    };


Simple C Extension
-------------------

foo.c

.. code-block:: c

    #include <stdio.h>
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
        PyObject *u = NULL;
        if (!PyArg_ParseTuple(args, "is", &i, &s)) return NULL;

        u = PyUnicode_FromFormat("args(%d, %s)", i, s);
        return u;
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

Raise Exception
----------------

.. code-block:: c

    static PyObject* foo(PyObject* self)
    {
        // equal to raise NotImplementedError
        PyErr_SetString(
            PyExc_NotImplementedError, "Not implemented"
        );
        return NULL;
    }

Reference:

- `Standard Exceptions`_

.. _Standard Exceptions: https://docs.python.org/3/c-api/exceptions.html

Customize Exception
--------------------

.. code-block:: c

    #include <stdio.h>
    #include <Python.h>

    static PyObject *FooError;

    PyDoc_STRVAR(doc_foo, "foo() -> void\n"
        "\n"
        "Equal to the following example:\n"
        "\n"
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

PyObject with Member and Methods
--------------------------------

C API source
~~~~~~~~~~~~


.. code-block:: c

    #include <Python.h>
    #include <structmember.h>

    typedef struct {
        PyObject_HEAD
        PyObject *hello;
        PyObject *world;
        int spam_id;
    } spamObj;

    static void
    spamdealloc(spamObj *self)
    {
        Py_XDECREF(self->hello);
        Py_XDECREF(self->world);
        self->ob_type
            ->tp_free((PyObject*)self);
    }

    /* __new__ */
    static PyObject *
    spamNew(PyTypeObject *type, PyObject *args, PyObject *kwds)
    {
        spamObj *self = NULL;

        self = (spamObj *)
               type->tp_alloc(type, 0);
        if (self == NULL) {
            goto END;
        }
        /* alloc str to hello */
        self->hello =
            PyString_FromString("");
        if (self->hello == NULL)
        {
            Py_XDECREF(self);
            self = NULL;
            goto END;
        }
        /* alloc str to world */
        self->world =
            PyString_FromString("");
        if (self->world == NULL)
        {
            Py_XDECREF(self);
            self = NULL;
            goto END;
        }
        self->spam_id = 0;
    END:
        return (PyObject *)self;
    }

    /* __init__ */
    static int
    spamInit(spamObj *self, PyObject *args, PyObject *kwds)
    {
        int ret = -1;
        PyObject *hello=NULL,
                 *world=NULL,
                 *tmp=NULL;

        static char *kwlist[] = {
            "hello",
            "world",
            "spam_id", NULL};

        /* parse input arguments */
        if (! PyArg_ParseTupleAndKeywords(
              args, kwds,
              "|OOi",
              kwlist,
              &hello, &world,
              &self->spam_id)) {
            goto END;
        }
        /* set attr hello */
        if (hello) {
            tmp = self->hello;
            Py_INCREF(hello);
            self->hello = hello;
            Py_XDECREF(tmp);
        }
        /* set attr world */
        if (world) {
            tmp = self->world;
            Py_INCREF(world);
            self->world = world;
            Py_XDECREF(tmp);
        }
        ret = 0;
    END:
        return ret;
    }

    static long
    fib(long n) {
        if (n<=2) {
            return 1;
        }
        return fib(n-1)+fib(n-2);
    }

    static PyObject *
    spamFib(spamObj *self, PyObject *args)
    {
        PyObject  *ret = NULL;
        long arg = 0;

        if (!PyArg_ParseTuple(args, "i", &arg)) {
            goto END;
        }
        ret = PyInt_FromLong(fib(arg));
    END:
        return ret;
    }

    //ref: python doc
    static PyMemberDef spam_members[] = {
        /* spameObj.hello*/
        {"hello",                   //name
         T_OBJECT_EX,               //type
         offsetof(spamObj, hello),  //offset
         0,                         //flags
         "spam hello"},             //doc
        /* spamObj.world*/
        {"world",
         T_OBJECT_EX,
         offsetof(spamObj, world),
         0,
         "spam world"},
        /* spamObj.spam_id*/
        {"spam_id",
         T_INT,
         offsetof(spamObj, spam_id),
         0,
         "spam id"},
        /* Sentiel */
        {NULL}
    };

    static PyMethodDef spam_methods[] = {
        /* fib */
        {"spam_fib",
         (PyCFunction)spamFib,
         METH_VARARGS,
         "Calculate fib number"},
        /* Sentiel */
        {NULL}
    };

    static PyMethodDef module_methods[] = {
        {NULL}  /* Sentinel */
    };

    static PyTypeObject spamKlass = {
        PyObject_HEAD_INIT(NULL)
        0,                               //ob_size
        "spam.spamKlass",                //tp_name
        sizeof(spamObj),                 //tp_basicsize
        0,                               //tp_itemsize
        (destructor) spamdealloc,        //tp_dealloc
        0,                               //tp_print
        0,                               //tp_getattr
        0,                               //tp_setattr
        0,                               //tp_compare
        0,                               //tp_repr
        0,                               //tp_as_number
        0,                               //tp_as_sequence
        0,                               //tp_as_mapping
        0,                               //tp_hash
        0,                               //tp_call
        0,                               //tp_str
        0,                               //tp_getattro
        0,                               //tp_setattro
        0,                               //tp_as_buffer
        Py_TPFLAGS_DEFAULT |
        Py_TPFLAGS_BASETYPE,             //tp_flags
        "spamKlass objects",             //tp_doc
        0,                               //tp_traverse
        0,                               //tp_clear
        0,                               //tp_richcompare
        0,                               //tp_weaklistoffset
        0,                               //tp_iter
        0,                               //tp_iternext
        spam_methods,                    //tp_methods
        spam_members,                    //tp_members
        0,                               //tp_getset
        0,                               //tp_base
        0,                               //tp_dict
        0,                               //tp_descr_get
        0,                               //tp_descr_set
        0,                               //tp_dictoffset
        (initproc)spamInit,              //tp_init
        0,                               //tp_alloc
        spamNew,                         //tp_new
    };

    /* declarations for DLL import */
    #ifndef PyMODINIT_FUNC
    #define PyMODINIT_FUNC void
    #endif

    PyMODINIT_FUNC
    initspam(void)
    {
        PyObject* m;

        if (PyType_Ready(&spamKlass) < 0) {
            goto END;
        }

        m = Py_InitModule3(
          "spam",         // Mod name
          module_methods, // Mod methods
          "Spam Module"); // Mod doc

        if (m == NULL) {
            goto END;
        }
        Py_INCREF(&spamKlass);
        PyModule_AddObject(
          m,                           // Module
          "SpamKlass",                 // Class Name
          (PyObject *) &spamKlass);    // Class
    END:
        return;
    }

Compare performance with pure Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> import spam
    >>> o = spam.SpamKlass()
    >>> def profile(func):
    ...     def wrapper(*args, **kwargs):
    ...         s = time.time()
    ...         ret = func(*args, **kwargs)
    ...         e = time.time()
    ...         print(e-s)
    ...     return wrapper
    ...
    >>> def fib(n):
    ...     if n <= 2:
    ...         return n
    ...     return fib(n-1)+fib(n-2)
    ...
    >>> @profile
    ... def cfib(n):
    ...     o.spam_fib(n)
    ...
    >>> @profile
    ... def pyfib(n):
    ...     fib(n)
    ...
    >>> cfib(30)
    0.0106310844421
    >>> pyfib(30)
    0.399799108505
