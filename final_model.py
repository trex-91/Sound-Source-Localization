# -*- coding: utf-8 -*-
"""Final Model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EixPBhlCkQiWXVuQ3n0oPI8DbCaVAVc2
"""

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from keras import layers
from scipy.io import loadmat
from scipy.io import savemat
import pandas as pd
from keras.models import Model
from keras.layers import Input
from google.colab import drive
drive.mount('/content/drive')

#Deep Learning Model (Autoencoder)
encoder_input = keras.Input(shape=(600,600,1), name="Map")
x = layers.MaxPooling2D((3,3), padding="same")(encoder_input)
x = layers.Conv2D(600, (3,3), activation="relu", padding="same")(x)
x = layers.Conv2D(600, (3,3), activation="relu", padding="same")(x)
x = layers.MaxPooling2D((2,2), padding="same")(x)
x = layers.Conv2D(300, (3,3), activation="relu", padding="same")(x)
x = layers.Conv2D(300, (3,3), activation="relu", padding="same")(x)
x = layers.MaxPooling2D((2,2), padding="same")(x)
x = layers.Conv2D(150, (2,2), activation="relu", padding="same")(x)
x = layers.Conv2D(150, (2,2), activation="relu", padding="same")(x)
encoder_output = layers.MaxPooling2D((2,2), padding="same")(x)

encoder = keras.Model(encoder_input, encoder_output, name="encoder")
encoder.summary()

x = layers.Conv2DTranspose(150, (2,2), activation="relu", padding="same")(encoder_output)
x = layers.UpSampling2D((2,2))(x)
x = layers.Conv2DTranspose(150, (2,2), activation="relu", padding="same")(x)
x = layers.UpSampling2D((2,2))(x)
x = layers.Conv2DTranspose(300, (3,3), activation="relu", padding="same")(x)
x = layers.Conv2DTranspose(300, (3,3), activation="relu", padding="same")(x)
x = layers.UpSampling2D((2,2))(x)
x = layers.Conv2DTranspose(600, (3,3), activation="relu", padding="same")(x)
x = layers.Conv2DTranspose(600, (3,3), activation="relu", padding="same")(x)
x = layers.UpSampling2D((3,3))(x)
decoder_output = layers.Conv2DTranspose(1, (3,3), activation="linear", padding="same")(x)


decoder = keras.Model(encoder_output, decoder_output, name="decoder")
decoder.summary()

autoencoder_input = keras.Input(shape=(600,600,1), name="Map")
encoded = encoder(autoencoder_input)
decoded = decoder(encoded)
autoencoder = keras.Model(autoencoder_input, decoded, name="autoencoder")
autoencoder.summary()

#Loading and Arranging the Data Set
data2 = loadmat('/content/drive/MyDrive/Data_Set_2D_1.23.mat')
X_copy = data2['Training_Data_2D']
Y_copy = data2['Target_Value_2D']
X_copy=X_copy*10
Y_copy=Y_copy*10
print(np.shape(X_copy))
print(np.shape(Y_copy))
X_copy=np.reshape(X_copy, (11, len(X_copy), len(X_copy)))
Y_copy=np.reshape(Y_copy, (11, len(Y_copy), len(Y_copy)))
print("X_copy size is", np.shape(X_copy))
print("Y_copy size is", np.shape(Y_copy))
X=np.zeros((11,600,600))
Y=np.zeros((11,600,600))
j=-1
for i in [8, 2, 3, 10, 4, 5, 7,
          1, 9, 11, 6]:
  j+=1
  X[j]=X_copy[i-1]
  Y[j]=Y_copy[i-1]

print("X size is", np.shape(X))
print("Y size is", np.shape(Y))
print(i)
print(j)

# compile the model
#opt = keras.optimizers.Adam(learning_rate=1e-4)
autoencoder.compile(loss='rmse', optimizer="Adam", metrics=['mse'])

# Training the model and saving the best one
model_checkpoint_callback = keras.callbacks.ModelCheckpoint("1.22 11SS 1st mse multiplyed_by_10 Ep350 Auto_Save Adam_lr_-2.h5", monitor="loss",
    verbose=0,
    save_best_only=True,
    save_weights_only=True,
    mode="min")
# fit the test model on the dataset
history=autoencoder.fit(X, Y, batch_size=1, epochs=350, shuffle=False, validation_split=0.3, callbacks=[model_checkpoint_callback])

# Predicting on the data set and saving the result
#autoencoder.load_weights("1.20 11SS 7th mse multiplyed_by_10 Ep750 No_Validation Auto_Save.h5")
predictions = autoencoder.predict(X, batch_size=7)
predictions=np.reshape(predictions/10, (600, 600, 11))
savemat("predictions2D-1.23 11SS 1sth Ep350 mse multied_10 New_TV All_Linear.mat", {'Prediction':predictions})