#!/usr/bin/env python

import memcache
import collections
import sys
import subprocess
import time

PORT = 11411

# default settings
size_count = ((1, 1000), (100, 1000), (1000, 100), (10000, 100))

# parse args
argc = len(sys.argv) - 1
if argc > 0:
    if argc % 2 == 0:
        size_count = [(int(sys.argv[i * 2 + 1]), int(sys.argv[i * 2 + 2])) for i in xrange(argc // 2)]
    else:
        raise Exception("Odd number of arguments")


# start memcached with 512MB of memory, on PORT
proc = subprocess.Popen(["memcached", "-p", str(PORT), "-m", "512"])

# wait for memcached to come alive
time.sleep(0.1)


try:
    mc = memcache.Client(['127.0.0.1:%d' % PORT])

    # fill memcached
    i = 0
    for size, count in size_count:
        print "    alloc size: %6d bytes, count %6d items" % (size, count)
        for _ in xrange(count):
            mc.set("key%d" % i, "A" * size)
            i += 1

    # get slabs tats
    stats = mc.get_stats('slabs')[0][1]
    slabs = collections.defaultdict(dict)

    for key, value in stats.iteritems():
        if ":" not in key:
            continue
        slab, name = key.split(":")
        slabs[int(slab)][name] = value

    for slab in sorted(slabs.keys()):
        print "%3d: chunk size %6s bytes, used  %6s chunks, alloc memory %8d, used memory %8s bytes" % \
            (slab, slabs[slab]['chunk_size'], slabs[slab]['used_chunks'],
             int(slabs[slab]['total_pages']) * 1048576, slabs[slab]['mem_requested'])
finally:
    proc.terminate()
    proc.wait()
