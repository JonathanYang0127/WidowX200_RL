import gym
import gym_replab
import numpy as np
from PIL import Image

images = []
env = gym.make('Widow200RealRobotGraspV6-v0', observation_mode='verbose', reward_type='sparse', \
    grasp_detector='background_subtraction', transpose_image=True)._start_rospy()
obs = env.reset()

for i in range(10):
    print(i)
    env.step([1, 0, 0, 0, 0])
