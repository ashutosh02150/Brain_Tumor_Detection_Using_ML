# -*- coding: utf-8 -*-
"""DEEPLEARNING_PROJECT2_89_99-2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vnE8m97yRU7S324dvwxkhrjxSLFrODbu
"""

# from google.colab import drive
# drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# !pip install imutils
import numpy as np
import pandas as pd
import random
import os
from os import listdir
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

# %matplotlib inline
import imutils
import argparse
import cv2
import keras

from tensorflow.keras.models import Sequential
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import (
    Conv2D,
    Input,
    ZeroPadding2D,
    BatchNormalization,
    Flatten,
    Activation,
    Dense,
    MaxPooling2D,
)
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle  # shuffling the data improves the model


def load_data(folder, image_size):
    # load all images in a directory
    X = []
    y = []
    image_width, image_height = image_size

    for filename in os.listdir(folder):
        new_dir = folder + "/" + filename
        for img in os.listdir(new_dir):
            image = cv2.imread(new_dir + "/" + img)
            image = cv2.resize(image, dsize=(image_width, image_height))
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            hsv = hsv / 127.5 - 1
            X.append(hsv)
            if new_dir[-3:] == "yes":
                y.append([1])
            else:
                y.append([0])

    X = np.array(X)
    y = np.array(y)

    # Shuffle the data
    X, y = shuffle(X, y)

    # print(f"Number of examples is: {len(X)}")
    # print(f"X shape is: {X.shape}")
    # print(f"y shape is: {y.shape}")
    # print(X_train[1:])

    return X, y


IMG_WIDTH, IMG_HEIGHT = (64, 64)

X, y = load_data(
    "./Dataset",
    (IMG_WIDTH, IMG_HEIGHT),
)


def split_data(X, y, test_size=0.20):
    X_train, X_test_val, y_train, y_test_val = train_test_split(
        X, y, test_size=test_size
    )
    X_test, X_val, y_test, y_val = train_test_split(
        X_test_val, y_test_val, test_size=0.20
    )

    return X_train, y_train, X_val, y_val, X_test, y_test


X_train, y_train, X_val, y_val, X_test, y_test = split_data(X, y, test_size=0.2)

"""# Model Generation"""

# Create a model
model = Sequential()

# First Layer
model.add(
    Conv2D(filters=32, kernel_size=(3, 3), activation="relu", input_shape=(64, 64, 3))
)

# Second Layer
model.add(MaxPooling2D(pool_size=(2, 2)))

# Third Layer
model.add(Flatten())  # Flatten feature arrays

# Fourth Layer
model.add(Dense(128, activation="relu"))  # Add hidden dense layer

# Fifth Layer
model.add(Dense(1, activation="sigmoid"))  # Add output layer

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

model.fit(
    x=X_train, y=y_train, batch_size=32, epochs=40, validation_data=(X_val, y_val)
)


def predict_tumor(image_path):
    # Load and preprocess the image
    image = cv2.imread(image_path)
    image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image = image / 127.5 - 1
    image = np.expand_dims(image, axis=0)

    # Make the prediction
    prediction = model.predict(image)
    prediction = prediction > 0.5

    if prediction:
        return "Tumor"
    else:
        return "No Tumor"


# print("Our model says it is a :", predict_tumor("./Dataset/yes/Y1.jpg"))
