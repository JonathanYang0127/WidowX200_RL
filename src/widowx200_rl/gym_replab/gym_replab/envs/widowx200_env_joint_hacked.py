import gym
from gym import error, spaces, utils
from gym.utils import seeding

import os
import numpy as np

import rospy
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
from std_msgs.msg import String
from widowx200_core.ik import InverseKinematics


import random
from .. import utils


REWARD_NEGATIVE = -1.0
REWARD_POSITIVE = 10.0

class WidowX200EnvJointHacked(gym.Env):
    def __init__(self, obs_mode='verbose'):
        #Normalized action space
        self.action_space = spaces.Box(low=np.array([-0.5, -0.25, -0.25, -0.25, -0.5]),
                                       high=np.array([0.5, 0.25, 0.25, 0.25, 0.5]), dtype=np.float32)

        self.observation_space = spaces.Box(low=np.array([-3.0, -3.0, -3.0, -3.0, -3.9, -3.0]),
                                      high=np.array([3.0, 3.0, 3.0, 3.0, 3.0, 3.0]), dtype=np.float32)

        self.safety_box = spaces.Box(low=np.array([0.11, -0.22, 0.065]),
                                      high=np.array([0.33, 0.13, 0.2]), dtype=np.float32)
        self.obs_mode = obs_mode   #CHANGE
        self.goal = None          #CHANGE
        self._image_puller = utils.USBImagePuller()
        self.depth_image_service = None
        self.ik = InverseKinematics()


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
        TODO: Enforce safety box
        '''
        action = np.array(np.copy(action), dtype='float32')
        action = np.clip(np.array(action, dtype=np.float32), self.action_space.low, self.action_space.high)

        if self.current_pos is not None and self.current_pos[2] < 0.067:
            action = np.append(action, np.array([[-0.3]], dtype='float32'))
        else:
            action = np.append(action, np.array([[0.6]], dtype='float32'))

        self.action_publisher.publish(action)
        self.current_pos = np.array(rospy.wait_for_message(
            "/widowx_env/action/observation", numpy_msg(Floats)).data)

        return self._generate_step_tuple()


    def lift_object(self):
        #while self.current_pos[2] < 0.10:
        print(self.current_pos[8])
        print('***********************"HI" *******************************')
        while self.current_pos[8] > 0.1:
            self.action_publisher.publish(np.append(np.zeros(5, dtype='float32'), np.array([[-0.3]], dtype='float32')))
            self.current_pos = np.array(rospy.wait_for_message(
                "/widowx_env/action/observation", numpy_msg(Floats)).data)
            print("ASDASDASDA")
        rospy.sleep(0.5)
        self.move_to_neutral()


    def _generate_step_tuple(self):
        episode_over = self.current_pos is not None and self.current_pos[2] < 0.067
        info = {}
        if episode_over:
            self.lift_object()

        reward = self._get_reward(episode_over)


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
            obs['image'] = utils.process_image_rgb(self._image_puller.pull_image(), 64, 64)
            obs['state'] =  self.current_pos[3:9]
        elif self.obs_mode == 'pixel_state':
            obs['image'] = utils.process_image_rgb(self._image_puller.pull_image(), 64, 64)
            obs['state'] =  self.current_pos[3:9]
        elif self.obs_mode == 'pixels':
            obs['image'] = utils.process_image_rgb(self._image_puller.pull_image(), 64, 64)

        return obs


    def _get_reward(self, episode_over):
        if episode_over and utils.check_if_object_grasped(self.depth_image_service):
            print("Object grasp succeeded!!!")
            return REWARD_POSITIVE

        return REWARD_NEGATIVE


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

        #NOTE: ROS node must be initialized before depth image service is created
        self.depth_image_service = utils.KinectImageService('sd_pts')

        return self
