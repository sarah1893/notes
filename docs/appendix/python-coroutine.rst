.. meta::
    :keywords: Python, Python3, coroutine, asyncio

===============================================
A Hitchhikers Guide to Asynchronous Programming
===============================================

.. contents:: Table of Contents
    :backlinks: none

Abstract
--------

The `C10k problem`_ is still a puzzle for a programmer to find a way to solve
it. Generally, developers deal with extensive I/O operations via **thread**,
**epoll**, or **kqueue** to avoid their software waiting for an expensive task.
However, developing a readable and bug-free concurrent code is challenging due
to data sharing and job dependency. Even though some powerful tools, such as
`Valgrind`_, help developers to detect deadlock or other asynchronous issues,
solving these problems may be time-consuming when the scale of software grows
large. Therefore, many programming languages such as Python, Javascript, or C++
dedicated to developing better libraries, frameworks, or syntaxes to assist
programmers in managing concurrent jobs properly. Instead of focusing on how to
use modern parallel APIs, this article mainly concentrates on the design
philosophy behind programming patterns.

Introduction
------------

Handling I/O operations such as network connections is one of the most expensive
tasks in a program. Take a simple TCP blocking echo server as an example
(The following snippet). If a client connects to the server successfully without
sending any request, it blocks others' connections. Even though clients send data
as soon as possible, the server cannot handle other requests if there is no
client tries to establish a connection. Also, handling multiple requests is
inefficient because it wastes a lot of time waiting for I/O responses from
hardware such as network interfaces. Thus, socket programming with concurrency
becomes inevitable to manage extensive requests.

.. code-block:: python

    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 5566))
    s.listen(10)

    while True:
        conn, addr = s.accept()
        msg = conn.recv(1024)
        conn.send(msg)

One possible solution to prevent a server waiting for I/O operations is to
dispatch tasks to other threads. The following example shows how to create a
thread to handle connections simultaneously. However, creating numerous threads
may consume all computing power without high throughput. Even worse, an
application may waste time waiting for a lock to process critical sections within
a thread. Although using threads can solve blocking issues for a socket server,
other factors, such as CPU utilization, are essential for a programmer to
overcome the C10k problem. Therefore, without creating unlimited threads, the
event loop is another solution to manage connections.

.. code-block:: python

    import threading
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 5566))
    s.listen(10240)

    def handler(conn):
        while True:
            msg = conn.recv(65535)
            conn.send(msg)

    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=handler, args=(conn,))
        t.start()

A simple event-driven socket server includes three main components: an I/O
multiplexing module (e.g., `select`_), a scheduler (loop), and callback
functions (events). For example, the following server utilizes the high-level
I/O multiplexing, `selectors`_, within a loop to check whether an I/O operation
is ready or not. If data is available to read/write, the loop acquires I/O
events and execute callback functions, ``accept``, ``read``, or ``write``, to
finish tasks.

.. code-block:: python

    import socket

    from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE
    from functools import partial

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 5566))
    s.listen(10240)
    s.setblocking(False)

    sel = DefaultSelector()

    def accept(s, mask):
        conn, addr = s.accept()
        conn.setblocking(False)
        sel.register(conn, EVENT_READ, read)

    def read(conn, mask):
        msg = conn.recv(65535)
        if not msg:
            sel.unregister(conn)
            return conn.close()
        sel.modify(conn, EVENT_WRITE, partial(write, msg=msg))

    def write(conn, mask, msg=None):
        if msg:
            conn.send(msg)
        sel.modify(conn, EVENT_READ, read)

    sel.register(s, EVENT_READ, accept)
    while True:
        events = sel.select()
        for e, m in events:
            cb = e.data
            cb(e.fileobj, m)

Although managing connections via threads may not be efficient, a program that
utilizes an event loop to schedule tasks isn’t easy to read. To enhance code
readability, many programming languages, including Python, introduce abstract
concepts such as coroutine, future, or async/await to handle I/O multiplexing.
To better understand programming jargon and using them correctly, the following
sections discuss what these concepts are and what kind of problems they try to
solve.

