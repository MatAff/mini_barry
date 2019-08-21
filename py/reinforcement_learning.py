#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import random
import unittest
from modeling import Model, flatten

def discount_reward(rewards, discount=0.95):
    running_reward = 0.0
    discounted_rewards = np.array([], 'float')
    for i in reversed(range(rewards.shape[0])):
        discounted_rewards = np.concatenate(([running_reward], discounted_rewards))
        running_reward = running_reward * discount + rewards[i] * (1 - discount)
    return(discounted_rewards)

class RLBase(object):

    def __init__(self, state_space):
        self.state_space = state_space
        self.run_nr = 0
        self.all_states = np.empty((0, *state_space))
        self.all_actions = np.empty((0))
        self.all_rewards = np.empty((0))
        self.all_discounted_rewards = np.empty((0))

    def pre(self):
        self.states = np.empty((0, *self.state_space))
        self.actions = np.empty((0))
        self.rewards = np.empty((0))
        self.err = 0.0
        self.err_discount = 0.95

    def decide(self, state, reward):
        self.states = np.append(self.states, np.array([state]), 0)
        self.rewards = np.append(self.rewards, reward)
        self.err = self.err * self.err_discount + (1 - self.err_discount) * ((random.random() - 0.5) / 30.0)

    def store_action(self, action):
        self.actions = np.append(self.actions, action)

    def post(self):
        self.shift = 1
        discounted_rewards = discount_reward(self.rewards)
        self.all_states = np.append(self.all_states, self.states[0:-self.shift,:], 0)
        self.all_actions = np.append(self.all_actions, self.actions[0:-self.shift])
        self.all_rewards = np.append(self.all_rewards, self.rewards[self.shift:])
        self.all_discounted_rewards = np.append(self.all_discounted_rewards, discounted_rewards[self.shift:])
        self.run_nr += 1

class RLStateAction(RLBase):

    def __init__(self, state_space, mimic_param, state_action_param):
        super(RLStateAction, self).__init__(state_space)
        self.pre(0)
        self.mimic_model = Model(mimic_param, shape=(-1, *state_space))
        if len(state_space) > 1 :
            self.state_action_model = Model(state_action_param, (-1, state_space[0] * state_space[1] + 1))
        else:
            self.state_action_model = Model(state_action_param, (-1, state_space[0] + 1))

    def pre(self, run_nr):
        super(RLStateAction, self).pre()

        if run_nr == 1:
            self.mimic_model.train(X=self.all_states, y=self.all_actions)
        if run_nr > 1:
            all_states_flat = flatten(self.all_states)
            all_states_actions = np.append(all_states_flat, np.array([self.all_actions]).transpose(), axis=1)
            self.state_action_model.train(X=all_states_actions, y=self.all_discounted_rewards)

    def post(self):
        super(RLStateAction, self).post()

    def decide(self, state, reward, action):
        super(RLStateAction, self).decide(state, reward)
        if self.run_nr == 0:
            rl_action = action
        if self.run_nr > 0:
            rl_action_mimic = self.mimic_model.predict(np.array([state]))[0]
        if self.run_nr > 1:
            if len(state.shape) > 1 : state = flatten(np.array([state]))
            pos_actions = np.arange(-0.25, 0.25, 0.05)
            val = np.empty((0,1))
            for act in pos_actions:
                X = np.append(state, act)
                y = self.state_action_model.predict(np.array([X]))[0]
                val = np.append(val, y)
            print(val)
            best_act = pos_actions[np.argmax(val)]
            print('rl action: %.2f' % best_act)
            rl_action_state_action = best_act

        # combine results
        if self.run_nr > 0:
            rl_action = rl_action_mimic
        if self.run_nr > 1:
            rl_action = rl_action_state_action
            #p = np.min([(self.run_nr - 1.0) / 20.0, 1.0])
            #rl_action = (1 - p) * rl_action_mimic + p * rl_action_state_action

        print(np.round(action, 3), " >> ", np.round(rl_action, 3))
        super(RLStateAction, self).store_action(rl_action)
        return rl_action

class TestRL(unittest.TestCase):

    def test_RLBase_dim_one(self):
        # test RLBase class can be created using one dimentional tuple
        raised = False
        try:
            dim_one = (100,)
            rl = RLBase(dim_one)
        except:
            raised = True
        with self.subTest():
            self.assertFalse(raised)
        with self.subTest():
            self.assertEqual(rl.all_states.shape, (0, 100))
        with self.subTest():
            self.assertEqual(rl.all_actions.shape, (0,))
        with self.subTest():
            self.assertEqual(rl.all_rewards.shape, (0,))
        with self.subTest():
            self.assertEqual(rl.all_discounted_rewards.shape, (0,))

        try:
            rl.pre()
            state = np.ones(dim_one)
            for i in range(3):
                rl.decide(state=state, reward=-1)
                rl.store_action(-1)
            rl.post()
        except:
            raised = True
        with self.subTest():
            self.assertFalse(raised)
        with self.subTest():
            self.assertEqual(rl.all_states.shape, (2,100))
        with self.subTest():
            self.assertEqual(rl.all_actions.shape, (2,))
        with self.subTest():
            self.assertEqual(rl.all_rewards.shape, (2,))
        with self.subTest():
            self.assertEqual(rl.all_discounted_rewards.shape, (2,))

    def test_RLBase_dim_two(self):
        # test RLBase class can be created using one dimentional tuple
        raised = False
        try:
            dim_two = (5,20)
            rl = RLBase(dim_two)
        except:
            raised = True
        with self.subTest():
            self.assertFalse(raised)
        with self.subTest():
            self.assertEqual(rl.all_states.shape, (0,5,20))
        with self.subTest():
            self.assertEqual(rl.all_actions.shape, (0,))
        with self.subTest():
            self.assertEqual(rl.all_rewards.shape, (0,))
        with self.subTest():
            self.assertEqual(rl.all_discounted_rewards.shape, (0,))

        try:
            rl.pre()
            state = np.ones(dim_two)
            for i in range(3):
                rl.decide(state=state, reward=-1)
                rl.store_action(-1)
            rl.post()
        except:
            raised = True
        with self.subTest():
            self.assertFalse(raised)
        with self.subTest():
            self.assertEqual(rl.all_states.shape, (2,5,20))
        with self.subTest():
            self.assertEqual(rl.all_actions.shape, (2,))
        with self.subTest():
            self.assertEqual(rl.all_rewards.shape, (2,))
        with self.subTest():
            self.assertEqual(rl.all_discounted_rewards.shape, (2,))

class TestRLStateAction(unittest.TestCase):

    def test_RLBase_dim_one(self):
        raised = False
        try:
            model_param = { 'method':'nn', 'layers':[10,5] }
            rl = RLStateAction((100, ), model_param, model_param)
        except:
            raised = True
        self.assertFalse(raised)

    def test_RLBase_dim_two(self):
        raised = False
        try:
            model_param = { 'method':'nn', 'layers':[10,5] }
            rl = RLStateAction((5, 20), model_param, model_param)
        except:
            raised = True
        self.assertFalse(raised)

if __name__ == '__main__':
    unittest.main()
