from envs.rover_lander_1 import rover_lander_1
import os
import random
import datetime
import requests
from collections import deque
import numpy as np
from tqdm.auto import tqdm

import tensorflow as tf
from tensorflow.keras import Sequential, layers, optimizers, activations

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--master-endpoint", help="Endpoint for train_master")
parser.add_argument("--worker-name", help="Worker name")
parser.add_argument("--show-preview", help="Show preview", action='store_true', default=False)
parser.add_argument("--mem-size", help="Replay memory size", type=int, default=1000000)
parser.add_argument("--max-ep", help="Maximum episodes", type=int, default=5000)
parser.add_argument("--lr", help="Learning rate", type=float, default=0.001)
parser.add_argument("--loss", help="Loss function", default="mse")
args = parser.parse_args()

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

MASTER_ENDPOINT = args.master_endpoint
WORKER_NAME = args.worker_name
MAX_EPISODES = args.max_ep
SHOW_PREVIEW = args.show_preview
REPLAY_MEMORY_SIZE = args.mem_size

RENDER_EVERY = 10
SAVE_MODEL_EVERY = 500
SAVE_MODEL_LOCAL_EVERY = 100

TRAIN_PARAMS = {'learning_rate':  args.lr,
                'loss':  args.loss,
                'batch_size': 64
                }

Q_PARAMS = {'epsilon': 1.0,
            'gamma': 0.99,
            'epsilon_min': 0.01,
            'epsilon_decay': 0.996}


id = None

def connect():
    global id
    id = int(requests.get(MASTER_ENDPOINT + f"/master/connect?worker_name={WORKER_NAME}&max_episodes={MAX_EPISODES}&current_episode=0").text)
    
def update(properties=[]):
    global id
    requests.get(MASTER_ENDPOINT + f"/master/update?id={str(id)}&" + "&".join([str(p[0]) + "=" + str(p[1]) for p in properties]))
    
def send_model(model_path):
    global id
    files = {'model': open(model_path,'rb')}
    r = requests.post(MASTER_ENDPOINT + f"/master/send_model?id={str(id)}", files=files)
        
class customCallback(tf.keras.callbacks.Callback): 
    def on_epoch_end(self, epoch, logs={}): 
        update([("acc", logs.get('acc')),
                ("loss", logs.get('loss')),
                ("mse", logs.get('mse'))])
                
    # def on_train_end(self, logs=None):
    #     update([("last_trained", "curr_time")])
        
class Agent:
    def __init__(self):
        self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)
        self.model = self.create_model()
    
    def create_model(self):
        model = Sequential([layers.Dense(150, input_dim=rover_lander_1.observation_space[0] * rover_lander_1.observation_space[1] * 3, activation=activations.relu),
                            layers.Dense(120, activation=activations.relu),
                            layers.Dense(rover_lander_1.action_space, activation=activations.linear)])
        model.compile(loss=TRAIN_PARAMS['loss'], optimizer=optimizers.Adam(lr=TRAIN_PARAMS['learning_rate']), metrics=['mse', 'acc'])
        return model
    
    def load_model(self, model_path):
        self.model = tf.keras.models.load_model(model_path)
    
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
        
        # states = np.squeeze(states, axis=0)
        # next_states = np.squeeze(next_states, axis=0)

        states = states.reshape(states.shape[0], np.prod(states.shape[1:]))/255
        next_states = next_states.reshape(next_states.shape[0], np.prod(next_states.shape[1:]))/255
        targets = rewards + Q_PARAMS['gamma']*(np.amax(self.model.predict_on_batch(next_states), axis=1))*(1-dones)
        targets_full = self.model.predict_on_batch(states)
        ind = np.array([i for i in range(TRAIN_PARAMS['batch_size'])])
        targets_full[[ind], [actions]] = targets

        self.model.fit(states, targets_full, epochs=1, verbose=0, callbacks=[customCallback()])
        if Q_PARAMS['epsilon'] > Q_PARAMS['epsilon_min']:
            Q_PARAMS['epsilon'] *= Q_PARAMS['epsilon_decay']


    def qs(self, state):
        state = state.reshape(1, np.prod(state.shape[:]))/255
        return np.argmax(self.model.predict(state))
        
if __name__ == '__main__':
    # if not SHOW_PREVIEW:
    #     os.environ["SDL_VIDEODRIVER"] = "dummy"
        
    env = rover_lander_1()
    agent = Agent()
    connect()
    episode_rewards = []
    for episode in tqdm(range(0, MAX_EPISODES), ascii=True, unit='episodes'):
        episode_reward = 0
        step = 1
        current_state = env.reset()
        done = False
        while not done:
            if np.random.random() > Q_PARAMS['epsilon']:
                action = agent.qs(current_state)
            else:
                action = env.random_action_sample()
                
            if SHOW_PREVIEW and not episode % RENDER_EVERY:
                    env.render()

            new_state, reward, done = env.step(action)
            episode_reward += reward
            
            agent.update_replay_memory(current_state, action, reward, new_state, done)
            current_state = new_state
            agent.replay()
            step = step + 1
            
                
        episode_rewards.append(episode_reward)
        update([("last_ep_score", episode_reward), 
            ("avg_ep_score", sum(episode_rewards) / len(episode_rewards)),
            ("num_step", step)])
        
        if not episode % SAVE_MODEL_EVERY:
            pass
            # agent.save_model(local_only=False)
            
        if not episode % SAVE_MODEL_LOCAL_EVERY:
            agent.save_model(local_only=True)