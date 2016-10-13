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


check certificate information
-------------------------------

.. code-block:: python

    from cryptography import x509
    from cryptography.hazmat.backends import default_backend

    backend = default_backend()
    with open('./cert.crt', 'rb') as f:
        crt_data = f.read()
        cert = x509.load_pem_x509_certificate(crt_data, backend)

    class Certificate:

        _fields = ['country_name',
                   'state_or_province_name',
                   'locality_name',
                   'organization_name',
                   'organizational_unit_name',
                   'common_name',
                   'email_address']

        def __init__(self, cert):
            assert isinstance(cert, x509.Certificate)
            self._cert = cert
            for attr in self._fields:
                oid = getattr(x509, 'OID_' + attr.upper())
                subject = cert.subject
                info = subject.get_attributes_for_oid(oid)
                setattr(self, attr, info)


    cert = Certificate(cert)
    for attr in cert._fields:
        for info in getattr(cert, attr):
            print("{}: {}".format(info._oid._name, info._value))

output:

.. code-block:: bash

    $ genrsa -out cert.key
    Generating RSA private key, 1024 bit long modulus
    ..........++++++
    ...++++++
    e is 65537 (0x10001)
    $ openssl req -x509 -new -nodes \
    >       -key cert.key -days 365 \
    >       -out cert.crt
    You are about to be asked to enter information that will be incorporated
    into your certificate request.
    What you are about to enter is what is called a Distinguished Name or a DN.
    There are quite a few fields but you can leave some blank
    For some fields there will be a default value,
    If you enter '.', the field will be left blank.
    -----
    Country Name (2 letter code) [AU]:TW
    State or Province Name (full name) [Some-State]:Taiwan
    Locality Name (eg, city) []:Taipei
    Organization Name (eg, company) [Internet Widgits Pty Ltd]:personal
    Organizational Unit Name (eg, section) []:perfonal
    Common Name (e.g. server FQDN or YOUR name) []:localhost
    Email Address []:test@example.com
    $ python3 cert.py
    countryName: TW
    stateOrProvinceName: Taiwan
    localityName: Taipei
    organizationName: personal
    organizationalUnitName: perfonal
    commonName: localhost
    emailAddress: test@example.com


generate RSA keyfile without passphrase
-----------------------------------------

.. code-block:: python

    # $ openssl genrsa cert.key 2048

    >>> from cryptography.hazmat.backends import default_backend
    >>> from cryptography.hazmat.primitives import serialization
    >>> from cryptography.hazmat.primitives.asymmetric import rsa
    >>> key = rsa.generate_private_key(
    ... public_exponent=65537,
    ... key_size=2048,
    ... backend=default_backend())
    ...
    >>> with open('cert.key', 'wb') as f:
    ...     f.write(key.private_bytes(
    ...     encoding=serialization.Encoding.PEM,
    ...     format=serialization.PrivateFormat.TraditionalOpenSSL,
    ...     encryption_algorithm=serialization.NoEncryption()))
