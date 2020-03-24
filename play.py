import argparse

import tensorflow as tf
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--model", help="Path to model to be used by the agent")
parser.add_argument("--fps", help="Frames per second")
args = parser.parse_args()

model_path = args.model
fps = args.fps

from envs.rover_lander_1 import rover_lander_1


class Agent:
    def __init__(self, model_path):
        self.model = self.load_model(model_path)
    
    def load_model(self, model_path):
        return tf.keras.models.load_model(model_path)
    
    def qs(self, state):
        return np.argmax(self.model.predict(np.array(state)/255))[0]
    
    
if __name__ == '__main__':
    agent = Agent(model_path)
    env = rover_lander_1()
    
    state = env.reset()
    while True:
        time.sleep(1/fps)
        env.render()
        action = agent.get_qs(state)
        state, reward, done = env.step(action)
        
        if done:
            break
        