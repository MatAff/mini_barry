
import numpy as np
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
            rotate = line_pos[3] * -0.45
            return {'forward': 0.5, 'rotate': rotate}
        except TypeError as e:
            print(e)
            return {'forward': 0.5, 'rotate': 0.0}


class TestDrive(object):

    def __init__(self):
        self.count = 0

    def decide(self, line_pos):
        if self.count > 25:
            self.count = 0
        self.count += 1
        if self.count < 20:
            return {'forward': 0.1, 'rotate': 0.0}
        else:
            return {'forward': 0.1, 'rotate': 0.2}
    

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

    @staticmethod
    def discount_rewards(rewards, discount=0.5):
        running_reward = 0.0
        discounted_rewards = np.array([], 'float')
        for i in reversed(range(rewards.shape[0])):
            discounted_rewards = np.concatenate(([running_reward], discounted_rewards))
            running_reward = running_reward * discount + rewards[i] * (1 - discount)
        return discounted_rewards

    def create_model(self):

        # compute discounted rewards
        self.discounted_rewards = RL.discount_rewards(self.reward)

        # compile data
        X = np.append(self.state, self.action, axis=1)
        y = self.discounted_rewards

        # print(X.shape)
        # print(y.shape)

        # create model
        self.model = NeuralNet()
        self.model.create(X.shape, [20,20,5])
        self.model.train(X, y)

        # review training history
        # self.model.review_history() # TODO: figure out how to get this to work
  
    def use_model(self, line_pos):

        mu = self.action.mean(axis=0)[1]
        sd = self.action.std(axis=0)[1]

        line_pos = np.append(line_pos, [0.2])
        rotate_range = np.arange(-0.05, 0.05, 0.01)
        res = np.repeat([line_pos], len(rotate_range), axis=0)
        res = np.append(res, np.array([rotate_range]).T, axis=1)

        pred = self.model.predict(res)
        prob = scipy.stats.norm(mu, sd).pdf(rotate_range)

        props = pred # / prob

        return rotate_range[np.argmin(props)]

    def compute_reward(self, line_pos, retained_pos):

        reward = 0 
        for pos in range(len(line_pos)):
            if line_pos[pos] is None:
                pos_reward = 10
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
            if np.random.rand() < (self.cycle / 3):
                res = self.use_model(retained_pos)
                act_dict = {'forward': 0.2, 'rotate': res}
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

            # print(self.state.shape)
            # print(self.reward.shape)
            # print(self.action.shape)

            self.create_model()

        return act_dict
