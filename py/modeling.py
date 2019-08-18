#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import keras
import unittest
import statsmodels.api as sm

def flatten_shape(shape):
    s = 1
    for v in shape[1:]:
        s *= v
    return (shape[0], s)

def flatten(X):
    shape = X.shape
    s = 1
    for v in shape[1:]:
        s *= v
    Xt = X.copy()
    Xt.resize(shape[0], s)
    return Xt

class ConvoNeuralNet(object):

    def create(self, shape, out=1, activation='relu'):
        # TODO: add arguments to specify convolutions
        model = keras.Sequential()
        model.add(keras.layers.Conv2D(32, (2,2), activation=activation, input_shape=shape[1:]))
        model.add(keras.layers.Conv2D(32, (2,2), activation=activation))
        model.add(keras.layers.Flatten())
        model.add(keras.layers.Dense(20, activation=activation))
        model.add(keras.layers.Dense(5, activation=activation))
        model.add(keras.layers.Dense(out))
        model.compile(optimizer='rmsprop', loss='mse')
        self.model = model

    def train(self, X, y, epochs=50, batch_size=256, verbose=0):
        self.history = self.model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=verbose)

    def predict(self, X):
        return self.model.predict([X])[:,0]

class NeuralNet(object):

    def create(self, shape, layers=[10, 10], out=1, activation='relu'):
        if len(shape) > 2 : shape = flatten_shape(shape)
        model = keras.Sequential()
        for i, l in enumerate(layers):
            if i==0:
                model.add(keras.layers.Dense(l, activation=activation, input_shape=(shape[1:])))
            else:
                model.add(keras.layers.Dense(l, activation=activation))
        model.add(keras.layers.Dense(out))
        model.compile(optimizer='rmsprop', loss='mse')
        self.model = model

    def train(self, X, y, epochs=50, batch_size=256, verbose=0):
        if len(X.shape) > 2 : X = flatten(X)
        self.history = self.model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=verbose)

    def predict(self, X):
        if len(X.shape) > 2 : X = flatten(X)
        return self.model.predict([X])[:,0]

    def review_history(history):
        history_dict = history.history
        train_loss_values = history_dict['loss']
        test_loss_values = history_dict['val_loss']
        epochs = range(1, len(train_loss_values) + 1)
        plt.plot(epochs, train_loss_values, 'bo', label='Training loss')
        plt.plot(epochs, test_loss_values, 'b', label='Test loss')
        plt.title('Training and test loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.show()

    def review_prediction(model, X_train, y_train, X_test, y_test):
        predictions = model.predict(X_test)
        df = pd.DataFrame({'x':predictions[:,0], 'y':y_test})
        df.plot.scatter(x=0, y=1)
        print(df.corr())
        return df

class Regression(object):

    def create(self, shape):
        self.model = None

    def train(self, X, y):
        if len(X.shape) > 2 : X = flatten(X)
        self.model = sm.OLS(y, X).fit()

    def predict(self, X):
        if len(X.shape) > 2 : X = flatten(X)
        return self.model.predict(np.array([X]))[0]

class Model(object):

    def __init__(self, param, shape=None):
        self.param = param
        if shape is not None:
            self.create(shape)

    def create(self, shape):
        if self.param['method']=='cnn':
            self.model = ConvoNeuralNet()
            self.model.create(shape)
        if self.param['method']=='nn':
            self.model = NeuralNet()
            self.model.create(shape, layers=self.param['layers'])
        if self.param['method']=='reg':
            self.model = Regression()

    def train(self, X, y):
        if self.param['method']=='cnn':
            return self.model.train(X, y)
        if self.param['method']=='nn':
            return self.model.train(X, y)
        if self.param['method']=='reg':
            return self.model.train(X, y)

    def predict(self, X):
        if self.param['method']=='cnn':
            return self.model.predict(X)
        if self.param['method']=='nn':
            return self.model.predict(X)
        if self.param['method']=='reg':
            return self.model.predict(X)

####################
### UNIT TESTING ###
####################

class TestConv0NeuralNet(unittest.TestCase):

    def test_convo_nn(self):
        raised = False
        try:
            shape=(10,5,20,1)
            cnn = ConvoNeuralNet()
            cnn.create(shape)
            X = np.ones(shape)
            y = np.ones((10,))
            cnn.train(X, y)
            cnn.predict(X)
        except:
            raised = True
        self.assertFalse(raised)

class TestNeuralNet(unittest.TestCase):

    def test_dim_one(self):
        raised = False
        try:
            nn = NeuralNet()
            nn.create(shape=(0,2))
            X = np.ones((10,2))
            y = np.ones((10,))
            nn.train(X, y)
            nn.predict(X)
        except:
            raised = True
        self.assertFalse(raised)

    def test_dim_two(self):
        raised = False
        try:
            nn = NeuralNet()
            nn.create(shape=(0,2,2))
            X = np.ones((10,2,2))
            y = np.ones((10,))
            nn.train(X, y)
        except:
            raised = True
        self.assertFalse(raised)

class TestRegression(unittest.TestCase):

    def test_regression_dim_one(self):
        raised = False
        try:
            lm = Regression()
            lm.create((100,2))
            X = np.ones((10,2))
            y = np.ones((10,))
            lm.train(X, y)
            lm.predict(X)
        except:
            raised = True
        self.assertFalse(raised)

    def test_regression_dim_two(self):
        raised = False
        try:
            lm = Regression()
            lm.create((100,2))
            X = np.ones((10,2,2))
            y = np.ones((10,))
            lm.train(X, y)
            lm.predict(X)
        except:
            raised = True
        self.assertFalse(raised)


class TestModel(unittest.TestCase):

    def test_convo_neural_net(self):
        raised = False
        try:
            param = { 'method':'cnn' }
            cnn = Model(param, (100,5,20,1))
            X = np.ones((10,5,20,1))
            y = np.ones((10,))
            cnn.train(X, y)
        except:
            raised = True
        self.assertFalse(raised)

    def test_neural_net(self):
        raised = False
        try:
            param = { 'method':'nn', 'layers':[10,5] }
            nn = Model(param, (100,2))
            X = np.ones((10,2))
            y = np.ones((10,))
            nn.train(X, y)
        except:
            raised = True
        self.assertFalse(raised)

    def test_regression(self):
        raised = False
        try:
            param = { 'method':'reg'}
            nn = Model(param, (100,2))
            X = np.ones((10,2))
            y = np.ones((10,))
            nn.train(X, y)
        except:
            raised = True
        self.assertFalse(raised)

if __name__ == '__main__':
    unittest.main()





