#!/usr/bin/env python

import zmq

context = zmq.Context()

socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:5555")

while True:
    request = socket.recv()
    print "Server got: %s" % (request, )

    socket.send("reply to: " + request)
