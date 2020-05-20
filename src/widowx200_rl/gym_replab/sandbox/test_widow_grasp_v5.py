import gym
import gym_replab
from widowx200_core.ik import InverseKinematics
import numpy as np
import time
import argparse
import os
import sys
from PIL import Image


ik = InverseKinematics()
env = gym.make('widow200graspv5-v0')._start_rospy()
env.reset()


depth_image_service = env.depth_image_service
rgb_image_service = gym_replab.utils.KinectImageService('rgb')

for i in range(6):
    next_obs, reward, done, info = env.step([1, 0, -1, 0, 0, 0])
    if done:
        break

for i in range(10):
    next_obs, reward, done, info = env.step([1, 0, 1, 0, -1, 0])
    print(next_obs['observation'][2])

env.step([1, 0, 1, 0, -1, 1])
