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


simple RSA encrypt via pem file
--------------------------------

.. code-block:: python

    from __future__ import print_function, unicode_literals

    import base64
    import sys

    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_v1_5

    key_text = sys.stdin.read()

    # import key via rsa module
    pubkey = RSA.importKey(key_text)

    # create a cipher via PKCS1.5
    cipher = PKCS1_v1_5.new(pubkey)

    # encrypt
    cipher_text = cipher.encrypt(b"Hello RSA!")

    # do base64 encode
    cipher_text = base64.b64encode(cipher_text)
    print(cipher_text.decode('utf-8'))

output:

.. code-block:: bash

    $ openssl genrsa -out private.key 2048
    $ openssl rsa -in private.key -pubout -out public.key
    $ cat public.key                                |\
    > python3 rsa.py                                |\
    > openssl base64 -d -A                          |\
    > openssl rsautl -decrypt -inkey private.key
    Hello RSA!


simple RSA encrypt via RSA module
----------------------------------

.. code-block:: python

    from __future__ import print_function, unicode_literals

    import base64
    import sys

    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_v1_5
    from Crypto.PublicKey.RSA import construct

    # prepare public key
    e = int('10001', 16)
    n = int(sys.stdin.read(), 16)
    pubkey = construct((n, e))

    # create a cipher via PKCS1.5
    cipher = PKCS1_v1_5.new(pubkey)

    # encrypt
    cipher_text = cipher.encrypt(b"Hello RSA!")

    # do base64 encode
    cipher_text = base64.b64encode(cipher_text)
    print(cipher_text.decode('utf-8'))

output:

.. code-block:: bash

    $ openssl genrsa -out private.key 2048
    $ openssl rsa -in private.key -pubout -out public.key
    $ # check (n, e)
    $ openssl rsa -pubin -inform PEM -text -noout < public.key
    Public-Key: (2048 bit)
    Modulus:
        00:93:d5:58:0c:18:cf:91:f0:74:af:1b:40:09:73:
        0c:d8:13:23:6c:44:60:0d:83:71:e6:f9:61:85:e5:
        b2:d0:8a:73:5c:02:02:51:9a:4f:a7:ab:05:d5:74:
        ff:4d:88:3d:e2:91:b8:b0:9f:7e:a9:a3:b2:3c:99:
        1c:9a:42:4d:ac:2f:6a:e7:eb:0f:a7:e0:a5:81:e5:
        98:49:49:d5:15:3d:53:42:12:08:db:b0:e7:66:2d:
        71:5b:ea:55:4e:2d:9b:40:79:f8:7d:6e:5d:f4:a7:
        d8:13:cb:13:91:c9:ac:5b:55:62:70:44:25:50:ca:
        94:de:78:5d:97:e8:a9:33:66:4f:90:10:00:62:21:
        b6:60:52:65:76:bd:a3:3b:cf:2a:db:3f:66:5f:0d:
        a3:35:ff:29:34:26:6d:63:a2:a6:77:96:5a:84:c7:
        6a:0c:4f:48:52:70:11:8f:85:11:a0:78:f8:60:4b:
        5d:d8:4b:b2:64:e5:ec:99:72:c5:a8:1b:ab:5c:09:
        e1:80:70:91:06:22:ba:97:33:56:0b:65:d8:f3:35:
        66:f8:f9:ea:b9:84:64:8e:3c:14:f7:3d:1f:2c:67:
        ce:64:cf:f9:c5:16:6b:03:a1:7a:c7:fa:4c:38:56:
        ee:e0:4d:5f:ec:46:7e:1f:08:7c:e6:45:a1:fc:17:
        1f:91
    Exponent: 65537 (0x10001)
    $ openssl rsa -pubin -in public.key -modulus -noout |\
    > cut -d'=' -f 2                                    |\
    > python3 rsa.py                                    |\
    > openssl base64 -d -A                              |\
    > openssl rsautl -decrypt -inkey private.key
    Hello RSA!


HMAC - check integrity of a message
-------------------------------------

.. code-block:: python

    >>> import socket
    >>> import hmac
    >>> import hashlib
    >>> secret_key = b"Alice & Bob secret key"
    >>> def verify(digest, msg):
    ...     h = hmac.new(secret_key, msg, hashlib.sha256)
    ...     if h.digest() != digest:
    ...         raise ValueError("Check integrity fail")
    ...
    >>> alice_msg = b"Hello Bob"
    >>> h = hmac.new(secret_key, alice_msg, hashlib.sha256)
    >>> alice_digest = h.digest()
    >>> alice, bob = socket.socketpair()
    >>> _ = alice.send(alice_msg)    # Alice send msg to Bob
    >>> msg = bob.recv(1024)         # Bob recv msg from Alice
    >>> _ = alice.send(alice_digest) # Alice send digest to Bob
    >>> digest = bob.recv(1024)      # Bob recv digest from Alice
    >>> verify(digest, msg)          # Bob check msg integrity
    >>> # if message be modified by someone, check integrity fail
    >>> verify(digest, b"Hello Attack")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 4, in verify
    ValueError: Check integrity fail
    Check integrity fail

Using DSA to proof of identity
--------------------------------

