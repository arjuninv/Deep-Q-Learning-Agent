from envs.rover_lander_1 import rover_lander_1

MAX_EPISODES = 5_000

env = rover_lander_1()

class Agent:
    def __init__(self):
        pass
    
    def create_model(self):
        pass
    
    def update_replay_memory(self):
        pass
    
    def train(self):
        pass
    
    def qs(self):
        pass
    
for episode in tqdm(range(0, MAX_EPISODES), ascii=True, unit='episodes'):
    pass
