#!/usr/bin/env python
import time
import math
import sys

start = time.time()
tab = [] 
iterations = int(sys.argv[1])
for i in range(0,iterations):
    for x in range(1,1000):
      3.141592 * 2**x
    for x in range(1,10000):
      float(x) / 3.141592
    for x in range(1,10000):
      float(3.141592) / x

end = time.time()

duration = round(end - start,3)
print(f"Time taken: {duration}")
