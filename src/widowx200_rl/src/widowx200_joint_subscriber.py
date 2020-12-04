#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg

import numpy as np
import os

from widowx200_core.widowx_controller import WidowXController
from widowx200_core.params import WIDOW200_PARAMS, WIDOW250_PARAMS

def start_controller():
    global widowx_controller
    widowx_controller = WidowXController(robot_type='wx200')


def initialize_publishers_and_subscribers():
    global observation_publisher
    '''
    Subscribers
    '''
    reset_subscriber = rospy.Subscriber("/widowx_env/reset", String, reset)
    action_subscriber = rospy.Subscriber(
        "/widowx_env/action", numpy_msg(Floats), take_action)
    joint_subscriber = rospy.Subscriber(
        "/widowx_env/joint/command", numpy_msg(Floats), move_to_joints)
    gripper_subscriber = rospy.Subscriber(
        "widowx_env/gripper/command", String, gripper_cb)
    neutral_subscriber = rospy.Subscriber(
        "/widowx_env/neutral", String, neutral_cb)
    observation_subscriber = rospy.Subscriber(
        "/widowx_env/get_observation", String, observation_cb)

    '''
    Publishers
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
    assert action.shape[0] == 6 or action.shape[0] == 5
    if action.shape[0] == 6:
        gripper_action = action[-1]
        widowx_controller.move_gripper(gripper_action * 3)
    action = action[:5]
    target_joints = widowx_controller._ik.get_joint_angles()[:5] + action
    widowx_controller.move_to_target_joints(target_joints)
    rospy.sleep(0.25)
    current_state = np.array(get_state(), dtype=np.float32)
    observation_publisher.publish(current_state)


def move_to_joints(data):
    widowx_controller.move_to_target_joints(data.data)
    rospy.sleep(0.5)
    current_state = np.array(get_state(), dtype=np.float32)
    observation_publisher.publish(current_state)


def observation_cb(data):
    current_state = np.array(get_state(), dtype=np.float32)
    rospy.sleep(1)
    observation_publisher.publish(current_state)


def reset(data):
    #widowx_controller.move_to_neutral()
    #rospy.sleep(1.5)
    if 'FAR_POSITION' in data.data:
        widowx_controller.move_to_reset_far()
        rospy.sleep(1.0)
    else:
        widowx_controller.move_to_reset()
        rospy.sleep(1.0)
    if not "NO_GRIPPER" in data.data:
        while widowx_controller._ik.get_joint_angles()[5] < 1.6:
             widowx_controller.open_gripper()


def gripper_cb(data):
    if data.data == 'CLOSE':
        widowx_controller.close_gripper()
    else:
        widowx_controller.open_gripper()


def neutral_cb(data):
    widowx_controller.move_to_neutral()
    rospy.sleep(1.5)

if __name__ == '__main__':
    start_controller()
    initialize_publishers_and_subscribers()
    rospy.spin()
