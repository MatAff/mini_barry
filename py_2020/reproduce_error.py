

import numpy as np
from queue import Queue
import threading
import time


import keras

# sample data
X = np.random.rand(10, 3)
y = np.random.rand(10,)

que = Queue()


def create_model(X, y):

    activation='relu'
    out = 1
    
    model = keras.Sequential()
    model.add(keras.layers.Dense(10, activation=activation, input_shape=(X.shape[1:])))
    model.add(keras.layers.Dense(out))
    model.compile(optimizer='rmsprop', loss='mse')

    return model


# train model function
def train_model(model, X, y):

    model = create_model(X, y)

    epochs=50
    batch_size=256
    verbose=0

    # train
    model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=verbose)

    return model


def train_model_weights(model, X, y):
    return train_model(model, X, y).get_weights()


model = create_model(X, y)

# # train not on thread
# que.put(train_model_weights(model, X, y))

# train on thread
t = threading.Thread(target=lambda q, m, X, y: q.put(train_model_weights(m, X, y)), args=(que, model, X, y))
t.start()

while que.empty():
    time.sleep(1)

weights = que.get()
print(weights)

# model = create_model(X, y)
model.set_weights(weights)

# use mode to predict
res = model.predict(X)

print(res)

#  w = model.get_weights(), send the list of numpy arrays to the Queue, and then model.set_weights(w)