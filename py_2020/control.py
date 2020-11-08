
import copy
import matplotlib.pyplot as plt
import numpy as np
from queue import Queue
import scipy.stats
import threading

from modeling import NeuralNet


class Retainer(object):

    def __init__(self, data):
        self.prev = data

    def retain(self, current):
        current = current.astype('float')
        current[np.isnan(current)] = self.prev[np.isnan(current)]
        self.prev = current
        return(current)


class EngineeredControl(object):
    
    def __init__(self):
        pass

    def decide(self, line_pos):
        try:
            rotate = line_pos[4] * 3.0
            return {'forward': 0.6, 'rotate': rotate}
        except TypeError as e:
            print(e)
            return {'forward': 0.6, 'rotate': 0.0}


class TestDrive(object):

    def __init__(self):
        self.count = 0

    def decide(self, line_pos):
        if self.count > 15:
            self.count = 0
        self.count += 1
        if self.count < 10:
            return {'forward': 0.6, 'rotate': 0.0}
        else:
            return {'forward': 0.6, 'rotate': 0.9}
    

class RL(object):

    def __init__(self, l):

        # cycle settings
        self.count = 0
        self.cycle = 0
        self.cycle_size = 200

        # initial controller
        self.initial_controller = EngineeredControl()

        # store
        self.state = np.empty((0,5)) # should match len(line_pos)
        self.reward = np.empty((0))
        self.action = np.empty((0,2))

        # model
        self.model = None

        # retainer
        self.ret = Retainer(np.zeros(l)) 

        # queue
        self.que = Queue()

    @staticmethod
    def discount_rewards(rewards, discount=0.5):
        running_reward = 0.0
        discounted_rewards = np.array([], 'float')
        for i in reversed(range(rewards.shape[0])):
            discounted_rewards = np.concatenate(([running_reward], discounted_rewards))
            running_reward = running_reward * discount + rewards[i] * (1 - discount)
        return discounted_rewards

    @staticmethod
    def thread_train_model(X, y):
        model = NeuralNet()
        model.create(X.shape, [20, 20, 20, 20, 2])
        print(X.shape)
        model.train(X, y)
        return model

    def create_model(self):

        # compute discounted rewards
        self.discounted_rewards = RL.discount_rewards(self.reward, 0.5)

        # compile data
        X = np.append(self.state, self.action, axis=1)
        y = self.discounted_rewards

        # # train not on thread
        # model = RL.thread_train_model(X, y)
        # self.que.put(model)

        # train on thread
        t = threading.Thread(target=lambda q, X, y: q.put(RL.thread_train_model(X, y)), args=(self.que, X, y))
        t.start()

        # review training history
        # self.model.review_history() # TODO: figure out how to get this to work
  
    def use_model(self, line_pos):

        mu = self.action.mean(axis=0)[1]
        sd = self.action.std(axis=0)[1]

        line_pos = np.append(line_pos, [0.2])
        rotate_range = np.arange(-0.05, 0.05, 0.001)
        res = np.repeat([line_pos], len(rotate_range), axis=0)
        res = np.append(res, np.array([rotate_range]).T, axis=1)

        pred = self.model.predict(res)
        if np.random.rand() < 0.1:
            plt.plot(pred)
            plt.show()
        prob = scipy.stats.norm(mu, sd).pdf(rotate_range)

        props = pred # / (prob**1/10)

        return rotate_range[np.argmin(props)]

    def compute_reward(self, line_pos, retained_pos):

        reward = 0 
        for pos in range(len(line_pos)):
            if line_pos[pos] is None:
                pos_reward = 1
            else:
                pos_reward = abs(line_pos[pos])
            reward += pos_reward**(1/(pos + 1))

        return reward

    def decide(self, line_pos, verbose=False):

        # retainer
        retained_pos = self.ret.retain(np.array(line_pos)) # insert retained values

        # compute reward
        reward = self.compute_reward(line_pos, retained_pos)

        # decide
        if self.model is None:
            act_dict =  self.initial_controller.decide(retained_pos)
        else:
            if np.random.rand() < (self.cycle / 10):
                res = self.use_model(retained_pos)
                act_dict = {'forward': 0.5, 'rotate': res}
            else:
                act_dict =  self.initial_controller.decide(retained_pos)

        # store state, reward, and action
        self.state = np.append(self.state, [retained_pos], axis=0)
        self.reward = np.append(self.reward, reward)
        action = [act_dict['forward'], act_dict['rotate']]
        self.action = np.append(self.action, [action], axis=0)
        
        # update count and cycle
        self.count += 1
        if self.count % self.cycle_size == 0:
            self.cycle += 1
            self.create_model()

        # check queue for models
        if not self.que.empty():
            self.model = self.que.get()
            # self.model.model._make_predict_function()

        return act_dict
