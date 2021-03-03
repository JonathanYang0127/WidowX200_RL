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
from gym_replab.envs.widow200_base import Widow200RealRobotBaseEnv
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
sys.path.append('/opt/ros/kinetic/lib/python2.7/dist-packages')

import random
from .. import utils


REWARD_FAIL = 0.0
REWARD_SUCCESS = 1.0


class Widow200RealRobotReachEnv(Widow200RealRobotBaseEnv):
    def __init__(self, reward_type='sparse', **kwargs):
        super().__init__(**kwargs)
        self._reward_type = reward_type

        self.goal = np.array([0.3, -0.07, 0.09])
        self.quat = np.array([0.5, 0.5, -0.5, 0.5], dtype=np.float32)

        self._is_gripper_open = True
        self._upwards_bias = 0.08

        self._gripper_closed = -0.3
        self._gripper_open = 0.6
        self.reward_height_thresh = 0.14

        self.radius = 0.015

        self.observation_space = Dict(
            {'state': spaces.Box(low=np.array([-1.0] * 9),
                                 high=np.array([1.0] * 9), dtype=np.float32),
             'image': spaces.Box(low=np.array([0] * self.image_shape[0] * self.image_shape[1] * 3),
                                 high=np.array([255] * self.image_shape[0] * self.image_shape[1] * 3),
                                 dtype=np.float32)})

    def _set_action_space(self):
        #Normalized action space
        self.action_space = spaces.Box(low=np.array([-1, -1, -1, -1, -1]),
                                       high=np.array([1, 1, 1, 1, 1]), dtype=np.float32)

    def get_reward(self):
        if np.linalg.norm(self.goal - self.current_pos[:3]) < self.radius:
            return REWARD_SUCCESS
        else:
            return REWARD_FAIL


    def get_observation(self):
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
            obs['render'] = self.render()
            obs['state'] =  self.current_pos[:9]
        elif self._obs_mode == 'pixel_state':
            obs['image'] = self.pull_image()
            obs['state'] =  self.current_pos[:9]
        elif self._obs_mode == 'pixels':
            obs['image'] = self.pull_image()
        return obs


    def _gripper_simulate(self, gripper_action):
        '''
        Determines gripper action given ik_command
        '''
        # is_gripper_open = self._is_gripper_open()
        is_gripper_open = self._is_gripper_open
        lift = False

        if gripper_action > 0.5 and is_gripper_open:
            # keep it open
            gripper = self._gripper_open
        elif gripper_action > 0.5 and not is_gripper_open:
            # gripper is currently closed and we want to open it
            gripper = self._gripper_open
            self._is_gripper_open = True
            self.open_gripper()
        elif gripper_action < -0.5 and not is_gripper_open:
            # keep it closed
            gripper = self._gripper_closed
        elif gripper_action < -0.5 and is_gripper_open:
            # gripper is open and we want to close it
            gripper = self._gripper_closed
            # we will also lift the object up a little
            lift = True
            self._is_gripper_open = False
            self.close_gripper()
        elif gripper_action <= 0.5 and gripper_action >= -0.5:
            # maintain current status
            if is_gripper_open:
                gripper = self._gripper_open
            else:
                gripper = self._gripper_closed
        else:
            raise NotImplementedError

        return gripper, lift


    def step(self, action):
        '''
        TODO: Change quaternion based on wrist rotation
        action: [x, y, z, wrist, gripper]
        '''
        action = np.array(action, dtype='float32')
        action = np.clip(action, self.action_space.low, self.action_space.high)
        gripper_command = 0.7

        action /= 3
        action[2] *= 4
        wrist = action[3]


        pos = self.ik.get_cartesian_pose()[:3]
        pos += action[:3]
        pos[2] += self._upwards_bias         #ik has a downwards bias for some reason
        pos = np.clip(np.array(pos, dtype=np.float32), self._safety_box.low, self._safety_box.high)
        joint_action = utils.compute_ik_solution(pos, self.quat, self.joint_space.low, self.joint_space.high, self.ik)
        joint_action[4] = wrist

        gripper, lift = self._gripper_simulate(gripper_command)

        self.action_publisher.publish(joint_action)

        try:
            self.current_pos = np.array(rospy.wait_for_message(
                "/widowx_env/action/observation", numpy_msg(Floats), timeout=5).data)
            for i in range(3):
                if self.current_pos[i] < self._safety_box.low[i] or \
                    self.current_pos[i] > self._safety_box.high[i]:
                    print(i, self._safety_box.low, self.current_pos[i], "SAFETY BOX VIOLATION")
                    return None, None, None, {'timeout': True}
            if self.current_pos[0] < 0.17 and self.current_pos[2] < 0.11:
                print(self.current_pos, "SAFETY BOX VIOLATION")
                return None, None, None, {'timeout': True}
        except:
            return None, None, None, {'timeout': True}

        if lift:
            rospy.sleep(0.2)
            moved = self.lift_object()
            print(self.current_pos[2])
            if not moved:
                return None, None, None, {'timeout': True}

        step_tuple = self._generate_step_tuple()

        #Add joint information to step tuple
        step_tuple[3]['joint_command'] = np.append(joint_action[:5], \
            np.array([[gripper_command]], dtype='float32'))
        return step_tuple


    def set_goal(self, goal):
        self.goal = goal


    def _generate_step_tuple(self):
        info = {'timeout': False}

        reward = self.get_reward()

        return self.get_observation(), reward, False, info


    def reset(self, gripper = True):
        self.move_to_neutral()
        if gripper:
            self._is_gripper_open = True
            self.reset_publisher.publish("FAR_POSITION OPEN_GRIPPER")
        else:
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
        return self.get_observation()