import numpy as np
import tensorflow as tf


classes = ["neg", "pos"]


def load_model(model_file_path):
    model = tf.keras.models.load_model(model_file_path)
    return model


def Text_to_Tensor_converter(text_list):
    if len(text_list) == 1:
        output = tf.constant(text_list, shape=(1, ))
    
    elif len(text_list) > 1:
        output = tf.constant(text_list)

    return output

def result_converter(x):
    if x < 0:
        x = 0
    elif x > 0:
        x = 1
    return classes[x]

