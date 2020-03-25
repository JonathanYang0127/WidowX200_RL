#!/usr/bin/env python
from params import *
from ik import InverseKinematics
import rospy
from interbotix_sdk.msg import SingleCommand, JointCommands


class WidowXController:
    def __init__(self):
        rospy.init_node('widowx_controller')
        self._single_joint_pub = rospy.Publisher('/wx200/single_joint/command', SingleCommand, queue_size = 1)
        self._multiple_joints_pub = rospy.Publisher('/wx200/joint/commands', JointCommands, queue_size = 1)
        rospy.sleep(2.0)

        self._ik = InverseKinematics()


    def move_to_target_joints(self, joint_values):
        '''
        Move arm to specified joint values
        '''
        self._multiple_joints_pub.publish(JointCommands(joint_values))
        rospy.sleep(MOVE_WAIT_TIME)


    def move_to_neutral(self):
        '''
        Move arm to neutral position
        '''
        self.move_to_target_joints(NEUTRAL_JOINTS)


    def move_to_reset(self):
        '''
        Move arm to reset position
        '''
        self.move_to_target_joints(RESET_JOINTS)


    def move_gripper(self, cmd):
        self._single_joint_pub.publish(SingleCommand('gripper', cmd))
        rospy.sleep(GRIPPER_WAIT_TIME)


    def open_gripper(self):
        self._single_joint_pub.publish(SingleCommand('gripper', GRIPPER_OPEN))
        rospy.sleep(GRIPPER_WAIT_TIME)


    def close_gripper(self):
        self._single_joint_pub.publish(SingleCommand('gripper', GRIPPER_CLOSED))
        rospy.sleep(GRIPPER_WAIT_TIME)


if __name__ == '__main__':
    controller = WidowXController()
    controller.move_to_neutral()
    controller.open_gripper()
    rospy.sleep(1.0)
    controller.close_gripper()
    rospy.sleep(1.0)
    rospy.spin()
