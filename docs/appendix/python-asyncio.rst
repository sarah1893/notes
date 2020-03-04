.. meta::
    :keywords: Python, Python3, Asyncio

=========================
Asyncio behind the Scenes
=========================

.. contents:: Table of Contents
    :backlinks: none


How does ``asyncio.wait`` work?
--------------------------------

.. code-block:: python

    import asyncio

    async def wait(fs, loop=None):
        fs = {asyncio.ensure_future(_) for _ in set(fs)}
        if loop is None:
            loop = asyncio.get_event_loop()

        waiter = loop.create_future()
        counter = len(fs)

        def _on_complete(f):
            nonlocal counter
            counter -= 1
            if counter <= 0 and not waiter.done():
                 waiter.set_result(None)

        for f in fs:
            f.add_done_callback(_on_complete)

        # wait all tasks done
        await waiter

        done, pending = set(), set()
        for f in fs:
            f.remove_done_callback(_on_complete)
            if f.done():
                done.add(f)
            else:
                pending.add(f)
        return done, pending

    async def slow_task(n):
        await asyncio.sleep(n)
        print('sleep "{}" sec'.format(n))

    loop = asyncio.get_event_loop()

    try:
        print("---> wait")
        loop.run_until_complete(
                wait([slow_task(_) for _ in range(1, 3)]))
        print("---> asyncio.wait")
        loop.run_until_complete(
                asyncio.wait([slow_task(_) for _ in range(1, 3)]))
    finally:
        loop.close()

output:

.. code-block:: bash

    ---> wait
    sleep "1" sec
    sleep "2" sec
    ---> asyncio.wait
    sleep "1" sec
    sleep "2" sec

How does ``loop.sock_*`` work?
-------------------------------

.. code-block:: python

    import asyncio
    import socket

    def sock_accept(self, sock, fut=None, registed=False):
        fd = sock.fileno()
        if fut is None:
            fut = self.create_future()
        if registed:
            self.remove_reader(fd)
        try:
            conn, addr = sock.accept()
            conn.setblocking(False)
        except (BlockingIOError, InterruptedError):
            self.add_reader(fd, self.sock_accept, sock, fut, True)
        except Exception as e:
            fut.set_exception(e)
        else:
            fut.set_result((conn, addr))
        return fut

    def sock_recv(self, sock, n, fut=None, registed=False):
        fd = sock.fileno()
        if fut is None:
            fut = self.create_future()
        if registed:
            self.remove_reader(fd)
        try:
            data = sock.recv(n)
        except (BlockingIOError, InterruptedError):
            self.add_reader(fd, self.sock_recv, sock, n, fut, True)
        except Exception as e:
            fut.set_exception(e)
        else:
            fut.set_result(data)
        return fut

    def sock_sendall(self, sock, data, fut=None, registed=False):
        fd = sock.fileno()
        if fut is None:
            fut = self.create_future()
        if registed:
            self.remove_writer(fd)
        try:
            n = sock.send(data)
        except (BlockingIOError, InterruptedError):
            n = 0
        except Exception as e:
            fut.set_exception(e)
            return
        if n == len(data):
            fut.set_result(None)
        else:
            if n:
                data = data[n:]
            self.add_writer(fd, sock, data, fut, True)
        return fut

    async def handler(loop, conn):
        while True:
            msg = await loop.sock_recv(conn, 1024)
            if msg: await loop.sock_sendall(conn, msg)
            else: break
        conn.close()

    async def server(loop):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setblocking(False)
        sock.bind(('localhost', 9527))
        sock.listen(10)

        while True:
            conn, addr = await loop.sock_accept(sock)
            loop.create_task(handler(loop, conn))

    EventLoop = asyncio.SelectorEventLoop
    EventLoop.sock_accept = sock_accept
    EventLoop.sock_recv = sock_recv
    EventLoop.sock_sendall = sock_sendall
    loop = EventLoop()

    try:
        loop.run_until_complete(server(loop))
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()

output:

.. code-block:: bash

    # console 1
    $ python3 async_sock.py &
    $ nc localhost 9527
    Hello
    Hello

    # console 2
    $ nc localhost 9527
    asyncio
    asyncio


How does ``loop.create_server`` work?
-------------------------------------

.. code-block:: python

    import asyncio
    import socket

    loop = asyncio.get_event_loop()

    async def create_server(loop, protocol_factory, host,
                            port, *args, **kwargs):
       sock = socket.socket(socket.AF_INET,
                            socket.SOCK_STREAM, 0)
       sock.setsockopt(socket.SOL_SOCKET,
                       socket.SO_REUSEADDR, 1)
       sock.setblocking(False)
       sock.bind((host, port))
       sock.listen(10)
       sockets = [sock]
       server = asyncio.base_events.Server(loop, sockets)
       loop._start_serving(protocol_factory, sock, None, server)

       return server


    class EchoProtocol(asyncio.Protocol):
        def connection_made(self, transport):
            peername = transport.get_extra_info('peername')
            print('Connection from {}'.format(peername))
            self.transport = transport

        def data_received(self, data):
            message = data.decode()
            self.transport.write(data)

    # Equal to: loop.create_server(EchoProtocol,
    #                              'localhost', 5566)
    coro = create_server(loop, EchoProtocol, 'localhost', 5566)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

output:

.. code-block:: bash

    # console1
    $ nc localhost 5566
    Hello
    Hello

    # console2
    $ nc localhost 5566
    asyncio
    asyncio
