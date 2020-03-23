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
        self.action_space = spaces.Box(low=np.array([-0.5, -0.25, -0.25, -0.25, -0.5, 0.0 / 3]),
                                       high=np.array([0.5, 0.25, 0.25, 0.25, 0.5, 2.0 / 3]), dtype=np.float32)


    def reset(self):
        self.reset_publisher.publish("OPEN_GRIPPER")


    def _start_rospy(self):
        rospy.init_node("WidowX200_Env")
        self.reset_publisher = rospy.Publisher(
            "/widowx_env/reset", String, queue_size=1)
        rospy.sleep(2.0)

        return self
