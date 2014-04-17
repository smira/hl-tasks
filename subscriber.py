#!/usr/bin/env python

import zmq
import sys

context = zmq.Context()

socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5444")

if len(sys.argv) > 1:
    socket.setsockopt(zmq.SUBSCRIBE, sys.argv[1])
else:
    socket.setsockopt(zmq.SUBSCRIBE, "")

while True:
    msg = socket.recv()
    print msg
