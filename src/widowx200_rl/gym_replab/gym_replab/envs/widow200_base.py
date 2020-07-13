import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym.spaces import Dict

import os
import numpy as np

import rospy
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
from std_msgs.msg import String
from widowx200_core.ik import InverseKinematics
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
sys.path.append('/opt/ros/kinetic/lib/python2.7/dist-packages')

import random
from .. import utils


class Widow200RealRobotBaseEnv(gym.Env):
    def __init__(self, observation_mode='verbose', grasp_detector='background_subtraction', transpose_image = False):
        self.joint_space = spaces.Box(low=np.array([-0.6, -0.6, -0.6, -0.6, -0.6]),
                                       high=np.array([0.6, 0.6, 0.6, 0.6, 0.6]), dtype=np.float32)

        self._safety_box = spaces.Box(low=np.array([0.13, -0.26, 0.049]),
                                      high=np.array([0.4, 0.16, 0.2]), dtype=np.float32)

        self.image_shape = (64, 64)
        self.observation_space = Dict({'state': spaces.Box(low=np.array([-3.0, -3.0, -3.0, -3.0, -3.0, -3.0]),
                                      high=np.array([3.0, 3.0, 3.0, 3.0, 3.0, 3.0]), dtype=np.float32),
                                      'image': spaces.Box(low=np.array([0]*self.image_shape[0]*self.image_shape[1]*3),
                                            high=np.array([255]*self.image_shape[0]*self.image_shape[1]*3), dtype=np.float32)})

        self._set_action_space()

        self._obs_mode = observation_mode
        self._grasp_detector = grasp_detector
        self._transpose_image = transpose_image

        self.depth_image_service = None
        self.ik = InverseKinematics()


    def _set_action_space(self):
        raise NotImplementedError

    def get_reward(self):
        raise NotImplementedError


    def step(self, action):
        raise NotImplementedError


    def _generate_step_tuple(self, episode_over):
        raise NotImplementedError


    def reset(self, gripper = True):
        raise NotImplementedError


    def lift_object(self):
        lift_target = np.array([0.16, -0.04, self.reward_height_thresh + 0.04])
        moved = self.move_to_xyz(lift_target, wrist = self.current_pos[7], wait = 0.2)
        return moved


    def move_to_background_subtract(self):
        while True:
            try:
                self.joint_publisher.publish(np.array([1.61, -0.455, -0.333, -1.631, 1.62], dtype='float32'))
                self.current_pos = np.array(rospy.wait_for_message(
                    "/widowx_env/action/observation", numpy_msg(Floats), timeout=5).data)
                rospy.sleep(1.0)
                break
            except:
                continue


    def move_to_neutral(self):
        self.neutral_publisher.publish("MOVE_TO_NEUTRAL")
        rospy.sleep(1.0)


    def move_to_xyz(self, pos, wrist = None, wait = 1):
        ik_command = self.ik._calculate_ik(pos, self.quat)[0][:5]
        if wrist is not None:
            ik_command[4] = wrist
        try:
            self.joint_publisher.publish(np.array(ik_command, dtype='float32'))
            self.current_pos = np.array(rospy.wait_for_message(
                "/widowx_env/action/observation", numpy_msg(Floats), timeout=5).data)
            rospy.sleep(wait)
            return True
        except:
            return False


    def drop_at_random_location(self, reset=True):
        if reset:
            self.reset_publisher.publish("NO_GRIPPER")
            rospy.sleep(1.5)
        goal = np.array([0, 0, 0], dtype = 'float32')

        '''
        tmp = np.random.choice(2, 2)
        goals_0 = [[0.16, 0.20], [0.30, 0.34]]
        goals_1 = [[-0.22, -0.18], [0.09, 0.13]]
        if tmp[0] == 0:
            goal[0] = np.random.uniform(low=goals_0[tmp[1]][0], high=goals_0[tmp[1]][1])
            goal[1] = np.random.uniform(low=-0.22, high=0.13)
        else:
            goal[0] = np.random.uniform(low=0.16, high=0.34)
            goal[1] = np.random.uniform(low=goals_1[tmp[1]][0], high=goals_1[tmp[1]][1])
        '''
        goal[0] = np.random.uniform(low=0.16, high=0.34)
        goal[1] = np.random.uniform(low=-0.22, high=0.15) #(-0.18, 0.13)

        goal[2] = 0.14
        ik_command = self.ik._calculate_ik(goal, self.quat)[0][:5]
        while True:
            try:
                self.joint_publisher.publish(np.array(ik_command, dtype='float32'))
                self.current_pos = np.array(rospy.wait_for_message(
                    "/widowx_env/action/observation", numpy_msg(Floats), timeout=5).data)
                rospy.sleep(1)
                break
            except:
                continue
        self.open_gripper()


    def open_gripper(self):
        while self.current_pos[8] < 1.2:
            self.gripper_publisher.publish("OPEN")
            rospy.sleep(1)
            try:
                self.get_observation_publisher.publish("GET_OBSERVATION")
                self.current_pos = np.array(rospy.wait_for_message(
                "/widowx_env/action/observation", numpy_msg(Floats), timeout=5).data)
            except:
                continue


    def close_gripper(self):
        while self.current_pos[8] > 0.3:
            self.gripper_publisher.publish("CLOSE")
            rospy.sleep(1)
            try:
                self.get_observation_publisher.publish("GET_OBSERVATION")
                self.current_pos = np.array(rospy.wait_for_message(
                "/widowx_env/action/observation", numpy_msg(Floats), timeout=5).data)
            except:
                continue


    def pull_image(self):
        img = utils.get_image(*self.image_shape)
        if self._transpose_image:
            img = np.transpose(img, (2, 0, 1))
            img = np.float32(img.flatten())/255.0
        return img


    def render(self):
        return utils.get_image(*self.image_shape)


    def get_info(self):
        pass


    def _start_rospy(self):
        rospy.init_node("WidowX200_Env")
        self.reset_publisher = rospy.Publisher(
            "/widowx_env/reset", String, queue_size=1)
        self.action_publisher = rospy.Publisher(
            "/widowx_env/action", numpy_msg(Floats), queue_size=1)
        self.joint_publisher = rospy.Publisher(
            "/widowx_env/joint/command", numpy_msg(Floats), queue_size=1)
        self.gripper_publisher = rospy.Publisher(
            "/widowx_env/gripper/command", String, queue_size=1)
        self.neutral_publisher = rospy.Publisher(
            "/widowx_env/neutral", String, queue_size=1)
        self.get_observation_publisher = rospy.Publisher(
            "/widowx_env/get_observation", String, queue_size=1)
        rospy.sleep(2.0)

        #NOTE: ROS node must be initialized before depth image service is created
        self.depth_image_service = utils.KinectImageService('sd_pts')

        return self