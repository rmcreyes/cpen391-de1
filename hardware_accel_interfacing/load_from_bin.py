import numpy as np
from ctypes import *

bin_arr = np.fromfile('6_3.bin', dtype='int32')
print(bin_arr)

p = (c_int*len(bin_arr))()

for idx,elem in enumerate(bin_arr):
    p[idx] = elem.item()

x = CDLL('./x.so')
x.read.argtype = POINTER(c_int)
x.read.restype = None

x.read(p)