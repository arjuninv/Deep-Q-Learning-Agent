import numpy as np

from envs.rover_lander_1 import rover_lander_1

MAX_EPISODES = 5_000

SHOW_PREVIEW = True
AGGREGATE_STATS_EVERY = 10

epsilon = 0.98


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
    
agent = Agent()
    
for episode in tqdm(range(0, MAX_EPISODES), ascii=True, unit='episodes'):
    episode_reward = 0
    step = 1
    current_state = env.reset()
    done = False
    while not done:
        if np.random.random() > epsilon:
            action = np.argmax(agent.get_qs(current_state))
        else:
            action = env.random_action_sample()
            
    new_state, reward, done = env.step(action)
    episode_reward += reward
    
    if SHOW_PREVIEW and not episode % AGGREGATE_STATS_EVERY:
            env.render()