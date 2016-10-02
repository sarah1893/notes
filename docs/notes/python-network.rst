Python network cheatsheet
=========================

Simple DNS Server
------------------

.. code-block:: python

    import asyncio
    import socket
    import struct

    loop = asyncio.get_event_loop()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(False)

    host = '192.168.1.50'
    port = 3553

    sock.bind((host, port))

    def get_dns_domain(data):
        """ DSN packet struct

        typedef struct dns_header {
            uint16_t id; 
            uint8_t  rd :1;     /* recursion desired */
            uint8_t  tc :1;     /* truncated message */
            uint8_t  aa :1;     /* authoritive answer */
            uint8_t  opcode :4; /* purpose of message */
            uint8_t  qr :1;     /* response flag */
            uint8_t  rcode :4;  /* response code */
            uint8_t  unused :3; /* unused bits */
            uint8_t  ra :1;
            uint16_t qdcount;   /* number of question entries */
            uint16_t ancount;   /* number of answer entries */
            uint16_t nscount;   /* number of authority entries */
            uint16_t arcount;   /* number of resource entries */
        };

        Ref: RFC-1034, RFC-1035
        """
        # get dns header
        header = struct.unpack("2s2s2s2s2s2s", data[0:12]) 
        # get dns body
        body = data[12:]

        # parse domain
        domain = b''
        len_ = data[12] 
        ptr_ = 13
        while len_:
            domain += data[ptr_:ptr_ + len_] + b'.'
            ptr_ += len_ + 1
            len_ = data[ptr_ - 1]

        # return domain name
        return domain


    def make_response(data, domain):

        fake_map = {b'www.google.com.': '192.168.55.66'}
        ip = fake_map.get(domain, '127.0.0.1')

        # make dns resp header
        resp_id      = data[:2]
        # standard query response, no error
        resp_flags   = b'\x81\x80'
        resp_qdcount = b'\x00\x01'
        resp_ancount = b'\x00\x01'
        resp_nscount = b'\x00\x00'
        resp_qrcount = b'\x00\x00'

        # make dns query resp body
        resp_query   = data[12:]

        # make dns ans resp body
        resp_ans_name  = b'\xc0\x0c'
        resp_ans_type  = b'\x00\x01'
        resp_ans_class = b'\x00\x01'
        resp_ans_ttl   = b'\x00\x00\x01\x0a'
        resp_ans_len   = b'\x00\x04'
        resp_ans_addr  = bytes([int(_w) for _w in ip.split('.')])
        
        resp  = b''
        resp += resp_id + resp_flags + resp_qdcount + resp_ancount
        resp += resp_nscount + resp_qrcount + resp_query
        resp += resp_ans_name + resp_ans_type + resp_ans_class
        resp += resp_ans_ttl + resp_ans_len + resp_ans_addr
        return resp


    def recvfrom(loop, sock, n_bytes, fut=None, registed=False):
        fd = sock.fileno()
        if fut is None:
            fut = loop.create_future()
        if registed:
            loop.remove_reader(fd)

        try:
            data, addr = sock.recvfrom(n_bytes) 
        except (BlockingIOError, InterruptedError):
            loop.add_reader(fd, recvfrom, loop, sock,
                            n_bytes, fut, True)
        else:
            fut.set_result((data, addr))
        return fut

    def sendto(loop, sock, data, addr, fut=None, registed=False):
        fd = sock.fileno()
        if fut is None:
            fut = loop.create_future()
        if registed:
            loop.remove_writer(fd)
        if not data:
            return

        try:
            n = sock.sendto(data, addr)
        except (BlockingIOError, InterruptedError):
            loop.add_writer(fd, sendto, loop, sock,
                            data, addr, fut, True)
        else:
            fut.set_result(n)
        return fut

    async def server(loop, sock):
        while True:
            data, addr = await recvfrom(loop, sock, 1024)
            resp = make_response(data, get_dns_domain(data))
            n_bytes = await sendto(loop, sock, resp, addr)

    try:
        loop.run_until_complete(server(loop, sock))
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()

output:

.. code-block:: bash

    $ python3 dns_server.py &
    $ nslookup -port=3553 www.google.com 192.168.1.50
    Server:		192.168.1.50
    Address:	192.168.1.50#3553

    Non-authoritative answer:
    Name:	www.google.com
    Address: 192.168.55.66 
