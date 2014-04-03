#!/usr/bin/env python

import memcache
import collections
import sys
import os
import subprocess
import time
import random


NUTCRACKER_PORT = 11222
MEMCACHED_PORTS = (11212, 11213, 11214, 11215, 11216, 11217, 11218, 11219)
NUTCRACKER_CONF = """
alpha:
  listen: 127.0.0.1:%d
  hash: fnv1a_64
  distribution: ketama
  auto_eject_hosts: true
  server_retry_timeout: 8000
  server_failure_limit: 2
  timeout: 100
  servers:
%s

"""

N = 10000
PAGE = 10

memcacheds = {}

print "Starting memcacheds on ports: %r" % (MEMCACHED_PORTS, )

for port in MEMCACHED_PORTS:
    memcacheds[port] = subprocess.Popen(["memcached", "-p", str(port), "-m", "128"])

print "Starting nutcracker on port: %r" % (NUTCRACKER_PORT, )

with open("cracker.conf", "w") as cracker_conf:
    cracker_conf.write(NUTCRACKER_CONF % (NUTCRACKER_PORT, "\n".join("   - 127.0.0.1:%d:1" % (port, ) for port in memcacheds.keys())))

nutcracker = subprocess.Popen(["nutcracker", "-v", "0", "-c", "cracker.conf"])

# wait for memcacheds & nutcracker to come alive
time.sleep(0.1)

values = {}

random.seed()

def check_cycle():
    mismatched = 0
    missing = 0

    print "Checking items..."

    i = 0
    while i < N:
        expected = dict(("key%d" % j, values[j]) for j in xrange(i, min(i+PAGE, N)))
        memc = memcache.Client(['127.0.0.1:%d' % NUTCRACKER_PORT])
        result = memc.get_multi(expected.keys())
        for key in expected.keys():
            if key not in result:
                missing += 1
            elif result[key] != expected[key]:
                mismatched += 1
        i += PAGE

    print "Missing: %d, wrong value: %d" % (missing, mismatched)

def renew_values():
    print "Refreshing values..."
    for i in xrange(N):
        values[i] = str(random.randrange(10000000))

def refill_memcached():
    print "Refilling memcached..."
    i = 0
    memc = memcache.Client(['127.0.0.1:%d' % NUTCRACKER_PORT])
    while i < N:
        packet = {}
        for j in xrange(i, min(i+PAGE, N)):
            packet["key%d" % j] = values[j]
        memc.set_multi(packet)
        i += PAGE

    print "Item distribution:"

    for port in memcacheds.keys():
        mc = memcache.Client([('127.0.0.1:%d' % port)])
        print " - %d: %s items" % (port, mc.get_stats()[0][1]['curr_items'])
        mc.disconnect_all()

try:

    renew_values()

    for _ in xrange(2):
        refill_memcached()

        check_cycle()

        memc_to_stop = random.choice(memcacheds.keys())
        print "Stopping random memcached (%d)..." % memc_to_stop
        memcacheds[memc_to_stop].terminate()
        memcacheds[memc_to_stop].wait()
        del memcacheds[memc_to_stop]

        check_cycle()

        renew_values()

        refill_memcached()

        check_cycle()

        print "Bringing back..."
        memcacheds[memc_to_stop] = subprocess.Popen(["memcached", "-p", str(memc_to_stop), "-m", "128"])

        check_cycle()

        time.sleep(10)

        check_cycle()

finally:
    nutcracker.terminate()
    nutcracker.wait()

    for proc in memcacheds.values():
        proc.terminate()
        proc.wait()