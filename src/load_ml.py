
import numpy as np
import os
import constants
if constants.GEN_BIN:
    import c_interfacing_utils

# mapping labels to actual character
# 0-9 represents the 0-9 characters
# 10-25 represents A-Z
predict_map = ['0','1','2','3','4','5',
            '6','7','8','9','A','B',
            'C','D','E','F','G','H',
            'I','J','K','L','M','N',
            'O','P','Q','R','S','T',
            'U','V','W', 'X','Y','Z']

def create_flat_imgs(images):
	final_images = []
	for elem in images:
		img = elem.flatten()
		img = img / 255.0
		final_images.append(img)
	return np.array(final_images, dtype="float32")

def recog_images_tensorflow(images):
    from tensorflow import keras # only import tensorflow if necessary... it takes a while to import
    model = keras.models.load_model('models/model_hl_1000_750.h5')

    # custom flattening for images before using them to predict
    test_images = create_flat_imgs(images)
    predictions = model.predict(test_images)

    final_str = ""
    for i in range(len(test_images)):
        most_probable_elem_index = np.argmax(predictions[i])
        final_str += predict_map[most_probable_elem_index]

    return final_str

def recog_images_c(images):
    final_str = ""
    for i,img in enumerate(images):
        mod_img = img.flatten()
        mod_img = mod_img/255.0

        # images must be multiplied by 2^16, as needed by lower level process Q16.16 floating point
        mod_img = np.array(mod_img*65536.0,dtype="int32")
        if constants.CREATE_BIN:
            mod_img.tofile(f"output/custom_char_{i}.bin")
        else:
            most_probable_elem_index = c_interfacing_utils.run_c_nn(mod_img)
            final_str += predict_map[most_probable_elem_index]

    return final_str
