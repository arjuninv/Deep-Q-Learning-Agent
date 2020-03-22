class Env:
    def __init__(self):
        self.action_space = None
        self.observation_space = None
        
    def step(self):
        raise NotImplementedError
    
    def render(self):
        raise NotImplementedError
    
    def save_frame(self):
        raise NotImplementedError
    
    def reset(self):
        raise NotImplementedError
    
    def step(self):
        raise NotImplementedError
    
    def __repr__(self):
        return '<{} env>'.format(type(self).__name__)
    

if __name__ == '__main__':
    pass