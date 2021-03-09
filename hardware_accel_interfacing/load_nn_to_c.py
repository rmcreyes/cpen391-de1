import numpy as np
from ctypes import *

in_size = 784
l1_size = 1000
l2_size = 750
l3_size = 36

bin_arr = np.fromfile('generated_nn.bin', dtype='int32')

num_elems = len(bin_arr)

p = (c_int*num_elems)()

for idx,elem in enumerate(bin_arr):
    p[idx] = elem.item()

x = CDLL('./x.so')
x.read.argtype = POINTER(c_int),c_int,c_int,c_int,c_int
x.read.restype = None

x.read(p)