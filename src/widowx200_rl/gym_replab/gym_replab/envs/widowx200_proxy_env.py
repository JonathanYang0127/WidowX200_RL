import gym
from gym import error, spaces, utils
from gym.utils import seeding

import os
import numpy as np

import rospy
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
from std_msgs.msg import String

import random
from .. import utils

class WidowX200ProxyEnv(gym.Env):
    def __init__(self):
        #Normalized action space
        self.action_space = spaces.Box(low=np.array([-0.5, -0.25, -0.25, -0.25, -0.5, -1.0 / 3]),
                                       high=np.array([0.5, 0.25, 0.25, 0.25, 0.5, 1.8 / 3]), dtype=np.float32)

        self.observation_space = spaces.Box(low=np.array([-3.0, -3.0, -3.0, -3.0, -3.9, -3.0]),
                                      high=np.array([3.0, 3.0, 3.0, 3.0, 3.0, 3.0]), dtype=np.float32)

        self.obs_mode = 'verbose'   #CHANGE
        self.goal = None          #CHANGE


    def set_goal(self, goal):
        pass

    def reset(self, gripper = True):
        pass

    def move_to_neutral(self):
        pass


    def step(self, action):
        pass


    def _generate_step_tuple(self):
        pass


    def _get_obs(self):
        pass


    def _get_reward(self):
        return 0


    def check_if_object_grasped_gripper(self):
        pass


    def _start_rospy(self):
        pass
