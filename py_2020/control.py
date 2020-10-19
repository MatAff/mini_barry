
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
        pass

    def decide(self, line_pos):
        raise NotImplementedError()


class RL(object):

    def __init__(self):
        pass

    def decide(self, line_pos):
        raise NotImplementedError()