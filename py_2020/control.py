
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
        pass

    def decide(self, line_pos):
        raise NotImplementedError()