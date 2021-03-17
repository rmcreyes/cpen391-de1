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

x = CDLL('./libnn.so')
x.init_accel.argtype = POINTER(c_int),c_int,c_int,c_int,c_int
x.init_accel.restype = c_int

print(x.init_accel(p,in_size,l1_size,l2_size,l3_size))
