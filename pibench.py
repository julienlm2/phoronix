#!/usr/bin/env python
import time
import math

start = time.time()
tab = [] 

for i in range(0,10000):
    for x in range(1,1000):
      3.141592 * 2**x
    for x in range(1,10000):
      float(x) / 3.141592
    for x in range(1,10000):
      float(3.141592) / x


end = time.time()

duration = round(end - start,3)
print(f"Time taken: {duration}")