#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import keras

import statsmodels.api as sm

##

def discount_reward(rewards, discount):
    running_reward = 0.0
    discounted_rewards = np.array([], 'float')
    for i in reversed(range(rewards.shape[0])):
        discounted_rewards = np.concatenate(([running_reward], discounted_rewards))
        running_reward = running_reward * discount + rewards[i] * (1 - discount)
    return(discounted_rewards)

def create_model(shape, layers=[10, 10], out=1, activation='relu'):
    model = keras.Sequential()
    for i, l in enumerate(layers):
        if i==0:
            model.add(keras.layers.Dense(l, activation=activation, input_shape=(shape[1],)))
        else:
            model.add(keras.layers.Dense(l, activation=activation))
    model.add(keras.layers.Dense(out))
    model.compile(optimizer='rmsprop', loss='mse')
    return(model)

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

# Generic RI control class not specific to task at hand
class RLBase(object):

    def __init__(self, state_space):
        self.state_space = state_space
        self.run_nr = 0
        self.all_states = np.empty((0, state_space))
        self.all_actions = np.empty((0, 1))
        self.all_rewards = np.empty((0, 1))
        self.all_discounted_rewards = np.empty((0,1))
        self.all_mean_rewards = np.empty((0,1))
        self.mean_reward_list = np.empty((0,1))
        self.before_after = np.empty((0,2))

    def pre(self, run_nr):
        self.run_nr = run_nr
        self.states = np.empty((0,self.state_space))
        self.actions = np.empty((0,1))
        self.rewards = np.empty((0,1))
        self.err = 0.0 # Set error
        self.err_discount = 0.9

    def post(self):
        self.run_nr += 1
        self.shift = 1
        self.all_states = np.append(self.all_states, self.states[0:-self.shift,:], 0)
        self.all_actions = np.append(self.all_actions, self.actions[0:-self.shift])
        self.all_rewards = np.append(self.all_rewards, self.rewards[self.shift:])

        # Mean reward
        mean_reward = np.mean(self.rewards)
        self.all_mean_rewards = np.append(self.all_mean_rewards, np.repeat(mean_reward, len(self.rewards) - 1))
        self.mean_reward_list = np.append(self.mean_reward_list, mean_reward)

        # Discounted reward
        discounted_rewards = discount_reward(self.rewards, 0.95)
        self.all_discounted_rewards = np.append(self.all_discounted_rewards, discounted_rewards[self.shift:])

    def decide(self, state, reward):
        self.states = np.append(self.states, np.array([state]), 0) # Store
        self.rewards = np.append(self.rewards, reward)  # Update reward list
        self.err = self.err * self.err_discount + (1 - self.err_discount) * ((random.random() - 0.5) / 30.0) # Update error

class RLStateAction(RLBase):

    def __init__(self, state_space, layers, pause=False):
        super(RLStateAction, self).__init__(state_space)
        self.layers = layers
        self.model_mimic = create_model((-1, state_space), self.layers)
        self.model_state_action = create_model((-1, state_space + 1), self.layers)
        self.pre(0)

    def pre(self, run_nr):
        super(RLStateAction, self).pre(run_nr)

        # train model
        if run_nr == 1:
            #self.model_mimic.fit(self.all_states, self.all_actions, epochs=50, batch_size=256, verbose=0)
            self.model_mimic_ols = sm.OLS(self.all_actions, self.all_states).fit()
        if run_nr > 0:
            all_states_actions = np.append(self.all_states, np.array([self.all_actions]).transpose(), axis=1)
            self.model_state_action.fit(all_states_actions, self.all_discounted_rewards, epochs=10, batch_size=256, verbose=0)

    def post(self):
        super(RLStateAction, self).post()

    def decide(self, state, reward, action):
        super(RLStateAction, self).decide(state, reward)
        if self.run_nr == 0:
            self.act = action
        if self.run_nr > 0:
            #self.act_mimic = self.model_mimic.predict(np.array([state]))[0,0]
            self.act_mimic = self.model_mimic_ols.predict(np.array([state]))[0]
            self.before_after = np.append(self.before_after, np.array([[action, self.act_mimic]]), axis=0)
        if self.run_nr > 0:
            pos_actions = np.arange(-0.25, 0.25, 0.05)
            val = np.empty((0,1))
            for act in pos_actions:
                X = np.append(state, act)
                y = self.model_state_action.predict(np.array([X]))[0]
                val = np.append(val, y)
            if val.size > 0:
                print(val)
                best_act = pos_actions[np.argmax(val)]
                print('rl action: %.2f' % best_act)
                self.act_state_action = best_act
        if self.run_nr > 0:
            p = np.min([(self.run_nr - 1.0) / 10.0, 1.0])
            self.act = (1 - p) * self.act_mimic + p * self.act_state_action

        print(np.round(action, 3), " >> ", np.round(self.act, 3))

        self.actions = np.append(self.actions, self.act)
        return(self.act)
