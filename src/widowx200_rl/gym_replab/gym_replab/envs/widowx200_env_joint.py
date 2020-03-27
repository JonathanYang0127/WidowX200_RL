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


class WidowX200EnvJoint(gym.Env):
    def __init__(self):
        #Normalized action space
        self.action_space = spaces.Box(low=np.array([-0.5, -0.25, -0.25, -0.25, -0.5, -1.0 / 3]),
                                       high=np.array([0.5, 0.25, 0.25, 0.25, 0.5, 1.8 / 3]), dtype=np.float32)

        self.obs_mode = 'verbose'   #CHANGE
        self.goal = None          #CHANGE


    def set_goal(self, goal):
        self.goal = goal


    def reset(self, gripper = True):
        if gripper:
            self.reset_publisher.publish("OPEN_GRIPPER")
        else:
            self.reset_publisher.publish("NO_GRIPPER")
        rospy.sleep(3.0)
        self.get_observation_publisher.publish("GET_OBSERVATION")
        self.current_pos = np.array(rospy.wait_for_message(
            "/widowx_env/action/observation", numpy_msg(Floats)).data)
        return self._get_obs()


    def move_to_neutral(self):
        self.neutral_publisher.publish("MOVE_TO_NEUTRAL")
        rospy.sleep(1.0)


    def step(self, action):
        '''
        TODO: Get action bounds and enforce them
        '''
        action = np.array(action, dtype='float32')
        action = np.clip(np.array(action, dtype=np.float32), self.action_space.low, self.action_space.high)
        self.action_publisher.publish(action)
        self.current_pos = np.array(rospy.wait_for_message(
            "/widowx_env/action/observation", numpy_msg(Floats)).data)
        return self._generate_step_tuple()


    def _generate_step_tuple(self):
        reward = self._get_reward()
        episode_over = False
        info = {}

        return self._get_obs(), reward, episode_over, info


    def _get_obs(self):
        '''
        TODO: Set image obs
        '''
        #assert self.original_image is not None
        obs = {}

        if self.obs_mode == 'verbose':
            obs['observation'] = self.current_pos[:3]
            obs['joints'] = self.current_pos[3:9]
            obs['desired_goal'] = self.goal
            obs['achieved_goal'] = self.current_pos[:3]
            obs['gripper'] = self.current_pos[8]

        obs['image'] = None #np.append(self._get_rgb(), self.original_image, axis=2)
        obs['state'] =  self.current_pos[3:9]
        return obs


    def _get_reward(self):
        return 0


    def check_if_object_grasped_gripper(self):
        self.step([0, 0, 0, 0, 0, -0.3])
        if self.current_pos[8] > -0.9:
            return True
        return False


    def _start_rospy(self):
        rospy.init_node("WidowX200_Env")
        self.reset_publisher = rospy.Publisher(
            "/widowx_env/reset", String, queue_size=1)
        self.action_publisher = rospy.Publisher(
            "/widowx_env/action", numpy_msg(Floats), queue_size=1)
        self.neutral_publisher = rospy.Publisher(
            "/widowx_env/neutral", String, queue_size=1)
        self.get_observation_publisher = rospy.Publisher(
            "/widowx_env/get_observation", String, queue_size=1)
        rospy.sleep(2.0)

        return self
