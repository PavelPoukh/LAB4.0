# -*- coding: utf-8 -*-
"""step.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1h0eRKBCyPcSWn_7bp-JdNxzVbD-SKjsk
"""

# -*- coding: utf-8 -*-
"""step

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1s1_N1hhsl0JHqG3tk2uz35xZGfSW3Ypn
"""

"""This module implements data feeding and training loop to create model
to classify X-Ray chest images as a lab example for BSU students.
"""

__author__ = 'Alexander Soroka, soroka.a.m@gmail.com'
__copyright__ = """Copyright 2020 Alexander Soroka"""


import math
import random
import argparse
import glob
import numpy as np
import tensorflow as tf
import time
from tensorflow.python import keras as keras
from tensorflow.python.keras.callbacks import LearningRateScheduler



LOG_DIR = '/content/drive/My Drive/logs'
SHUFFLE_BUFFER = 4
BATCH_SIZE = 80
NUM_CLASSES = 6
PARALLEL_CALLS=4
RESIZE_TO = 224
TRAINSET_SIZE = 14034
VALSET_SIZE = 3000


def parse_proto_example(proto):
    keys_to_features = {
        'image/encoded': tf.io.FixedLenFeature((), tf.string, default_value=''),
        'image/class/label': tf.io.FixedLenFeature([], tf.int64, default_value=tf.zeros([], dtype=tf.int64))
    }
    example = tf.io.parse_single_example(proto, keys_to_features)
    example['image'] = tf.image.decode_jpeg(example['image/encoded'], channels=3)
    example['image'] = tf.image.convert_image_dtype(example['image'], dtype=tf.float32)
    example['image'] = tf.image.resize(example['image'], tf.constant([RESIZE_TO, RESIZE_TO]))
    return example['image'], tf.one_hot(example['image/class/label'], depth=NUM_CLASSES)


def normalize(image, label):
    return tf.image.per_image_standardization(image), label

def resize(image, label):
    return tf.image.resize(image, tf.constant([RESIZE_TO, RESIZE_TO])), label

def create_dataset(filenames, batch_size):
    """Create dataset from tfrecords file
    :tfrecords_files: Mask to collect tfrecords file of dataset
    :returns: tf.data.Dataset
    """
    return tf.data.TFRecordDataset(filenames)\
        .map(parse_proto_example)\
        .map(resize)\
        .map(normalize)\
        .batch(batch_size)\
        .prefetch(batch_size)


def build_model():
  
    model = tf.keras.applications.MobileNetV2(input_shape=(224,224,3),
                                           include_top=False,weights='imagenet'
                                           )
    return model

def step_decay(epoch):
   initial_lrate = 0.0001
   drop = 0.5         
   epochs_drop = 15.0   
   lrate = initial_lrate * math.pow(drop, math.floor((1+epoch)/epochs_drop))
   return lrate



def main():
    train_path = '/content/drive/My Drive/dataset/train*'
    test_path = '/content/drive/My Drive/dataset/val*'
    
    train_dataset = create_dataset(glob.glob(train_path), BATCH_SIZE)
    validation_dataset = create_dataset(glob.glob(test_path), BATCH_SIZE)
    lrate = LearningRateScheduler(step_decay)



    base_model = build_model()
    base_model.trainable = False
    model = tf.keras.models.Sequential([
      base_model,
      tf.keras.layers.Flatten(),
      tf.keras.layers.Dense(NUM_CLASSES, activation=tf.keras.activations.softmax)
    ])
    model.summary()

    model.compile(
        optimizer=tf.optimizers.SGD(lr=0.0, momentum=0.9),
        loss=tf.keras.losses.categorical_crossentropy,
        metrics=[tf.keras.metrics.categorical_accuracy],
    )

    log_dir='{}/ilcd-{}'.format(LOG_DIR, time.time())
    model.fit(
        train_dataset,
        epochs=100,
        validation_data=validation_dataset,
        callbacks=[
            tf.keras.callbacks.TensorBoard(log_dir),            
            tf.keras.callbacks.LearningRateScheduler(step_decay, verbose=1),
        ]
    )


if __name__ == '__main__':
    main()

# Commented out IPython magic to ensure Python compatibility.
# %load_ext tensorboard
# %tensorboard --logdir "/content/drive/My Drive/logs"
