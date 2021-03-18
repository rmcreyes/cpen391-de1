import load_nn_to_c
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()

if args.file is None:
    print("no file provided")
    quit()

load_nn_to_c.load_c_nn()

bin_arr = np.fromfile(args.file, dtype='int32')

print(load_nn_to_c.run_c_nn(bin_arr))
