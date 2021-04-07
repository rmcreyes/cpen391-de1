from tensorflow import keras
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", nargs='?', const="")
args = parser.parse_args()

model = keras.models.load_model(args.file)

str_label = args.file[0:args.file.find(".")]

final_nums = np.array([], dtype='float32')
for i in range(0,len(model.layers)):
    layer = model.layers[i].get_weights()

    final_nums = np.append(final_nums,layer[1])

    final_weights = []
    weights = layer[0]

    j = 0
    print(f"L{i} input: {len(weights)}")
    print(f"L{i} output: {len(weights[0])}")
    while j < len(weights[0]):
        for i in range(len(weights)):
            final_weights.append(weights[i][j])
        j+=1

    final_nums = np.append(final_nums,final_weights)

final_nums = np.array(final_nums*65536.0,dtype="int32")
final_nums.tofile(f"{str_label}_generated_nn.bin")