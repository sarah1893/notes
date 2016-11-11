========================
Python socket cheatsheet
========================

Get Hostname
------------

.. code-block:: python

    >>> import socket
    >>> socket.gethostname()
    'MacBookPro-4380.local'
    >>> hostname = socket.gethostname()
    >>> socket.gethostbyname(hostname)
    '172.20.10.4'
    >>> socket.gethostbyname('localhost')
    '127.0.0.1'

Transform Host & Network Endian
--------------------------------

.. code-block:: python

    # little-endian machine
    >>> import socket
    >>> a = 1 # host endian
    >>> socket.htons(a) # network endian
    256
    >>> socket.htonl(a) # network endian
    16777216
    >>> socket.ntohs(256) # host endian
    1
    >>> socket.ntohl(16777216) # host endian
    1

    # big-endian machine
    >>> import socket
    >>> a = 1 # host endian
    >>> socket.htons(a) # network endian
    1
    >>> socket.htonl(a) # network endian
    1L
    >>> socket.ntohs(1) # host endian
    1
    >>> socket.ntohl(1) # host endian
    1L


IP dotted-quad string & byte format convert
-------------------------------------------

.. code-block:: python

    >>> import socket
    >>> addr = socket.inet_aton('127.0.0.1')
    >>> addr
    '\x7f\x00\x00\x01'
    >>> socket.inet_ntoa(addr)
    '127.0.0.1'

Mac address & byte format convert
---------------------------------

.. code-block:: python

    >>> mac = '00:11:32:3c:c3:0b'
    >>> byte = binascii.unhexlify(mac.replace(':',''))
    >>> byte
    '\x00\x112<\xc3\x0b'
    >>> binascii.hexlify(byte)
    '0011323cc30b'

Simple TCP Echo Server
----------------------

.. code-block:: python

    import socket

    class Server(object):
        def __init__(self,host,port):
            self._host = host
            self._port = port
        def __enter__(self):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            sock.bind((self._host,self._port))
            sock.listen(10)
            self._sock = sock
            return self._sock 
        def __exit__(self,*exc_info):
            if exc_info[0]:
                import traceback
                traceback.print_exception(*exc_info)
            self._sock.close()
          
    if __name__ == '__main__':
        host = 'localhost'
        port = 5566
        with Server(host,5566) as s:
            while True:
                conn, addr = s.accept()
                msg = conn.recv(1024)
                conn.send(msg)
                conn.close()

output:

.. code-block:: console

    $ nc localhost 5566
    Hello World 
    Hello World

Simple TCP Echo Server Via SocketServer
---------------------------------------

.. code-block:: python

    >>> import SocketServer
    >>> bh = SocketServer.BaseRequestHandler
    >>> class handler(bh):
    ...   def handle(self):
    ...     data = self.request.recv(1024)
    ...     print self.client_address
    ...     self.request.sendall(data)
    ... 
    >>> host = ('localhost',5566)
    >>> s = SocketServer.TCPServer(
    ...   host, handler)
    >>> s.serve_forever()

output:

.. code-block:: console

    $ nc -u localhost 5566
    Hello World
    Hello World


Simple SSL TCP Echo Server
---------------------------

.. code-block:: python

    import socket
    import ssl

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 5566))
    sock.listen(10)

    sslctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    sslctx.load_cert_chain(certfile='./root-ca.crt',
                           keyfile='./root-ca.key')

    try:
        while True:
            conn, addr = sock.accept()
            sslconn = sslctx.wrap_socket(conn, server_side=True)
            msg = sslconn.recv(1024)
            if msg:
                sslconn.send(msg)
            sslconn.close()
    finally:
        sock.close()

output:

.. code-block:: bash

    # console 1
    $ openssl genrsa -out root-ca.key 2048
    $ openssl req -x509 -new -nodes -key root-ca.key -days 365 -out root-ca.crt
    $ python3 ssl_tcp_server.py

    # console 2
    $ openssl s_client -connect localhost:5566
    ...
    Hello SSL
    Hello SSL
    read:errno=0


Simple UDP Echo Server
----------------------

.. code-block:: python

    import socket

    class UDPServer(object):
        def __init__(self,host,port):
            self._host = host
            self._port = port

        def __enter__(self):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((self._host,self._port))
            self._sock = sock
            return sock
       def __exit__(self,*exc_info):
            if exc_info[0]:
                import traceback
                traceback.print_exception(*exc_info)
            self._sock.close()

    if __name__ == '__main__':
        host = 'localhost'
        port = 5566
        with UDPServer(host,port) as s:
            while True:
                msg, addr = s.recvfrom(1024)
                s.sendto(msg, addr)

