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

class WidowX200EnvJoint(gym.Env):
    def __init__(self, use_rgb=True):
        #Normalized action space
        self.action_space = spaces.Box(low=np.array([-0.5, -0.25, -0.25, -0.25, -0.5, -1.0 / 3]),
                                       high=np.array([0.5, 0.25, 0.25, 0.25, 0.5, 1.8 / 3]), dtype=np.float32)

        self.observation_space = spaces.Box(low=np.array([-3.0, -3.0, -3.0, -3.0, -3.9, -3.0]),
                                      high=np.array([3.0, 3.0, 3.0, 3.0, 3.0, 3.0]), dtype=np.float32)

        self.obs_mode = 'verbose'   #CHANGE
        self.goal = None          #CHANGE
        self.use_rgb = use_rgb



    def set_goal(self, goal):
        self.goal = goal


    def reset(self, gripper = True):
        while True:
            try:
                self.get_observation_publisher.publish("GET_OBSERVATION")
                self.current_pos = np.array(rospy.wait_for_message(
                "/widowx_env/action/observation", numpy_msg(Floats), timeout=5).data)
                break
            except:
                continue
        self.move_to_neutral()
        self.reset_publisher.publish("FAR_POSITION NO_GRIPPER")
        rospy.sleep(1.0)
        while True:
            try:
                self.get_observation_publisher.publish("GET_OBSERVATION")
                self.current_pos = np.array(rospy.wait_for_message(
                "/widowx_env/action/observation", numpy_msg(Floats), timeout=5).data)
                break
            except:
                continue
        if gripper:
            self.open_gripper()
        return self._get_obs()


    def open_gripper(self):
        while self.current_pos[8] < 1.2:
            self.gripper_publisher.publish("OPEN")
            rospy.sleep(1)
            try:
                self.get_observation_publisher.publish("GET_OBSERVATION")
                self.current_pos = np.array(rospy.wait_for_message(
                "/widowx_env/action/observation", numpy_msg(Floats), timeout=5).data)
                self._is_gripper_open = True
            except:
                continue

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

        if self.use_rgb:
            obs['image'] = utils.get_image(64, 64   )
        #np.append(self._get_rgb(), self.original_image, axis=2)
        obs['state'] =  self.current_pos[3:9]
        return obs


    def _get_reward(self):
        return 0


    def check_if_object_grasped_gripper(self):
        self.step([0, 0, 0, 0, 0, -0.3])
        if self.current_pos[8] > -0.9:
            return True
        return False


    def _start_rospy(self, ):
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
