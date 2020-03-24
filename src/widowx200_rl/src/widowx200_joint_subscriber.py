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


def initialize_publishers_and_subscribers():
    global observation_publisher
    '''
    Publishers
    '''
    reset_subscriber = rospy.Subscriber("/widowx_env/reset", String, reset)
    action_subscriber = rospy.Subscriber(
        "/widowx_env/action", numpy_msg(Floats), take_action)

    '''
    Subscribers
    '''
    observation_publisher = rospy.Publisher(
        "/widowx_env/action/observation", numpy_msg(Floats), queue_size=1)


def get_state():
    '''
    Gets the current state of the arm: [cartesian pose, joints]
    '''
    pos = list(widowx_controller._ik.get_cartesian_pose())[:3]
    joints = list(widowx_controller._ik.get_joint_angles())
    pos.extend(joints)
    return pos


def take_action(data):
    """
    Action [joint_1, joint_2, joint_3, joint_4, joint_5, gripper_joint]
    """
    action = data.data
    assert action.shape[0] == 6
    gripper_action = action[-1]
    action = action[:-1]
    target_joints = widowx_controller._ik.get_joint_angles()[:5] + action
    widowx_controller.move_to_target_joints(target_joints)
    widowx_controller.move_gripper(gripper_action)
    current_state = np.array(get_state(), dtype=np.float32)
    observation_publisher.publish(current_state)


def reset(data):
    widowx_controller.move_to_reset()
    if data.data != "NO_GRIPPER":
        widowx_controller.open_gripper()


if __name__ == '__main__':
    start_controller()
    initialize_publishers_and_subscribers()
    rospy.spin()
