import numpy as np
from ctypes import *
import constants

in_size = 784
l1_size = 1000
l2_size = 750
l3_size = 36

if constants.GEN_BIN:
    x = CDLL('./src/compiled_c/libnn.so')

def load_c_nn():
    bin_arr = np.fromfile('models/model_hl_1000_750_generated_nn.bin', dtype='int32')

    num_elems = len(bin_arr)

    p = (c_int*num_elems)()

    for idx,elem in enumerate(bin_arr):
        p[idx] = elem.item()

    x.init_accel.argtype = POINTER(c_int),c_int,c_int,c_int,c_int
    x.init_accel.restype = c_int

    x.init_accel(p,in_size,l1_size,l2_size,l3_size)


def run_c_nn(bin_arr):
    p = (c_int*len(bin_arr))()

    for idx,elem in enumerate(bin_arr):
        p[idx] = elem.item()

    x.run.argtype = POINTER(c_int)
    x.run.restype = c_int

    return x.run(p)