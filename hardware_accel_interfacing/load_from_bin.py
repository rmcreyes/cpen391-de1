import numpy as np
from ctypes import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()

if args.file is None:
    print("no file provided")
    quit()

bin_arr = np.fromfile('6_3.bin', dtype='int32')
print(bin_arr)

p = (c_int*len(bin_arr))()

for idx,elem in enumerate(bin_arr):
    p[idx] = elem.item()

x = CDLL('./libnn.so')
x.run.argtype = POINTER(c_int)
x.run.restype = c_int

print(x.run(p))