Callback Functions
------------------

A callback function is used to control data flow at runtime when an event is
invoked. However, preserving current callback function's status is challenging.
For example, if a programmer wants to implement a handshake over a TCP server,
he/she may require to store previous status in some where.

.. code-block:: python

    import socket

    from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE
    from functools import partial

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 5566))
    s.listen(10240)
    s.setblocking(False)

    sel = DefaultSelector()
    is_hello = {}

    def accept(s, mask):
        conn, addr = s.accept()
        conn.setblocking(False)
        is_hello[conn] = False;
        sel.register(conn, EVENT_READ, read)

    def read(conn, mask):
        msg = conn.recv(65535)
        if not msg:
            sel.unregister(conn)
            return conn.close()

        # check whether handshake is successful or not
        if is_hello[conn]:
            sel.modify(conn, EVENT_WRITE, partial(write, msg=msg))
            return

        # do a handshake
        if msg.decode("utf-8").strip() != "hello":
            sel.unregister(conn)
            return conn.close()

        is_hello[conn] = True

    def write(conn, mask, msg=None):
        if msg:
            conn.send(msg)
        sel.modify(conn, EVENT_READ, read)

    sel.register(s, EVENT_READ, accept)
    while True:
        events = sel.select()
        for e, m in events:
            cb = e.data
            cb(e.fileobj, m)



Although the variable ``is_hello`` assists in storing status to check whether a
handshake is successful or not, the code becomes harder for a programmer to
understand. In fact, the concept of the previous implementation is simple. It
is equal to the following snippet (blocking version).

.. code-block:: python

    def accept(s):
        conn, addr = s.accept()
        success = handshake(conn)
        if not success:
            conn.close()

    def handshake(conn):
        data = conn.recv(65535)
        if not data:
            return False
        if data.decode('utf-8').strip() != "hello":
            return False
        conn.send(b"hello")
        return True

To migrate the similar structure from blocking to non-blocking, a function (or
a task) requires to snapshot the current status, including arguments, variables,
and breakpoints, when it needs to wait for I/O operations. Also, the scheduler
should be able to re-entry the function and execute the remaining code after
I/O operations finish. Unlike other programming languages such as C++, Python can
achieve the concepts discussed above easily because its **generator** can preserve
all status and re-entry by calling the built-in function ``next()``. By utilizing
generators, handling I/O operations like the previous snippet but a non-blocking
form, which is called *inline callback*, is reachable inside an event loop.

Event Loop
----------

An event loop is a scheduler to manage tasks within a program instead of
operating systems. The following snippet shows how a simple event loop to
handle socket connections asynchronously. The implementation concept is to
append tasks into a FIFO job queue and register a *selector* when I/O operations
are not ready. Also, a *generator* preserves the status of a task that allows
it to be able to execute its remaining jobs without callback functions when
I/O results are available. By observing how an event loop works, therefore, it
would assist in understanding a Python *generator* is indeed a form of
*coroutine*.