output:

.. code-block:: console 

    $ nc -u localhost 5566
    Hello World
    Hello World


Simple UDP Echo Server Via SocketServer
---------------------------------------

.. code-block:: python

    >>> import SocketServer
    >>> bh = SocketServer.BaseRequestHandler
    >>> class handler(bh):
    ...   def handle(self):
    ...     m,s = self.request
    ...     s.sendto(m,self.client_address)
    ...     print self.client_address
    ... 
    >>> host = ('localhost',5566)
    >>> s = SocketServer.UDPServer(
    ...   host, handler)
    >>> s.serve_forever()

output:

.. code-block:: console

    $ nc -u localhost 5566
    Hello World
    Hello World


Simple UDP client - Sender
--------------------------

.. code-block:: python

    >>> import socket
    >>> import time
    >>> sock = socket.socket(
    ...   socket.AF_INET,
    ...   socket.SOCK_DGRAM)
    >>> host = ('localhost',5566)
    >>> while True:
    ...   sock.sendto("Hello\n",host)
    ...   time.sleep(5)
    ...

output:

.. code-block:: console

    $ nc -lu localhost 5566
    Hello
    Hello

Broadcast UDP Packets
---------------------

.. code-block:: python

    >>> import socket
    >>> import time
    >>> sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    >>> sock.bind(('',0))
    >>> sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
    >>> while True:
    ...   m = '{0}\n'.format(time.time())
    ...   sock.sendto(m,('<broadcast>',5566))
    ...   time.sleep(5)
    ...

output:

.. code-block:: console

    $ nc -k -w 1 -ul 5566
    1431473025.72

Simple UNIX Domain Socket
-------------------------

.. code-block:: python

    import socket
    import contextlib
    import os

    @contextlib.contextmanager
    def DomainServer(addr):
        try:
            if os.path.exists(addr):
                os.unlink(addr)
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.bind(addr)
            sock.listen(10)
            yield sock
        finally:
            sock.close()
            if os.path.exists(addr):
                os.unlink(addr)

    addr = "./domain.sock"
    with DomainServer(addr) as sock:
        while True:
            conn, _ = sock.accept()
            msg = conn.recv(1024)
            conn.send(msg)
            conn.close()

output:

.. code-block:: console

    $ nc -U ./domain.sock
    Hello
    Hello


Simple duplex processes communication
---------------------------------------

.. code-block:: python

    import os
    import socket

    child, parent = socket.socketpair()
    pid = os.fork()
    try:

        if pid == 0:
            print('chlid pid: {}'.format(os.getpid()))

            child.send(b'Hello Parent')
            msg = child.recv(1024)
            print('p[{}] ---> c[{}]: {}'.format(
                os.getppid(), os.getpid(), msg))
        else:
            print('parent pid: {}'.format(os.getpid()))

            # simple echo server (parent)
            msg = parent.recv(1024)
            print('c[{}] ---> p[{}]: {}'.format(
                    pid, os.getpid(), msg))
            parent.send(msg)

    except KeyboardInterrupt:
        pass
    finally:
        child.close()
        parent.close()

output:

.. code-block:: bash

    $ python3 socketpair_demo.py
    parent pid: 9497
    chlid pid: 9498
    c[9498] ---> p[9497]: b'Hello Parent'
    p[9497] ---> c[9498]: b'Hello Parent'


Simple Asynchronous TCP Server - Thread
---------------------------------------

.. code-block:: python

    >>> from threading import Thread
    >>> import socket
    >>> def work(conn):
    ...   while True:
    ...     msg = conn.recv(1024)
    ...     conn.send(msg)
    ...
    >>> sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    >>> sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    >>> sock.bind(('localhost',5566))
    >>> sock.listen(5)
    >>> while True:
    ...   conn,addr = sock.accept()
    ...   t=Thread(target=work,args=(conn,))
    ...   t.daemon=True
    ...   t.start()
    ...

output: (bash 1)

.. code-block:: console

    $ nc localhost 5566
    Hello
    Hello

output: (bash 2)

.. code-block:: console

    $ nc localhost 5566
    Ker Ker
    Ker Ker

Simple Asynchronous TCP Server - select
---------------------------------------

