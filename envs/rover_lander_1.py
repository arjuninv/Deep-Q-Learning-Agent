from envs.core import Env

class rover_lander_1(Env):
    def __init__(self):
        # Action Space
        #   0 - Do nothing
        #   1 - thruters left 
        #   2 - thruters down 
        #   3 - thruters right 
        self.action_space = [0, 1, 2, 3]
    
    def step(self):
        pass
     
    def render(self):
        pass
    
    def save_frame(self):
        pass
    
    def reset(self):
        pass
    
    def step(self):
        pass