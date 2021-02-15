
import numpy as np
import os

def create_flat_imgs(images):
	final_images = []
	for elem in images:
		img = elem.flatten()
		img = img / 255.0
		final_images.append(img)
	return np.array(final_images, dtype="float32")

def recog_images(images):
    from tensorflow import keras # only import tensorflow if necessary... it takes a while to import
    model = keras.models.load_model('letterrecog256.h5')

    test_images = create_flat_imgs(images)
    predictions = model.predict(test_images)

    predict_map = ['0','1','2','3','4','5',
                '6','7','8','9','A','B',
                'C','D','E','F','G','H',
                'I','J','K','L','M','N',
                'O','P','Q','R','S','T',
                'U','V','W', 'X','Y','Z']

    final_str = ""
    for i in range(len(test_images)):
        final_str += predict_map[np.argmax(predictions[i])]

    return final_str

def create_bin(images):
    for i,img in enumerate(images):
        mod_img = img.flatten()

        mod_img = mod_img/255.0

        mod_img = np.array(mod_img*65536.0,dtype="int32")
        mod_img.tofile(f"output/custom_char_{i}.bin")