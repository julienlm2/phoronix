#!/usr/bin/env python

from multiprocessing import Pool
from multiprocessing import cpu_count
import time
import math
import sys

start = time.time()


if len(sys.argv) == 1  or len(sys.argv) > 2:
    print("Erreur, Le Script prend 1 parametre (nombre d'itérations)")
    exit()

def bench(x):
    iterations = int(sys.argv[1])
    for i in range(0,iterations):
        for x in range(1,1000):
            3.141592 * 2**x
        for x in range(1,10000):
            float(x) / 3.141592
        for x in range(1,10000):
            float(3.141592) / x

if __name__ == '__main__':
    processes = cpu_count()
    print ('utilizing %d cores\n' % processes)
    pool = Pool(processes)
    pool.map(bench, range(processes))
    pool.close()
    pool.join()
    end = time.time()
    duration = round(end - start,3)
    print(f"Time taken: {duration}")