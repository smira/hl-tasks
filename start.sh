#!/bin/sh

start-stop-daemon --background --exec /home/hl-tasks/fork.py  -S
start-stop-daemon --background --exec /home/hl-tasks/async.py  -S
start-stop-daemon --background --exec /home/hl-tasks/thread.py  -S

/bin/bash