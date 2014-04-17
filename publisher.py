#!/usr/bin/env python

import zmq
import random

context = zmq.Context()

socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:5444")

i = 0

while True:
    msg = random.choice("ABCD") + str(i)
    i += 1

    socket.send(msg)
