from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import emnist
import random
from PIL import Image
import os
import struct

model = keras.models.load_model("letterrecog256_mod_3.h5")

final_nums = np.array([], dtype='float32')
for i in range(0,len(model.layers)):
    print(i)
    layer = model.layers[i].get_weights()

    final_nums = np.append(final_nums,layer[1])

    final_weights = []
    weights = layer[0]

    j = 0
    print(len(weights[0]))
    print(len(weights))
    while j < len(weights[0]):
        for i in range(len(weights)):
            final_weights.append(weights[i][j])
        j+=1

    final_nums = np.append(final_nums,final_weights)

np.savetxt('output.bin', final_nums, fmt="%f")

final_nums = np.array(final_nums*65536.0,dtype="int32")
final_nums.tofile("output2.bin")