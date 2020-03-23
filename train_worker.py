from envs.rover_lander_1 import rover_lander_1

import random
import datetime
import requests
from collections import deque
import numpy as np
import tqdm

import tensorflow as tf
from keras import Sequential
from keras.layers import Dense
from keras.optimizers import adam
from keras.activations import relu, linear

MASTER_ENDPOINT = "localhost:5000"
WORKER_NAME = ""
MAX_EPISODES = 5_000
SHOW_PREVIEW = True
AGGREGATE_STATS_EVERY = 10
REPLAY_MEMORY_SIZE = 1000000

TRAIN_PARAMS = {'learning_rate': 0.001}

Q_PARAMS = {'epsilon': 1.0,
            'gamma': 0.99,
            'epsilon_min': 0.01,
            'epsilon_decay': 0.996}


id = None

def connect():
    id = int(requests.get(MASTER_ENDPOINT + f"/master/connect?worker_name={WORKER_NAME}&max_episodes={MAX_EPISODES}&current_episode=0"))
    
def update(properties=[]):
    requests.get(MASTER_ENDPOINT + f"/master/update?id={id}" + "&".join(properties[0] + "=" + properties[1]))
    
def send_model(model_path):
    files = {'model': open(model_path,'rb')}
    r = requests.post(MASTER_ENDPOINT + f"/master/send_model?id={id}", files=files)
        
class customCallback(tf.keras.callbacks.Callback): 
    def on_epoch_end(self, epoch, logs={}): 
        update(("acc", logs.get('acc')),
                ("loss", logs.get('loss')),
                ("mse", logs.get('mse')),
                ("epocs", epoch))
                
    def on_train_end(self, logs=None):
        update(("last_trained", "curr_time"))
        
class Agent:
    def __init__(self):
        self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)
        self.model = self.build_model()
    
    def create_model(self):
        model = Sequential([Dense(150, input_dim=self.state_space, activation=relu),
                            Dense(120, activation=relu),
                            Dense(self.action_space, activation=linear)])
        model.compile(loss='mse', optimizer=adam(lr=TRAIN_PARAMS['learning_rate']))
        return model
    
    def save_model(self, local_only=True):
        self.model.save(f"models/{WORKER_NAME}.h5")
        if not local_only:
            send_model(f"models/{WORKER_NAME}.h5")
    
    def update_replay_memory(self, state, action, reward, next_state, done):
        self.replay_memory.append((state, action, reward, next_state, done))
    
    def replay(self):
        if len(self.replay_memory) < TRAIN_PARAMS['batch_size']:
            return
        
        minibatch = random.sample(self.replay_memory, TRAIN_PARAMS['batch_size'])
        states = np.array([i[0] for i in minibatch])
        actions = np.array([i[1] for i in minibatch])
        rewards = np.array([i[2] for i in minibatch])
        next_states = np.array([i[3] for i in minibatch])
        dones = np.array([i[4] for i in minibatch])
        
        states = np.squeeze(states)
        next_states = np.squeeze(next_states)
        
        targets = rewards + Q_PARAMS['gamma']*(np.amax(self.model.predict_on_batch(next_states), axis=1))*(1-dones)
        targets_full = self.model.predict_on_batch(states)
        ind = np.array([i for i in range(self.batch_size)])
        targets_full[[ind], [actions]] = targets

        self.model.fit(states, targets_full, epochs=1, verbose=0)
        if Q_PARAMS['epsilon'] > Q_PARAMS['epsilon_min']:
            Q_PARAMS['epsilon'] *= Q_PARAMS['epsilon_decay']


    def qs(self, state):
        return np.argmax(self.model.predict(np.array(state)/255))[0]
    
env = rover_lander_1()
agent = Agent()

episode_rewards = []
for episode in tqdm(range(0, MAX_EPISODES), ascii=True, unit='episodes'):
    episode_reward = 0
    step = 1
    current_state = env.reset()
    done = False
    while not done:
        if np.random.random() > agent.epsilon:
            action = np.argmax(agent.get_qs(current_state))
        else:
            action = env.random_action_sample()
            
        if SHOW_PREVIEW and not episode % AGGREGATE_STATS_EVERY:
                env.render()

        new_state, reward, done = env.step(action)
        episode_reward += reward
        
        agent.update_replay_memory(current_state, action, reward, new_state, done)
        current_state = new_state
        
        agent.replay()
        
    
    episode_rewards.append(episode_reward)
    update(("last_ep_score", episode_reward), ("avg_ep_score", sum(episode_rewards) / len(episode_rewards)))