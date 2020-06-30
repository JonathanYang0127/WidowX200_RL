import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym.spaces import Dict

import os
import numpy as np

import sys


import random


REWARD_FAIL = 0.0
REWARD_SUCCESS = 1.0


class Widow200GraspV6ProxyEnv(gym.Env):
    def __init__(self, observation_mode='verbose', reward_type='sparse', grasp_detector='background_subtraction', transpose_image = False):
        #Normalized action space
        self.action_space = spaces.Box(low=np.array([-1, -1, -1, -0.5, -1]),
                                       high=np.array([1, 1, 1, 0.5, 1]), dtype=np.float32)

        self.joint_space = spaces.Box(low=np.array([-0.5, -0.25, -0.25, -0.25, -0.5]),
                                       high=np.array([0.5, 0.25, 0.25, 0.25, 0.5]), dtype=np.float32)

        self._safety_box = spaces.Box(low=np.array([0.12, -0.22, 0.064]),
                                      high=np.array([0.37, 0.14, 0.2]), dtype=np.float32)

        self.image_shape = (64, 64)
        self.observation_space = Dict({'state': spaces.Box(low=np.array([-1, -1, -1, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0]),
                                      high=np.array([1, 1, 1, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0]), dtype=np.float32),
                                      'image': spaces.Box(low=np.array([0]*self.image_shape[0]*self.image_shape[1]*3),
                                            high=np.array([255]*self.image_shape[0]*self.image_shape[1]*3), dtype=np.float32)})

        self._obs_mode = observation_mode
        self._reward_type = reward_type
        self._grasp_detector = grasp_detector
        self._transpose_image = transpose_image

        self.depth_image_service = None

        self.goal = None
        self.quat = np.array([0.5, 0.5, -0.5, 0.5], dtype=np.float32)

        self._is_gripper_open = True
        self._upwards_bias = 0.03

        self._gripper_closed = -0.3
        self._gripper_open = 0.6
        self.reward_height_thresh = 0.14

        self.cnn_input_key = 'image'
        self.fc_input_key = 'state'


    def set_goal(self, goal):
        raise NotImplementedError

    def reset(self, gripper = True):
        raise NotImplementedError

    def move_to_neutral(self):
        raise NotImplementedError


    def step(self, action):
        raise NotImplementedError


    def _generate_step_tuple(self):
        raise NotImplementedError


    def _get_obs(self):
        raise NotImplementedError


    def _get_reward(self):
        raise NotImplementedError


    def check_if_object_grasped_gripper(self):
        raise NotImplementedError


    def _start_rospy(self):
        raise NotImplementedError
