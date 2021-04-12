import numpy as np
from ctypes import *
import constants

if constants.USE_C:
    x = CDLL(constants.LIBNN_SO_FILE)

# convert the openCV images to binary arrays and loads them into the custom NN
# args:
# > the openCV images of the cropped characters
# returns:
# > the string recognized (no spaces)
def recog_images_c(images):
    final_str = ""
    for i,img in enumerate(images):
        mod_img = img.flatten()
        mod_img = mod_img/255.0

        # images must be multiplied by 2^16, as needed by lower level process Q16.16 floating point
        mod_img = np.array(mod_img*65536.0,dtype="int32")
        if constants.CREATE_BIN:
            mod_img.tofile(f"output/custom_char_{i}.bin")

        most_probable_elem_index = run_c_nn(mod_img)
        final_str += constants.PREDICT_MAP[most_probable_elem_index]

    return final_str

# loads nn into custom neural network written in C.
def load_c_nn():
    bin_arr = np.fromfile(constants.NN_BIN, dtype='int32')

    num_elems = len(bin_arr)

    p = (c_int*num_elems)()

    for idx,elem in enumerate(bin_arr):
        p[idx] = elem.item()

    x.init_accel.argtype = POINTER(c_int),c_int,c_int,c_int,c_int
    x.init_accel.restype = c_int

    x.init_accel(p, constants.IN_SIZE, constants.L1_SIZE, constants.L2_SIZE, constants.L3_SIZE)

# Runs the hardware-accelerated neural network on the resultant bin file
# args:
# > binary array representing the photo
# returns:
# > the index of the character identified
def run_c_nn(bin_arr):
    p = (c_int*len(bin_arr))()

    for idx,elem in enumerate(bin_arr):
        p[idx] = elem.item()

    x.run.argtype = POINTER(c_int)
    x.run.restype = c_int

    return x.run(p)
