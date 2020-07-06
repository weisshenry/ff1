# autoencoder denoising 
#import tensorflow.compat.v1 as tf #import tensorflow as tf
#tf.disable_v2_behavior()
import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random, time

gpu_devices = tf.config.experimental.list_physical_devices('GPU')
for device in gpu_devices:
    tf.config.experimental.set_memory_growth(device, True)

#config = tf.ConfigProto()
#config.gpu_options.allow_growth=True
#sess = tf.Session(config=config)
(xtran,ytran),(xtest,ytest) = tf.keras.datasets.fashion_mnist.load_data()
xtran = xtran/255 ; xtest = xtest/255 ; nf = 0.3
noitran = []
for img in xtran:
   nimg = img + nf * np.random.randn(*img.shape)
   nimg = np.clip(nimg,0,1)
   noitran.append(nimg)
noitran = np.array(noitran)
#------------------------
nf = 0.1
noitest = []
for img in xtest:
   nimg = img + nf * np.random.randn(*img.shape)
   nimg = np.clip(nimg,0,1)
   noitest.append(nimg)
noitest= np.array(noitest)
#----------------------------
autoenc = tf.keras.models.Sequential()
#----encoder ---
autoenc.add(tf.keras.layers.Conv2D(filters =16, kernel_size=3,strides =2,padding='same', input_shape=(28,28,1)))
autoenc.add(tf.keras.layers.Conv2D(filters =8, kernel_size=3,strides =2,padding='same'))
autoenc.add(tf.keras.layers.Conv2D(filters =8, kernel_size=3,strides =1,padding='same'))
#------decoder-----------
autoenc.add(tf.keras.layers.Conv2DTranspose(filters =16, kernel_size=3,strides =2,padding='same'))
autoenc.add(tf.keras.layers.Conv2DTranspose(filters =1, kernel_size=3,strides =2,activation='sigmoid',padding='same'))
#--------------------
autoenc.compile(loss='binary_crossentropy',optimizer=tf.keras.optimizers.Adam(lr=0.001))
autoenc.summary()
#------------------
autoenc.fit(noitran.reshape(-1,28,28,1), xtran.reshape(-1,28,28,1),
     epochs = 10,  batch_size = 200,
     validation_data = (noitest.reshape(-1,28,28,1),xtest.reshape(-1,28,28,1)))

