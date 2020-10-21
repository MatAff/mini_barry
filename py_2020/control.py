
import numpy as np
import scipy.stats

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
    def discount_rewards(rewards, discount=0.05):
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

        print(X.shape)
        print(y.shape)

        # create model
        self.model = NeuralNet()
        self.model.create(X.shape, [10,10,5])
        self.model.train(X, y)

        # review training history
        # self.model.review_history() # TODO: figure out how to get this to work
  
    def use_model(self, line_pos):

        def pred(x, mu, sd):
            p = self.model.predict(np.array([np.append(line_pos, [0.2, x])]))
            prob = scipy.stats.norm(mu, sd).pdf(x)
            return p / prob

        mu = self.action.mean(axis=0)
        sd = self.action.std(axis=0)

        rotate_range = np.arange(-0.5, 0.5, 0.05)
        props = [pred(r, mu[1], sd[1]) for r in rotate_range]

        return rotate_range[np.argmin(props)]

    def decide(self, line_pos, verbose=False):

        # compute reward
        if line_pos[0] is not None:
            reward = abs(line_pos[0])
        else:
            reward = 10

        # retainer
        line_pos = self.ret.retain(np.array(line_pos)) # insert retained values

        # decide
        if self.model is None:
            act_dict =  self.initial_controller.decide(line_pos)
        else:
            if np.random.rand() < (self.cycle / 1000):
                res = self.use_model(line_pos)
                act_dict = {'forward': 0.2, 'rotate': res}
            else:
                act_dict =  self.initial_controller.decide(line_pos)

        # store state, reward, and action
        self.state = np.append(self.state, [line_pos], axis=0)
        self.reward = np.append(self.reward, reward)
        action = [act_dict['forward'], act_dict['rotate']]
        self.action = np.append(self.action, [action], axis=0)
        
        # update count and cycle
        self.count += 1
        if self.count % self.cycle_size == 0:
            self.cycle += 1

            print(self.state.shape)
            print(self.reward.shape)
            print(self.action.shape)

            self.create_model()

        return act_dict
