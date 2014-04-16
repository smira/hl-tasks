#!/usr/bin/env python

import zmq

context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")

print "Saying hello!"
socket.send("hello!")

message = socket.recv()
print "Got: %s" % (message, )
