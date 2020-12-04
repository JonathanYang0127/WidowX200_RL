#!/usr/bin/env python
from params import WIDOW200_PARAMS, WIDOW250_PARAMS
from ik import InverseKinematics
import rospy
from interbotix_sdk.msg import SingleCommand, JointCommands


class WidowXController:
    def __init__(self, robot_type='wx200'):
        rospy.init_node('widowx_controller')
        
 	self.robot_type = robot_type
        if self.robot_type == 'wx200':
            self._single_joint_pub = rospy.Publisher('/wx200/single_joint/command', SingleCommand, queue_size = 1)
            self._multiple_joints_pub = rospy.Publisher('/wx200/joint/commands', JointCommands, queue_size = 1)
            self.robot_params = WIDOW200_PARAMS
        elif self.robot_type == 'wx250':
            self._single_joint_pub = rospy.Publisher('/wx250/single_joint/command', SingleCommand, queue_size = 1)
            self._multiple_joints_pub = rospy.Publisher('/wx250/joint/commands', JointCommands, queue_size = 1)
            self.robot_params = WIDOW250_PARAMS
        rospy.sleep(2.0)

        self._ik = InverseKinematics()


    def move_to_target_joints(self, joint_values):
        '''
        Move arm to specified joint values
        '''
        joint_command = [0] * self.robot_params['NUM_JOINTS'] - 1
        for i in range(self.robot_params['NUM_JOINTS'] - 1):
            joint_command[i] = max(joint_values[i], JOINT_MIN[i])
            joint_command[i] = min(joint_values[i], JOINT_MAX[i])
        self._multiple_joints_pub.publish(JointCommands(joint_command))
        rospy.sleep(self.robot_params['MOVE_WAIT_TIME'])


    def move_to_neutral(self):
        '''
        Move arm to neutral position
        '''
        self.move_to_target_joints(self.robot_params['NEUTRAL_JOINTS'])


    def move_to_reset(self):
        '''
        Move arm to reset position
        '''
        #self.move_to_target_joints(RESET_JOINTS_SLACK)
        #rospy.sleep(1.0)
        self.move_to_target_joints(self.robot_params['RESET_JOINTS'])


    def move_to_reset_far(self):
        '''
        Move arm to far reset position
        '''
        #self.move_to_target_joints(RESET_JOINTS_SLACK)
        #rospy.sleep(1.0)
        self.move_to_target_joints(self.robot_params['RESET_JOINTS_FAR'])


    def move_gripper(self, cmd):
        self._single_joint_pub.publish(SingleCommand('gripper', cmd))
        rospy.sleep(self.robot_params['GRIPPER_WAIT_TIME'])


    def open_gripper(self):
        self._single_joint_pub.publish(SingleCommand('gripper', self.robot_params['GRIPPER_OPEN']))
        rospy.sleep(self.robot_params['GRIPPER_WAIT_TIME'])


    def close_gripper(self):
        self._single_joint_pub.publish(SingleCommand('gripper', self.robot_params['GRIPPER_CLOSED']))
        rospy.sleep(self.robot_params['GRIPPER_WAIT_TIME'])


if __name__ == '__main__':
    controller = WidowXController()
    controller.move_to_neutral()
    controller.open_gripper()
    rospy.sleep(1.0)
    controller.close_gripper()
    rospy.sleep(1.0)
    #controller.move_to_reset()
    rospy.spin()
