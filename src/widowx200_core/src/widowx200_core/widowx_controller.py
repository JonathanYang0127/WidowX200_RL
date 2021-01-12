#!/usr/bin/env python
from params import *

from ik import InverseKinematics
import rospy
from interbotix_sdk.robot_manipulation import InterbotixRobot
from interbotix_sdk.msg import SingleCommand, JointCommands
from interbotix_sdk.srv import OperatingModes, OperatingModesRequest, RegisterValues, RegisterValuesRequest, FirmwareGains, FirmwareGainsRequest
import collections


class WidowXBaseController(object):
    def __init__(self):
        rospy.init_node('widowx_controller')
        self._single_joint_pub = rospy.Publisher('/wx200/single_joint/command', SingleCommand, queue_size = 1)
        self._multiple_joints_pub = rospy.Publisher('/wx200/joint/commands', JointCommands, queue_size = 1)
        rospy.sleep(2.0)

        self._ik = InverseKinematics()

        rospy.wait_for_service('/wx200/set_operating_modes')
        rospy.wait_for_service('/wx200/set_motor_register_values')
        rospy.wait_for_service('/wx200/set_firmware_pid_gains')
        self.operating_modes_proxy = rospy.ServiceProxy('/wx200/set_operating_modes', OperatingModes)
        self.srv_set_register = rospy.ServiceProxy('/wx200/set_motor_register_values', RegisterValues)
        self.firmware_pid_proxy = rospy.ServiceProxy('/wx200/set_firmware_pid_gains', FirmwareGains)
        self.use_time = False

    def set_default_firmware_gains(self):
        gains = collections.OrderedDict()
        gains["joint_id"] = 0
        gains["Kp_pos"] = [800, 800, 800, 800, 640, 640]
        gains["Ki_pos"] = [0, 0, 0, 0, 0, 0]
        gains["Kd_pos"] = [0, 0, 0, 0, 3600, 3600]
        gains["K1"] = [0, 0, 0, 0, 0, 0]
        gains["K2"] = [0, 0, 0, 0, 0, 0]
        gains["Kp_vel"] = [200, 200, 200, 200, 200, 200]
        gains["Ki_vel"] = [1920] * 4 + [1000] * 2
        req = FirmwareGainsRequest(*gains.values())
        self.firmware_pid_proxy(req)

    def set_trajectory_time(self, moving_time=None, accel_time=None):
        print(moving_time, accel_time)
        if (moving_time != None):
            self.moving_time = moving_time
            if self.use_time:
                self.srv_set_register(cmd=RegisterValuesRequest.ARM_JOINTS, addr_name="Profile_Velocity", value=int(moving_time * 1000))
            else:
                self.srv_set_register(cmd=RegisterValuesRequest.ARM_JOINTS, addr_name="Profile_Velocity", value=int(moving_time))
        if (accel_time != None):
            self.accel_time = accel_time
            if self.use_time:
                self.srv_set_register(cmd=RegisterValuesRequest.ARM_JOINTS, addr_name="Profile_Acceleration", value=int(accel_time * 1000))
            else:
                self.srv_set_register(cmd=RegisterValuesRequest.ARM_JOINTS, addr_name="Profile_Acceleration", value=int(accel_time))


    def enforce_joint_limits(self, joint_values):
        joint_command = [0, 0, 0, 0, 0]
        for i in range(5):
            joint_command[i] = max(joint_values[i], JOINT_MIN[i])
            joint_command[i] = min(joint_values[i], JOINT_MAX[i])
        return joint_command


    def move_to_neutral(self):
        '''
        Move arm to neutral position
        '''
        self.move_to_target_joints(NEUTRAL_JOINTS)
        rospy.sleep(1.0)


    def move_to_reset(self):
        '''
        Move arm to reset position
        '''
        #self.move_to_target_joints(RESET_JOINTS_SLACK)
        #rospy.sleep(1.0)
        self.move_to_target_joints(RESET_JOINTS)
        rospy.sleep(1.0)


    def move_to_reset_far(self):
        '''
        Move arm to far reset position
        '''
        #self.move_to_target_joints(RESET_JOINTS_SLACK)
        #rospy.sleep(1.0)
        self.move_to_target_joints(RESET_JOINTS_FAR)
        rospy.sleep(1.0)


    def move_gripper(self, cmd):
        self._single_joint_pub.publish(SingleCommand('gripper', cmd))
        rospy.sleep(GRIPPER_WAIT_TIME)


    def open_gripper(self):
        self._single_joint_pub.publish(SingleCommand('gripper', GRIPPER_OPEN))
        rospy.sleep(GRIPPER_WAIT_TIME)


    def close_gripper(self):
        self._single_joint_pub.publish(SingleCommand('gripper', GRIPPER_CLOSED))
        rospy.sleep(GRIPPER_WAIT_TIME)