.. code-block:: python

    import socket

    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import dsa

    alice, bob = socket.socketpair()

    def gen_dsa_key():
        private_key = dsa.generate_private_key(
            key_size=2048, backend=default_backend())
        return private_key, private_key.public_key()


    def sign_data(data, private_key):
        signature = private_key.sign(data, hashes.SHA256())
        return signature


    def verify_data(data, signature, public_key):
        try:
            public_key.verify(signature, data, hashes.SHA256())
        except InvalidSignature:
            print("recv msg: {} not trust!".format(data))
        else:
            print("check msg: {} success!".format(data))


    # generate alice private & public key
    alice_private_key, alice_public_key = gen_dsa_key()

    # alice send message to bob, then bob recv
    alice_msg = b"Hello Bob"
    b = alice.send(alice_msg)
    bob_recv_msg = bob.recv(1024)

    # alice send signature to bob, then bob recv
    signature = sign_data(alice_msg, alice_private_key)
    b = alice.send(signature)
    bob_recv_signature = bob.recv(1024)

    # bob check message recv from alice
    verify_data(bob_recv_msg, bob_recv_signature, alice_public_key)

    # attacker modify the msg will make the msg check fail
    verify_data(b"I'm attacker!", bob_recv_signature, alice_public_key)

output:

.. code-block:: bash

    $ python3 test_dsa.py
    check msg: b'Hello Bob' success!
    recv msg: b"I'm attacker!" not trust!


Simple Diffie-Hellman key exchange
------------------------------------

.. code-block:: python

    """
    p (public know)
    n (public know)
    Alice                               Bob

    alice_y = 23                        bob_y = 16
    alice_x = (n ** alice_y) % p  --->
                                  <---  bob_x = (n ** bob_y) % p
    k = (bob_x ** alice_y) %p           k = (alice_x ** bob_y) % p
    """

    >>> import socket
    >>> alice, bob = socket.socketpair()
    >>> p = 353       # public know
    >>> n = 3         # public know
    >>> alice_y = 23  # only alice know
    >>> bob_y = 16    # only bob know
    >>> alice_x = (n ** alice_y) % p
    >>> num_bytes = alice.send(alice_x.to_bytes(4, 'big'))
    >>> msg = bob.recv(1024)
    >>> bob_recv_x = int.from_bytes(msg, 'big')
    >>> bob_x = (n ** bob_y) % p
    >>> num_bytes = bob.send(bob_x.to_bytes(4, 'big'))
    >>> msg = alice.recv(1024)
    >>> alice_recv_x = int.from_bytes(msg, 'big')
    >>> alice_key = (alice_recv_x ** alice_y) % p
    >>> bob_key = (bob_recv_x ** bob_y) % p
    >>> alice_key
    136
    >>> bob_key
    136


AES CBC mode encrypt and decrypt
----------------------------------

.. code-block:: python

    import os
    from cryptography.hazmat.primitives import padding
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.ciphers import (
            Cipher,
            algorithms,
            modes)

    backend = default_backend()
    key = os.urandom(32)
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key),
                    modes.CBC(iv),
                    backend=backend)

    # PS. CBC mode need padding

    def encrypt(p_text, cipher):
        # add padding to plain text
        padder = padding.PKCS7(128).padder() # 128 bit
        text = padder.update(p_text) + padder.finalize()

        # encrypt plain text
        encryptor = cipher.encryptor()
        c_text = encryptor.update(text) + encryptor.finalize()
        return c_text

    def decrypt(c_text, cipher):
        # decrypt plain text with padding
        decryptor = cipher.decryptor()
        text = decryptor.update(c_text) + decryptor.finalize()

        # remove padding
        unpadder = padding.PKCS7(128).unpadder() # 128 bit
        p_text = unpadder.update(text) + unpadder.finalize()
        return p_text

    text = b"Hello Encrypt"
    c_text = encrypt(text, cipher)
    print(c_text)
    p_text = decrypt(c_text, cipher)
    print(p_text)

output:

.. code-block:: bash

    $ python3 aes_cbc.py
    b',n\xcb\xd3\x95\xfayvX\xa6q\\\x19\xdb\x12C'
    b'Hello Encrypt'


AES CTR mode encrypt and decrypt
---------------------------------

.. code-block:: python

    >>> import os
    >>> from cryptography.hazmat.backends import default_backend
    >>> from cryptography.hazmat.primitives.ciphers import (
    ... Cipher,
    ... algorithms,
    ... modes)
    >>> backend = default_backend()
    >>> key = os.urandom(32)
    >>> nonce = os.urandom(16)
    >>> # CTR mode does not require padding
    >>> cipher = Cipher(algorithms.AES(key),
    ...                 modes.CTR(nonce),
    ...                 backend=backend)
    >>> encryptor = cipher.encryptor()
    >>> p_text = b"Hello Encrypt"
    >>> ct = encryptor.update(p_text) + encryptor.finalize()
    >>> ct
    b'o\xb3;\x079\xde\x86@\xec^o\x1f\x9f'
    >>> decryptor = cipher.decryptor()
    >>> pt = decryptor.update(ct) + decryptor.finalize()
    >>> pt
    b'Hello Encrypt'

Require padding or not
~~~~~~~~~~~~~~~~~~~~~~~

================================   ===================
   mode                             require padding
================================   ===================
  CBC(initialization_vector)            YES
  CTR(nonce)                            NO
  OFB(initialization_vector)            NO
  CFB(initialization_vector)            NO
  CFB8(initialization_vector)           NO
  GCM(initialization_vector)            NO
================================   ===================
