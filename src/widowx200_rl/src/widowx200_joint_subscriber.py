#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg

import numpy as np
import os

from widowx200_core.widowx_controller import WidowXController


def start_controller():
    global widowx_controller
    widowx_controller = WidowXController()


def initialize_subscribers():
    reset_subscriber = rospy.Subscriber("/widowx_env/reset", String, reset)


def reset(data):
    widowx_controller.move_to_reset()
    if data.data != "NO_GRIPPER":
        widowx_controller.open_gripper()


if __name__ == '__main__':
    start_controller()
    initialize_subscribers()
    rospy.spin()

