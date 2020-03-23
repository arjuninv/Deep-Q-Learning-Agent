import numpy as np
import requests
from collections import deque
from envs.rover_lander_1 import rover_lander_1
import tqdm

MASTER_ENDPOINT = "localhost:5000"
WORKER_NAME = ""
MAX_EPISODES = 5_000
SHOW_PREVIEW = True
AGGREGATE_STATS_EVERY = 10

id = None

def connect():
    id = int(requests.get(MASTER_ENDPOINT + f"/master/connect?worker_name={WORKER_NAME}&max_episodes={MAX_EPISODES}&current_episode=0"))
    
def update(properties=[]):
    requests.get(MASTER_ENDPOINT + f"/master/update?id={id}" + "&".join(properties[0] + "=" + properties[1]))
        

class Agent:
    def __init__(self):
        self.epsilon = 1.0
        self.epsilon_decay = .996
        self.memory = deque(maxlen=1000000)
        self.model = self.build_model()
    
    def create_model(self):
        pass
    
    def update_replay_memory(self):
        pass
    
    def train(self):
        pass
    
    def qs(self):
        pass
    
env = rover_lander_1()
agent = Agent()
    
for episode in tqdm(range(0, MAX_EPISODES), ascii=True, unit='episodes'):
    env.
    # episode_reward = 0
    # step = 1
    # current_state = env.reset()
    # done = False
    # while not done:
    #     if np.random.random() > agent.epsilon:
    #         action = np.argmax(agent.get_qs(current_state))
    #     else:
    #         action = env.random_action_sample()
            
    # new_state, reward, done = env.step(action)
    # episode_reward += reward
    
    # if SHOW_PREVIEW and not episode % AGGREGATE_STATS_EVERY:
    #         env.render()