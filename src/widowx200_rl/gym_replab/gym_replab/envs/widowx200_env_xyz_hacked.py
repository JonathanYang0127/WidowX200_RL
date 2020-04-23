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

class WidowX200EnvXYZHacked(gym.Env):
    def __init__(self, obs_mode='verbose', reward_type='sparse', transpose_image = False):
        #Normalized action space
        self.action_space = spaces.Box(low=np.array([-0.5, -0.25, -0.25, -0.25, -0.5]),
                                       high=np.array([0.5, 0.25, 0.25, 0.25, 0.5]), dtype=np.float32)

        self.observation_space = spaces.Box(low=np.array([-3.0, -3.0, -3.0, -3.0, -3.9, -3.0]),
                                      high=np.array([3.0, 3.0, 3.0, 3.0, 3.0, 3.0]), dtype=np.float32)

        self._safety_box = spaces.Box(low=np.array([0.11, -0.22, 0.065]),
                                      high=np.array([0.33, 0.13, 0.2]), dtype=np.float32)

        self._obs_mode = obs_mode
        self._reward_type = reward_type
        self._transpose_image = transpose_image

        self._image_puller = utils.USBImagePuller()
        self.depth_image_service = None
        
        self.goal = None
        self.ik = InverseKinematics()
        self.quat = np.array([0.5, 0.5, -0.5, 0.5], dtype=np.float32)


    def set_goal(self, goal):
        self.goal = goal


    def drop_at_random_location(self):
        goal = np.array([0, 0, 0], dtype = 'float32')
        goal[0] = np.random.uniform(low=0.18, high=0.30)
        goal[1] = np.random.uniform(low=-0.17, high=0.13)
        goal[2] = 0.07
        ik_command = self.ik._calculate_ik(goal, self.quat)[0][:5]
        self.joint_publisher.publish(np.array(ik_command, dtype='float32'))
        self.current_pos = np.array(rospy.wait_for_message(
            "/widowx_env/action/observation", numpy_msg(Floats)).data)
        rospy.sleep(1)
        action = np.array([0, 0, 0, 0, 0, 0.6], dtype='float32')
        self.action_publisher.publish(action)
        self.current_pos = np.array(rospy.wait_for_message(
            "/widowx_env/action/observation", numpy_msg(Floats)).data)
        rospy.sleep(1)


    def reset(self, gripper = True, drop=True):
        self.move_to_neutral()
        if drop and utils.check_if_object_grasped(self.depth_image_service):
            self.drop_at_random_location()
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
        action: [x, y, z]
        '''
        action = np.array(np.copy(action), dtype='float32') / 5
        pos = self.ik.get_cartesian_pose()[:3]
        pos += action
        pos = np.clip(np.array(pos, dtype=np.float32), self._safety_box.low, self._safety_box.high)
        action = utils.compute_ik_solution(pos, self.quat, self.action_space.low, self.action_space.high, self.ik)

        if self.current_pos is not None and self.current_pos[2] < 0.067:
            action = np.append(action, np.array([[-0.3]], dtype='float32'))
        else:
            action = np.append(action, np.array([[0.6]], dtype='float32'))

        self.action_publisher.publish(action)
        self.current_pos = np.array(rospy.wait_for_message(
            "/widowx_env/action/observation", numpy_msg(Floats)).data)
        rospy.sleep(0.1)
        return self._generate_step_tuple()


    def lift_object(self):
        #while self.current_pos[2] < 0.10:
        print(self.current_pos[8])
        print('***********************"HI" *******************************')
        while self.current_pos[8] > 0.1:
            self.action_publisher.publish(np.append(np.zeros(5, dtype='float32'), np.array([[-0.3]], dtype='float32')))
            self.current_pos = np.array(rospy.wait_for_message(
                "/widowx_env/action/observation", numpy_msg(Floats)).data)
        rospy.sleep(0.5)
        self.move_to_neutral()


    def _generate_step_tuple(self):
        episode_over = self.current_pos is not None and self.current_pos[2] < 0.067
        info = {}
        if episode_over:
            self.lift_object()

        reward = self._get_reward(episode_over)

        return self._get_obs(), reward, episode_over, info


    def pull_image(self):
        img = utils.process_image_rgb(self._image_puller.pull_image(), 64, 64)
        if self._transpose_image:
            img = np.transpose(img, (2, 0, 1))
        return img


    def _get_obs(self):
        '''
        TODO: Set image obs
        '''
        #assert self.original_image is not None
        obs = {}

        if self._obs_mode == 'verbose':
            obs['observation'] = self.current_pos[:3]
            obs['joints'] = self.current_pos[3:9]
            obs['desired_goal'] = self.goal
            obs['achieved_goal'] = self.current_pos[:3]
            obs['gripper'] = self.current_pos[8]
            obs['image'] = self.pull_image()
            obs['state'] =  self.current_pos[3:9]
        elif self._obs_mode == 'pixel_state':
            obs['image'] = self.pull_image()
            obs['state'] =  self.current_pos[3:9]
        elif self._obs_mode == 'pixels':
            obs['image'] = self.pull_image()

        return obs



    def _get_reward(self, episode_over):
        if self._reward_type == 'sparse':
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
        self.joint_publisher = rospy.Publisher(
            "/widowx_env/joint/command", numpy_msg(Floats), queue_size=1)
        self.neutral_publisher = rospy.Publisher(
            "/widowx_env/neutral", String, queue_size=1)
        self.get_observation_publisher = rospy.Publisher(
            "/widowx_env/get_observation", String, queue_size=1)
        rospy.sleep(2.0)

        #NOTE: ROS node must be initialized before depth image service is created
        self.depth_image_service = utils.KinectImageService('sd_pts')

        return self
