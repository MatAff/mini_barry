

import numpy as np
from queue import Queue
import threading
import time


import keras

# sample data
X = np.random.rand(10, 3)
y = np.random.rand(10,)

que = Queue()


# train model function
def train_model(X, y):

    activation='relu'
    out = 1
    
    model = keras.Sequential()
    model.add(keras.layers.Dense(10, activation=activation, input_shape=(X.shape[1:])))
    model.add(keras.layers.Dense(out))
    model.compile(optimizer='rmsprop', loss='mse')

    epochs=50
    batch_size=256
    verbose=0

    # train
    model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=verbose)

    return model

# # train not on thread
# model = train_model(X, y)
# que.put(model)

# train on thread
t = threading.Thread(target=lambda q, X, y: q.put(train_model(X, y)), args=(que, X, y))
t.start()

while que.empty():
    time.sleep(1)

model = que.get()

# use mode to predict
res = model.predict(X)

print(res)