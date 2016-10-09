==============================
Python cryptography cheatsheet
==============================

simple https server
---------------------

.. code-block:: python

    # python2

    >>> import BaseHTTPServer, SimpleHTTPServer
    >>> import ssl
    >>> host, port = 'localhost', 5566
    >>> handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    >>> httpd = BaseHTTPServer.HTTPServer((host, port), handler)
    >>> httpd.socket = ssl.wrap_socket(httpd.socket,
    ...                                certfile='./cert.crt',
    ...                                keyfile='./cert.key',
    ...                                server_side=True)
    >>> httpd.serve_forever()

    # python3

    >>> from http import server
    >>> handler = server.SimpleHTTPRequestHandler
    >>> import ssl
    >>> host, port = 'localhost', 5566
    >>> httpd = server.HTTPServer((host, port), handler)
    >>> httpd.socket = ssl.wrap_socket(httpd.socket,
    ...                                certfile='./cert.crt',
    ...                                keyfile='./cert.key',
    ...                                server_side=True)
    ...
    >>> httpd.serve_forever()
