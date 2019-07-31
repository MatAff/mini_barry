#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import random
import keras

class Retainer(object):

    def __init__(self, data):
        self.prev = data

    def retain(self, current):
        current = current.astype('float')
        current[np.isnan(current)] = self.prev[np.isnan(current)]
        self.prev = current
        return(current)

def discount_reward(rewards, discount):
    running_reward = 0.0
    discounted_rewards = np.array([], 'float')
    for i in reversed(range(rewards.shape[0])):
        discounted_rewards = np.concatenate(([running_reward], discounted_rewards))
        running_reward = running_reward * discount + rewards[i] * (1 - discount)
    return(discounted_rewards)

def create_model(shape):
    activation = 'relu'
    model = keras.Sequential()
    model.add(keras.layers.Dense(50, activation=activation, input_shape=(shape[1],)))
    model.add(keras.layers.Dense(20, activation=activation))
    model.add(keras.layers.Dense(20, activation=activation))
    model.add(keras.layers.Dense(1))
    model.compile(optimizer='rmsprop', loss='mse')
    return(model)

# Generic RI control class not specific to task at hand
class RLBase(object):

    def __init__(self, state_space):
        self.state_space = state_space
        self.all_states = np.empty((0, state_space))
        self.all_actions = np.empty((0, 1))
        self.all_rewards = np.empty((0, 1))

    def pre(self):
        self.states = np.empty((0,self.state_space))
        self.actions = np.empty((0,1))
        self.rewards = np.empty((0,1))

    def post(self):
        self.shift = 1
        self.all_states = np.append(self.all_states, self.states[0:-self.shift,:], 0)
        self.all_actions = np.append(self.all_actions, self.actions[0:-self.shift])
        self.all_rewards = np.append(self.all_rewards, self.rewards[self.shift:])

# RI Control class dedicated to task
class RLLineFollow(RLBase):

    def __init__(self, state_space):
        super(RLLineFollow, self).__init__(state_space)
        self.phase = 0
        self.all_discounted_rewards = np.empty((0,1))
        self.all_mean_rewards = np.empty((0,1))
        self.mean_reward_list = np.empty((0,1))

    def pre(self, run_nr):
        super(RLLineFollow, self).pre() # Run super
        self.ret = Retainer(np.zeros(self.state_space))        # Set retrainer
        self.err = 0.0 # Set error
        self.err_discount = 0.9

    def post(self, run_nr):
        super(RLLineFollow, self).post()  # Run super
        self.phase = min(self.phase + 1, 2) # Update phase

        # Mean reward
        mean_reward = np.mean(self.rewards)
        print('Mean reward (less is better): %.2f' % mean_reward)
        self.all_mean_rewards = np.append(self.all_mean_rewards, np.repeat(mean_reward, len(self.rewards) - 1))
        self.mean_reward_list = np.append(self.mean_reward_list, mean_reward)

        # Discounted reward
        discounted_rewards = discount_reward(self.rewards, 0.95)
        self.all_discounted_rewards = np.append(self.all_discounted_rewards, discounted_rewards[self.shift:])

    def decide(self, state, reward):
        self.rewards = np.append(self.rewards, reward)  # Update reward list
        self.state = self.ret.retain(np.array(state)) # Insert retained values
        self.err = self.err * self.err_discount + (1 - self.err_discount) * ((random.random() - 0.5) / 30.0) # Update error
        self.states = np.append(self.states, np.array([self.state]), 0) # Store

# RI control class based on subsetting learning data
class RLStateAction(RLLineFollow):

    def __init__(self, state_space):
        super(RLStateAction, self).__init__(state_space)

    def pre(self, run_nr):
        super(RLStateAction, self).pre(run_nr)

        if run_nr > 0:
            all_states_actions = np.append(self.all_states, np.array([self.all_actions]).transpose(), axis=1)
            self.model = create_model(all_states_actions.shape)
            self.model.fit(all_states_actions, self.all_discounted_rewards, epochs=50, batch_size=256, verbose=0)

    def post(self, run_nr):
        super(RLStateAction, self).post(run_nr)
        #plt.show()

    def decide(self, state, reward, action):
        super(RLStateAction, self).decide(state, reward)
        if self.phase == 0:
            self.rotate = action
        else:
            pos_actions = np.arange(-0.50, 0.50, 0.05)
            val = np.empty((0,1))
            for act in pos_actions:
                X = np.append(self.state, act)
                y = self.model.predict(np.array([X]))[0]
                val = np.append(val, y)
            #plt.plot(val)
            if val.size > 0:
                best_act = pos_actions[np.argmax(val)]
                print('rl action: %.2f' % best_act)
                self.rotate = best_act

        self.actions = np.append(self.actions, self.rotate)
        return(self.rotate)

class rl_manager(object):

    def __init__(self, state_space, do_run=True):
        self.control = RLStateAction(state_space)
        self.control.pre(run_nr=0)
        self.do_run = do_run

    def switch_batch(self, run_nr):
        if self.do_run:
            self.control.post(run_nr - 1)
            self.control.pre(run_nr)
            self.control.phase = run_nr

    def decide(self, state, reward, action):
        if self.do_run:
            action = self.control.decide(state, reward, action)
        return action

# Plot
#plt.plot(control.mean_reward_list)
#plt.show()
