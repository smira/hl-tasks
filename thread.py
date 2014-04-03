#!/usr/bin/env python

import memcache
import random
import subprocess
import time
import SocketServer
import BaseHTTPServer


class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def log_request(*args):
        pass

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/text")
        self.end_headers()

        memc = memcache.Client(['127.0.0.1:11312'])

        counters = random.sample(xrange(100000), 100)

        for counter in counters:
            key = "counter_%d" % counter

            while True:
                result = memc.incr(key)
                if result is None:
                    r = memc.add(key, "1")
                    if r == 1:
                        result = 1
                        break
                else:
                    break

            self.wfile.write("%s -> %d\n" % (key, result))


class ThreadingHTTPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


if __name__ == "__main__":
    # start memcached with 512MB of memory, on PORT
    proc = subprocess.Popen(["memcached", "-p", str(11312), "-m", "512"])

    # wait for memcached to come alive
    time.sleep(0.1)

    try:
        HOST, PORT = "localhost", 8001

        server = ThreadingHTTPServer((HOST, PORT), RequestHandler)

        print "Threading HTTP server started on %s:%d" % (HOST, PORT)

        server.serve_forever()

        try:
            while True:
                pass
        finally:
            server.shutdown()
    finally:
        proc.terminate()
        proc.wait()
