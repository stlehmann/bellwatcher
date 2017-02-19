import socket


class Response:

    def __init__(self, f):
        self.raw = f
        self.encoding = "utf-8"
        self._cached = None

    def close(self):
        if self.raw:
            self.raw.close()
            self.raw = None
        self._cached = None

    @property
    def content(self):
        if self._cached is None:
            self._cached = self.raw.read()
            self.raw.close()
            self.raw = None
        return self._cached

    @property
    def text(self):
        return str(self.content, self.encoding)

    def json(self):
        import ujson
        return ujson.loads(self.content)


def request(method, url, data=None, json=None, headers={}, stream=None):
    try:
        proto, dummy, host, path = url.split("/", 3)
    except ValueError:
        proto, dummy, host = url.split("/", 2)
        path = ""
    if proto == "http:":
        port = 80
    else:
        raise ValueError("Unsupported protocol: " + proto)

    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)

    ai = socket.getaddrinfo(host, port)
    addr = ai[0][4]

    s = socket.socket()
    s.connect(addr)

    buf = [
        "%s /%s HTTP/1.0\r\n" % (method, path),
    ]

    if "Host" not in headers:
        buf.append("Host: %s\r\n" % host)

    # Iterate over keys to avoid tuple alloc
    for k in headers:
        buf.append(k)
        buf.append(": ")
        buf.append(headers[k])
        buf.append("\r\n")

    buf.append("\r\n")
    print(buf)

    msg = bytes('\r\n'.join(buf), 'utf-8')
    print(msg)
    s.send(msg)

    return