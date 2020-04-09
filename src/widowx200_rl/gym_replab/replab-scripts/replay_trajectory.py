import os
import pickle as pkl
import gym
import gym_replab
from widowx200_core.ik import InverseKinematics
import numpy as np
import time
from PIL import Image


def read_data(data_file):
    pool = gym_replab.utils.DemoPool()
    with open(data_file, 'rb') as fp:
        data = pkl.load(fp)
    return data['actions']

actions = read_data('/home/jonathan/Desktop/Projects/WidowX200_RL/src/widowx200_rl/gym_replab/data/WidowX200GraspNewXYZCombined/combined_training_pool.pkl')


env = gym.make('widowx200-v0')._start_rospy()
ik = InverseKinematics()
env.reset()
low_clip = env.action_space.low[:5]
high_clip = env.action_space.high[:5]
quat = ik.get_cartesian_pose()[3:]

for i in range(40):
    diff = actions[i][:3]
    a = gym_replab.utils.compute_ik_command(diff, low_clip, high_clip, quat, ik)
    env.step(np.append(a, actions[i][3]))