class WidowXPositionController(WidowXBaseController):
    def __init__(self):
        super(WidowXPositionController, self).__init__()
        print("HI")

        self.operating_modes_proxy(cmd=OperatingModesRequest.ARM_JOINTS, mode='position', \
        use_custom_profiles=True, profile_velocity=131, profile_acceleration=15)
        self.set_default_firmware_gains()


    def move_to_target_joints(self, joint_values):
        '''
        Move arm to specified joint valFirmwareGainsRequestues
        '''
        joint_command = self.enforce_joint_limits(joint_values)
        self._multiple_joints_pub.publish(JointCommands(joint_command))
        rospy.sleep(MOVE_WAIT_TIME)


class WidowXVelocityController(WidowXBaseController):
    def __init__(self):
        super(WidowXVelocityController, self).__init__()

        self.operating_modes_proxy(cmd=OperatingModesRequest.ARM_JOINTS, mode='velocity')
        self.set_trajectory_time(0, 0)
        self.set_default_firmware_gains()

    def move_to_target_joints(self, joint_values, duration=VEL_MOVE_WAIT_TIME, nsteps=10):
        '''
        Move arm to specified joint values
        '''
        per_step = duration / float(nsteps)
        print(per_step)
        for i in range(nsteps):
            current = self._ik.get_joint_angles()[:5]
            error = joint_values - current
            #print(error)
            if np.linalg.norm(error) < 0.05:
                ctrl = error
            else:
                ctrl = error / np.linalg.norm(error) / 3

            max_speed = 0.8
            ctrl = np.clip(ctrl, -max_speed, max_speed)
            # print('ctrl {}'.format(ctrl))
            ctrl = self.enforce_joint_limits(ctrl)
            #print(ctrl)
            self._multiple_joints_pub.publish(JointCommands(ctrl))
            self._last_healthy_tstamp = rospy.get_time()
            rospy.sleep(per_step)
        # self.arm.set_joint_commands(np.zeros(6), moving_time=0.2, accel_time=0.05, delay=0.01)
        print("stop")
        self._multiple_joints_pub.publish(JointCommands(np.zeros(5)))

    def move_to_neutral(self):
        '''
        Move arm to neutral position
        '''
        self.move_to_target_joints(NEUTRAL_JOINTS, duration=3, nsteps=60)
        rospy.sleep(1.5)


    def move_to_reset(self):
        '''
        Move arm to reset position
        '''
        #self.move_to_target_joints(RESET_JOINTS_SLACK)
        #rospy.sleep(1.0)
        self.move_to_target_joints(RESET_JOINTS, duration=3, nsteps=60)
        rospy.sleep(1.5)


    def move_to_reset_far(self):
        '''
        Move arm to far reset position
        '''
        #self.move_to_target_joints(RESET_JOINTS_SLACK)
        #rospy.sleep(1.0)
        self.move_to_target_joints(RESET_JOINTS_FAR, duration=3, nsteps=60)
        rospy.sleep(1.5)


if __name__ == '__main__':
    controller = WidowXController()
    controller.move_to_neutral()
    controller.open_gripper()
    rospy.sleep(1.0)
    controller.close_gripper()
    rospy.sleep(1.0)
    controller.move_to_reset()
    rospy.spin()