.. code-block:: python

    from select import select
    import socket

    host = ('localhost',5566)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    sock.bind(host)
    sock.listen(5)
    rl = [sock]
    wl = []
    ml = {}
    try:
        while True:
            r, w, _ = select(rl,wl,[])
            # process ready to ready
            for _ in r:
                if _ == sock:
                    conn, addr = sock.accept()
                    rl.append(conn)
                else:
                    msg = _.recv(1024)
                    ml[_.fileno()] = msg
                    wl.append(_) 
            # process ready to write
            for _ in w:
                msg = ml[_.fileno()] 
                _.send(msg)
                wl.remove(_)
                del ml[_.fileno()]
    except:
        sock.close()

output: (bash 1)

.. code-block:: console

    $ nc localhost 5566
    Hello
    Hello

output: (bash 2)

.. code-block:: console

    $ nc localhost 5566
    Ker Ker
    Ker Ker

High-Level API - selectors
--------------------------

.. code-block:: python

    # Pyton3.4+ only
    # Reference: selectors 
    import selectors
    import socket
    import contextlib

    @contextlib.contextmanager
    def Server(host,port):
       try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host,port))
            s.listen(10)
            sel = selectors.DefaultSelector()
            yield s, sel
        except socket.error:
            print("Get socket error")
            raise
        finally:
            if s:
                s.close()

    def read_handler(conn, sel):
        msg = conn.recv(1024) 
        if msg:
            conn.send(msg)
        else:
            sel.unregister(conn)
            conn.close()

    def accept_handler(s, sel):
        conn, _ = s.accept()
        sel.register(conn, selectors.EVENT_READ, read_handler)

    host = 'localhost'
    port = 5566
    with Server(host, port) as (s,sel):
        sel.register(s, selectors.EVENT_READ, accept_handler)
        while True:
            events = sel.select()
            for sel_key, m in events:
                handler = sel_key.data
                handler(sel_key.fileobj, sel)

output: (bash 1)

.. code-block:: console

    $ nc localhost 5566
    Hello 
    Hello

output: (bash 1)

.. code-block:: console

    $ nc localhost 5566
    Hi
    Hi

"socketpair" - Similar to PIPE
------------------------------

.. code-block:: python

    import socket
    import os
    import time

    c_s, p_s = socket.socketpair()
    try:
        pid = os.fork()
    except OSError:
        print "Fork Error"
        raise

    if pid:
        # parent process
        c_s.close()
        while True:
            p_s.sendall("Hi! Child!")
            msg = p_s.recv(1024)
            print msg
            time.sleep(3)
        os.wait()
    else:
        # child process
        p_s.close()
        while True:
            msg = c_s.recv(1024)
            print msg
            c_s.sendall("Hi! Parent!")

output:

.. code-block:: console

    $ python ex.py
    Hi! Child!
    Hi! Parent!
    Hi! Child!
    Hi! Parent!
    ...

Sniffer IP packets
------------------

.. code-block:: python

    from ctypes import * 
    import socket
    import struct

    # ref: IP protocol numbers
    PROTO_MAP = {
            1 : "ICMP",
            2 : "IGMP",
            6 : "TCP",
            17: "UDP",
            27: "RDP"}

    class IP(Structure):
        ''' IP header Structure

        In linux api, it define as below:

        strcut ip {
            u_char         ip_hl:4; /* header_len */
            u_char         ip_v:4;  /* version */
            u_char         ip_tos;  /* type of service */
            short          ip_len;  /* total len */
            u_short        ip_id;   /* identification */
            short          ip_off;  /* offset field */
            u_char         ip_ttl;  /* time to live */
            u_char         ip_p;    /* protocol */
            u_short        ip_sum;  /* checksum */
            struct in_addr ip_src;  /* source */
            struct in_addr ip_dst;  /* destination */
        };
        '''
        _fields_ = [("ip_hl" , c_ubyte, 4), # 4 bit
                    ("ip_v"  , c_ubyte, 4), # 1 byte
                    ("ip_tos", c_uint8),    # 2 byte
                    ("ip_len", c_uint16),   # 4 byte
                    ("ip_id" , c_uint16),   # 6 byte
                    ("ip_off", c_uint16),   # 8 byte
                    ("ip_ttl", c_uint8),    # 9 byte
                    ("ip_p"  , c_uint8),    # 10 byte
                    ("ip_sum", c_uint16),   # 12 byte
                    ("ip_src", c_uint32),   # 16 byte
                    ("ip_dst", c_uint32)]   # 20 byte

        def __new__(cls, buf=None):
            return cls.from_buffer_copy(buf)
        def __init__(self, buf=None):
            src = struct.pack("<L", self.ip_src)
            self.src = socket.inet_ntoa(src)
            dst = struct.pack("<L", self.ip_dst)
            self.dst = socket.inet_ntoa(dst)
            try:
                self.proto = PROTO_MAP[self.ip_p]
            except KeyError:
                print "{} Not in map".format(self.ip_p)
                raise

    host = '0.0.0.0'
    s = socket.socket(socket.AF_INET,
                      socket.SOCK_RAW, 
                      socket.IPPROTO_ICMP)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    s.bind((host, 0))

    print "Sniffer start..."
    try:
        while True:
            buf = s.recvfrom(65535)[0]
            ip_header = IP(buf[:20])
            print '{0}: {1} -> {2}'.format(ip_header.proto,
                                           ip_header.src,
                                           ip_header.dst)
    except KeyboardInterrupt:
        s.close()

