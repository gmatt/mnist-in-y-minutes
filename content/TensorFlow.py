# ! pip install tensorflow

# Source:
# https://github.com/tensorflow/docs/blob/7d9aab3abb979d304e768df250b7fd069d60497e/site/en/tutorials/quickstart/beginner.ipynb

import os
import random

import numpy as np
import tensorflow as tf

print("TensorFlow version:", tf.__version__)
# <<< TensorFlow version: 2.[output omitted]


# For some reason, this is required. `tf.random.set_seed` alone is not enough.
# https://stackoverflow.com/questions/60058588/tensorflow-2-0-tf-random-set-seed-not-working-since-i-am-getting-different-resul
def reset_random_seeds():
    os.environ["PYTHONHASHSEED"] = str(2)
    tf.random.set_seed(2)
    np.random.seed(2)
    random.seed(2)


mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
# <<< Downloading data from https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz
# <<< [output omitted]
# <<< 11490434/11490434 [==============================] - 0s 0us/step

x_train, x_test = x_train / 255.0, x_test / 255.0
reset_random_seeds()
model = tf.keras.models.Sequential(
    [
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10),
    ]
)
predictions = model(x_train[:1]).numpy()
predictions
# <<< array([[-0.00309502,  0.37660164, -0.05277926, -0.5661213 ,  0.26350388,
# <<<          0.3394952 ,  0.09216529,  0.06622345, -0.03807542, -0.4552781 ]],
# <<<       dtype=float32)
tf.nn.softmax(predictions).numpy()
# <<< array([[0.095506  , 0.13961458, 0.0908768 , 0.05438904, 0.12468466,
# <<<         0.13452893, 0.10505135, 0.10236117, 0.09222291, 0.06076451]],
# <<<       dtype=float32)
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
loss_fn(y_train[:1], predictions).numpy()
# <<< 2.0059762
model.compile(optimizer="adam", loss=loss_fn, metrics=["accuracy"])

model.fit(x_train, y_train, epochs=5)
# <<< Epoch 1/5
# <<< [output omitted]
# <<< Epoch 2/5
# <<< [output omitted]
# <<< Epoch 3/5
# <<< [output omitted]
# <<< Epoch 4/5
# <<< [output omitted]
# <<< Epoch 5/5
# <<< [output omitted]
# <<< <keras.callbacks.History object at [output omitted]>
model.evaluate(x_test, y_test, verbose=2)
# <<< 313/313 - [output omitted]s - loss: 0.0703 - accuracy: 0.9776 - [output omitted]s/epoch - [output omitted]s/step
# <<< [0.07030097395181656, 0.9775999784469604]
