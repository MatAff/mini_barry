#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from reinforcement_learning import create_model, review_history, review_prediction

bf = pd.DataFrame(np.clip(rl.before_after, -1, 1))
print(rl.before_after)
print(bf.shape)
bf.plot()
bf.plot.scatter(x=0, y=1)

# get data
X = rl.all_states
y = rl.all_actions
print(X.shape)

#X = X[:400,]
#y = y[:400]

# split data
n = 1250
X_train = X[:n,]
X_test = X[n:,]
y_train = y[:n]
y_test = y[n:]
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

# get rl.layers
layers = rl.layers
print(layers)

# overwrite
layers = []

# create model and train
model_mimic = create_model((-1, 100), layers)
history = model_mimic.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=256, verbose=1)

# review training
review_history(history)

# review prediction
df = review_prediction(model_mimic, X_train, y_train, X_test, y_test)

### REGRESSION ###

import statsmodels.api as sm

# fit regression model
model_ols = sm.OLS(y_train, X_train).fit()

# review prediction
def review_prediction_ols(model, X_train, y_train, X_test, y_test):
    predictions = model.predict(X_test)
    df = pd.DataFrame({'x':predictions, 'y':y_test})
    df.plot.scatter(x=0, y=1)
    print(df.corr())
    return df

df = review_prediction_ols(model_ols, X_train, y_train, X_test, y_test)