output: (bash 1)

.. code-block:: console

    python sniffer.py
    Sniffer start...
    ICMP: 127.0.0.1 -> 127.0.0.1
    ICMP: 127.0.0.1 -> 127.0.0.1
    ICMP: 127.0.0.1 -> 127.0.0.1

output: (bash 2)

.. code-block:: console

    $ ping -c 3 localhost
    PING localhost (127.0.0.1): 56 data bytes
    64 bytes from 127.0.0.1: icmp_seq=0 ttl=64 time=0.063 ms
    64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.087 ms
    64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.159 ms

    --- localhost ping statistics ---
    3 packets transmitted, 3 packets received, 0.0% packet loss
    round-trip min/avg/max/stddev = 0.063/0.103/0.159/0.041 ms


Sniffer ARP packet
------------------

.. code-block:: python

    """
    Ehternet Packet Header 

    struct ethhdr {
        unsigned char h_dest[ETH_ALEN];   /* destination eth addr */
        unsigned char h_source[ETH_ALEN]; /* source ether addr    */
        __be16        h_proto;            /* packet type ID field */
    } __attribute__((packed));

    ARP Packet Header

    struct arphdr {
        uint16_t htype;    /* Hardware Type           */
        uint16_t ptype;    /* Protocol Type           */
        u_char   hlen;     /* Hardware Address Length */
        u_char   plen;     /* Protocol Address Length */
        uint16_t opcode;   /* Operation Code          */
        u_char   sha[6];   /* Sender hardware address */
        u_char   spa[4];   /* Sender IP address       */
        u_char   tha[6];   /* Target hardware address */
        u_char   tpa[4];   /* Target IP address       */
    };
    """

    import socket
    import struct
    import binascii

    rawSocket = socket.socket(socket.AF_PACKET,
                              socket.SOCK_RAW,
                              socket.htons(0x0003))

    while True:

        packet = rawSocket.recvfrom(2048)
        ethhdr = packet[0][0:14]
        eth = struct.unpack("!6s6s2s", ethhdr)

        arphdr = packet[0][14:42]
        arp = struct.unpack("2s2s1s1s2s6s4s6s4s", arphdr)
        # skip non-ARP packets
        ethtype = eth[2]
        if ethtype != '\x08\x06': continue

        print "---------------- ETHERNET_FRAME ----------------"
        print "Dest MAC:        ", binascii.hexlify(eth[0])
        print "Source MAC:      ", binascii.hexlify(eth[1])
        print "Type:            ", binascii.hexlify(ethtype)
        print "----------------- ARP_HEADER -------------------"
        print "Hardware type:   ", binascii.hexlify(arp[0])
        print "Protocol type:   ", binascii.hexlify(arp[1])
        print "Hardware size:   ", binascii.hexlify(arp[2])
        print "Protocol size:   ", binascii.hexlify(arp[3])
        print "Opcode:          ", binascii.hexlify(arp[4])
        print "Source MAC:      ", binascii.hexlify(arp[5])
        print "Source IP:       ", socket.inet_ntoa(arp[6])
        print "Dest MAC:        ", binascii.hexlify(arp[7])
        print "Dest IP:         ", socket.inet_ntoa(arp[8])
        print "------------------------------------------------\n"

output:

.. code-block:: console

    $ python arp.py
    ---------------- ETHERNET_FRAME ----------------
    Dest MAC:         ffffffffffff
    Source MAC:       f0257252f5ca
    Type:             0806
    ----------------- ARP_HEADER -------------------
    Hardware type:    0001
    Protocol type:    0800
    Hardware size:    06
    Protocol size:    04
    Opcode:           0001
    Source MAC:       f0257252f5ca
    Source IP:        140.112.91.254
    Dest MAC:         000000000000
    Dest IP:          140.112.91.20
    ------------------------------------------------
