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
import collections
from interbotix_sdk.srv import FirmwareGains, FirmwareGainsRequest
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

        self._safety_box = spaces.Box(low=np.array([0.115, -0.26, 0.049]),
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

        self.image_save_dir = ""


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


    def set_image_save_dir(self, save_dir):
        self.image_save_dir = save_dir


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
        while True:
            try:
                self.get_observation_publisher.publish("GET_OBSERVATION")
                self.current_pos = np.array(rospy.wait_for_message(
                "/widowx_env/action/observation", numpy_msg(Floats), timeout=5).data)
                break
            except:
                continue
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
        #goal[0] = np.random.uniform(low=0.16, high=0.34)
        #goal[1] = np.random.uniform(low=-0.22, high=0.14) #(-0.22, 0.14)

        #goal[2] = 0.14
        goal_idx = np.random.uniform()
        if goal_idx < 0.5:
            goal = np.array([0.25, -0.12, 0.13])
        else:
            goal = np.array([0.25, 0.08, 0.13])
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
                self._is_gripper_open = True
            except:
                continue


    def close_gripper(self):
        #while self.current_pos[8] > 0.5:
        self.gripper_publisher.publish("CLOSE")
        rospy.sleep(1)
        try:
            self.get_observation_publisher.publish("GET_OBSERVATION")
            self.current_pos = np.array(rospy.wait_for_message(
            "/widowx_env/action/observation", numpy_msg(Floats), timeout=5).data)
            self._is_gripper_open = False
        except:
            pass


    def get_current_pos(self):
        try:
            self.get_observation_publisher.publish("GET_OBSERVATION")
            self.current_pos = np.array(rospy.wait_for_message(
            "/widowx_env/action/observation", numpy_msg(Floats), timeout=5).data)
        except:
            pass

        return self.current_pos


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


    def _start_rospy(self, use_kinect=True):
        rospy.init_node("WidowX200_Env")

        #Publishers
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


        #Services
        rospy.wait_for_service('/wx200/set_firmware_pid_gains')
        self.firmware_pid_proxy = rospy.ServiceProxy('/wx200/set_firmware_pid_gains', FirmwareGains)

        #NOTE: ROS node must be initialized before depth image service is created
        try:
            self.depth_image_service = utils.KinectImageService('sd_pts')
        except:
            print("Kinect not being used!")

        return self


    def set_default_firmware_gains(self):
        gains = collections.OrderedDict()
        gains["joint_id"] = 0
        gains["Kp_pos"] = [800, 800, 800, 800, 640, 640]
        gains["Ki_pos"] = [0, 0, 0, 0, 0, 0]
        gains["Kd_pos"] = [0, 0, 0, 0, 3600, 3600]
        gains["K1"] = [0, 0, 0, 0, 0, 0]
        gains["K2"] = [0, 0, 0, 0, 0, 0]
        gains["Kp_vel"] = [200, 200, 200, 200, 100, 100]
        gains["Ki_vel"] = [1920] * 4 + [1000] * 2
        req = FirmwareGainsRequest(*gains.values())
        self.firmware_pid_proxy(req)


    def set_low_firmware_gains(self):
        gains = collections.OrderedDict()
        gains["joint_id"] = 0
        gains["Kp_pos"] = [700, 700, 700, 700, 640, 640]
        gains["Ki_pos"] = [0, 0, 0, 0, 0, 0]
        gains["Kd_pos"] = [0, 0, 0, 0, 3600, 3600]
        gains["K1"] = [0, 0, 0, 0, 0, 0]
        gains["K2"] = [0, 0, 0, 0, 0, 0]
        gains["Kp_vel"] = [200, 200, 200, 200, 100, 100]
        gains["Ki_vel"] = [1920] * 4 + [1000] * 2
        req = FirmwareGainsRequest(*gains.values())
        self.firmware_pid_proxy(req)
