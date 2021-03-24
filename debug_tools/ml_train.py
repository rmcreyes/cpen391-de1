import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import emnist
import pickle
import os
from PIL import Image

def get_from_files(dirname):
	images = []
	labels = []
	for filename in os.listdir(dirname):
		image = Image.open(os.path.join(dirname, filename))
		str_label = filename[0:filename.find("_")]
		labels.append(int(str_label))
		data = np.asarray(image)
		images.append(data)
	return images, labels

def remove(max_digit, x, y):
    idx = (y <= max_digit).nonzero()
    return x[idx], y[idx]

def flat(images):
	final_images = []
	print("start flattening group")
	for elem in images:
		img = elem.flatten()
		img = img / 255.0
		final_images.append(img)
	print("done flattening group")
	
	return np.array(final_images, dtype="float32")

extra_train_images, extra_train_labels = get_from_files("custom_data/train")
extra_test_images, extra_test_labels = get_from_files("custom_data/test")

train_images_total, train_labels_total = emnist.extract_training_samples('byclass')
test_images_total, test_labels_total = emnist.extract_test_samples('byclass')

train_images_total, train_labels_total = remove(35, train_images_total[0:400000], train_labels_total[0:400000])
test_images_total, test_labels_total = remove(35, test_images_total[0:1000], test_labels_total[0:1000])

test_images_total = test_images_total[0:300]
test_labels_total = test_labels_total[0:300]


train_images_total = np.concatenate((train_images_total,extra_train_images))
train_labels_total =np.concatenate((train_labels_total,extra_train_labels))

test_images_total = np.concatenate((test_images_total,extra_test_images))
test_labels_total =np.concatenate((test_labels_total,extra_test_labels))

train_images = flat(train_images_total)
test_images = flat(test_images_total)

model = keras.Sequential([
	keras.layers.Dense(1000, activation="relu"),
	keras.layers.Dense(1000, activation="relu"),
	keras.layers.Dense(36, activation="softmax")
	])

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

model.fit(train_images, train_labels_total, epochs=10)

test_loss, test_acc = model.evaluate(test_images, test_labels_total)

print('\nTest accuracy:', test_acc)

predictions = model.predict(test_images)

model.save('letterrecog1000_750.h5')