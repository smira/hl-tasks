#!/usr/bin/env python

import random
import subprocess
import time

from twisted.web import server, resource
from twisted.internet import reactor, protocol, defer
from twisted.protocols.memcache import MemCacheProtocol


class Server(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        d = self.process_request(request)

        def render_ok(_):
            request.finish()

        def render_err(fail):
            request.write(str(fail))
            request.finish()

        d.addCallback(render_ok)
        d.addErrback(render_err)

        request.setHeader('Content-Type', 'text/text')
        return server.NOT_DONE_YET

    def process_request(self, request):
        counters = random.sample(xrange(100000), 100)

        def gotProtocol(memc):
            def process(counter):
                key = "counter_%d" % counter

                def add():
                    def gotResult(res):
                        if res is None:
                            return incr()

                        return 1
                    return memc.add(key, "1").addCallback(gotResult)

                def incr():
                    def gotResult(res):
                        if res == 0:
                            return add()
                        return res
                    return memc.increment(key).addCallback(gotResult)

                def done(value):
                    request.write("%s -> %d\n" % (key, value))

                return incr().addCallback(done)

            i = iter(counters)

            def iterator():
                try:
                    counter = i.next()
                except StopIteration:
                    memc.transport.loseConnection()
                    return

                return process(counter).addCallback(lambda _: iterator())

            return iterator()

        return protocol.ClientCreator(reactor, MemCacheProtocol).connectTCP("127.0.0.1", 11313) \
            .addCallback(gotProtocol)


if __name__ == "__main__":
    # start memcached with 512MB of memory, on PORT
    proc = subprocess.Popen(["memcached", "-p", str(11313), "-m", "512"])

    # wait for memcached to come alive
    time.sleep(0.1)

    PORT = 8003

    try:
        serv = Server()
        site = server.Site(serv)

        def gotProtocol(protocol):
            serv.memc = protocol

        reactor.listenTCP(PORT, site)
        print "Noblocking HTTP server started on localhost:%d" % (PORT, )
        reactor.run()
    finally:
        proc.terminate()
        proc.wait()
