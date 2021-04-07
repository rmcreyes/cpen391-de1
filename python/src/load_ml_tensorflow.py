
import numpy as np
import os
import constants
from tensorflow import keras # only import tensorflow if necessary, so be careful when importing this file!

# take image and flatten them into float32 arrays
# args:
# > the openCV images of the cropped characters
# returns:
# > flattened float32 array versions of the image arrays
def create_flat_imgs(images):
	final_images = []
	for elem in images:
		img = elem.flatten()
		img = img / 255.0
		final_images.append(img)
	return np.array(final_images, dtype="float32")

# convert the openCV image to be a flattened num array and load it into tensorflor running custom h5
# args:
# > the openCV images of the cropped characters
# returns:
# > the string recognized (no spaces)
def recog_images_tensorflow(images):
    model = keras.models.load_model(constants.NN_H5)

    # custom flattening for images before using them to predict
    test_images = create_flat_imgs(images)
    predictions = model.predict(test_images)

    final_str = ""
    for i in range(len(test_images)):
        most_probable_elem_index = np.argmax(predictions[i])
        final_str += constants.PREDICT_MAP[most_probable_elem_index]

    return final_str
