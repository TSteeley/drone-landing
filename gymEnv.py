import gymnasium as gym
import numpy as np
from typing import Union
from gymnasium import spaces
from brains import player
from gameState import gameState
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import A2C, PPO
from stable_baselines3.ppo import policies
from stable_baselines3.common.type_aliases import Schedule
# from stable_baselines3.common.

class droneLanding(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, player= player()):
        super(droneLanding, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Box(low = 0, high = 1, shape=(2,))
        # Example for using image as input:
        self.observation_space = spaces.Box(low=-2**63, high = 2**62,shape=(10,))
        self.player = player
        self.state = gameState((1280, 720), player)

    def step(self, action):
        self.player.engines.set_Throttle(action)
        self.player.physics_update(self.state.dt)
        self.player.env_update(self.state)
        terminated = self.state.update(self.player)
        return np.array(self.player.observations, dtype="float32"), self.state.dScore, terminated, False, {}


    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.state.reset()
        self.player.reset()
        self.player.env_update(self.state)
        return np.array(self.player.observations, dtype="float32"), {}

    # def render(self, mode='human'):
    #     ...

    # def close (self):
    #     ...
        
if __name__ == '__main__':
    env = droneLanding()
    check_env(env)
    print('Environment created succesfully')
        
    
