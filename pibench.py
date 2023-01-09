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
    processes = cpu_count() #processes = 4 (intel i3-3220)
    print ('utilizing %d CPU(s)\n' % processes) 
    pool = Pool(processes) #pool(4)
    pool.map(bench, range(processes)) # -> 0 1 2 3
    pool.close()
    pool.join() #attente de fin du pool
    end = time.time()
    duration = round(end - start,3) #calcul du temps d'exécution
    print(f"Time taken: {duration}")