.. code-block:: python

    # loop.py

    from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

    class Loop(object):
        def __init__(self):
            self.sel = DefaultSelector()
            self.queue = []

        def create_task(self, task):
            self.queue.append(task)

        def polling(self):
            for e, m in self.sel.select(0):
                self.queue.append((e.data, None))
                self.sel.unregister(e.fileobj)

        def is_registered(self, fileobj):
            try:
                self.sel.get_key(fileobj)
            except KeyError:
                return False
            return True

        def register(self, t, data):
            if not data:
                return False

            if data[0] == EVENT_READ:
                if self.is_registered(data[1]):
                    self.sel.modify(data[1], EVENT_READ, t)
                else:
                    self.sel.register(data[1], EVENT_READ, t)
            elif data[0] == EVENT_WRITE:
                if self.is_registered(data[1]):
                    self.sel.modify(data[1], EVENT_WRITE, t)
                else:
                    self.sel.register(data[1], EVENT_WRITE, t)
            else:
                return False

            return True

        def accept(self, s):
            conn, addr = None, None
            while True:
                try:
                    conn, addr = s.accept()
                except BlockingIOError:
                    yield (EVENT_READ, s)
                else:
                    break
            return conn, addr

        def recv(self, conn, size):
            msg = None
            while True:
                try:
                    msg = conn.recv(1024)
                except BlockingIOError:
                    yield (EVENT_READ, conn)
                else:
                    break
            return msg

        def send(self, conn, msg):
            size = 0
            while True:
                try:
                    size = conn.send(msg)
                except BlockingIOError:
                    yield (EVENT_WRITE, conn)
                else:
                    break
            return size

        def once(self):
            self.polling()
            unfinished = []
            for t, data in self.queue:
                try:
                    data = t.send(data)
                except StopIteration:
                    continue

                if self.register(t, data):
                    unfinished.append((t, None))

            self.queue = unfinished

        def run(self):
            while self.queue or self.sel.get_map():
                self.once()

By assigning jobs into the event loop to handle connections, the programming
pattern is similar to use threads to manage I/O operations but utilizing a
user-level scheduler. Also, `PEP 380`_ enables a generator delegation, which
allows a generator can wait for other generators to finish their jobs. Obviously,
the following snippet is more intuitive and readable than using callback
functions to handle I/O operations.

.. code-block:: python

    # foo.py
    # $ python3 foo.py &
    # $ nc localhost 5566

    import socket

    from selectors import EVENT_READ, EVENT_WRITE

    from loop import Loop

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 5566))
    s.listen(10240)
    s.setblocking(False)

    loop = Loop()

    def handler(conn):
        while True:
            msg = yield from loop.recv(conn, 1024)
            if not msg:
                conn.close()
                break
            yield from loop.send(conn, msg)

    def main():
        while True:
            conn, addr = yield from loop.accept(s)
            conn.setblocking(False)
            loop.create_task((handler(conn), None))

    loop.create_task((main(), None))
    loop.run()

What is a Coroutine?
--------------------

.. code-block:: python

    import asyncio
    import inspect
    import types

    from functools import wraps
    from asyncio.futures import Future

    def coroutine(func):
        """Simple prototype of coroutine"""
        if inspect.isgeneratorfunction(func):
            return types.coroutine(func)

        @wraps(func)
        def coro(*a, **k):
            res = func(*a, **k)
            if isinstance(res, Future) or inspect.isgenerator(res):
                res = yield from res
            return res
        return types.coroutine(coro)

    @coroutine
    def foo():
        yield from asyncio.sleep(1)
        print("Hello Foo")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(loop.create_task(foo()))
    loop.close()

Reference
---------

1. `Coroutines and Tasks`_
2. `PEP 342 - Coroutines via Enhanced Generators`_
3. `PEP 380 - Syntax for Delegating to a Subgenerator`_
4. `PEP 492 - Coroutines with async and await syntax`_

.. _C10k problem: https://en.wikipedia.org/wiki/C10k_problem
.. _Valgrind: https://valgrind.org/
.. _select: https://docs.python.org/3/library/select.html
.. _selectors: https://docs.python.org/3/library/selectors.html
.. _Coroutines and Tasks: https://docs.python.org/3/library/asyncio-task.html
.. _PEP 380: https://www.python.org/dev/peps/pep-0380/
.. _PEP 342 - Coroutines via Enhanced Generators: https://www.python.org/dev/peps/pep-0342/
.. _PEP 492 - Coroutines with async and await syntax: https://www.python.org/dev/peps/pep-0492/
.. _PEP 380 - Syntax for Delegating to a Subgenerator: https://www.python.org/dev/peps/pep-0380/
