from envs.rover_lander_1 import rover_lander_1

import argparse
import time
import tensorflow as tf
import numpy as np
import random

parser = argparse.ArgumentParser()
parser.add_argument("--model", help="Path to model to be used by the agent")
parser.add_argument("--fps", help="Frames per second", type=int, default=20)
args = parser.parse_args()

model_path = args.model
fps = args.fps


class Agent:
    def __init__(self, model_path=None):
        self.testing = (model_path == None)
        if not self.testing:
            self.model = self.load_model(model_path)
    
    def load_model(self, model_path):
        return tf.keras.models.load_model(model_path)
    
    def qs(self, state):
        if self.testing:
            return (random.randint(0, 4) - 1)
        return np.argmax(self.model.predict(np.array(state)/255))[0]
    
    
if __name__ == '__main__':
    agent = Agent(model_path)
    env = rover_lander_1()
    
    state = env.reset()
    while True:
        time.sleep(1/fps)
        env.render()
        action = agent.qs(state)
        state, reward, done = env.step(action)
        # print(reward, done)
        if done:
            break
        