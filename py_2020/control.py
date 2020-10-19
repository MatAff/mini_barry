
import numpy as np

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

    def __init__(self):

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

    def decide(self, line_pos):

        # compute cost
        # TODO: create and implement cost function

        # store state and cost
        self.state = np.append(self.state, [line_pos], axis=0)
        
        # TODO: implement storing reward and action

        # update count and cycle
        self.count += 1
        if self.count % self.cycle_size == 0:
            self.cycle += 1

            model = None # TODO: implement training model

        # decide
        if self.model is None:
            act_dict =  self.initial_controller.decide(line_pos)
        else:
            res = model.predict(line_pos)
            act_dict = {'forward': res[0], 'rotatae': res[1]}

        # store action
        # TODO: implement storing action

        return act_dict
