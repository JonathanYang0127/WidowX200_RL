from visual_mpc.envs import robot_envs
from visual_mpc.envs.robot_envs import RobotController
import numpy as np
import math
import rospy
# from replab_core.config import *
import logging
from pyquaternion import Quaternion
from sensor_msgs.msg import JointState
from threading import Lock
import time
from interbotix_sdk.robot_manipulation import InterbotixRobot
import modern_robotics as mr
from interbotix_descriptions import interbotix_mr_descriptions as mrd
from visual_mpc.agent.general_agent import Environment_Exception
import sys
from modern_robotics.core import JacobianSpace, Adjoint, MatrixLog6, se3ToVec, TransInv, FKinSpace
import h5py
import _pickle as pkl
import visual_mpc.agent.utils.transformation_utils as tr

from interbotix_sdk.msg import JointCommands
from visual_mpc.envs.util.teleop.server import SpaceMouseRemoteReader
from visual_mpc.envs.robot_envs.widowx250s.custom_gripper_controller import GripperController

from visual_mpc.envs.robot_envs.util.vr_control.oculus_reader.reader import OculusReader


def compute_joint_velocities_from_cartesian(Slist, M, T, thetalist_current):
    """Computes inverse kinematics in the space frame for an open chain robot
    :param Slist: The joint screw axes in the space frame when the
                  manipulator is at the home position, in the format of a
                  matrix with axes as the columns
    :param M: The home configuration of the end-effector
    :param T: The desired end-effector configuration Tsd
    :param thetalist_current: An initial guess of joint angles that are close to
                       satisfying Tsd
    """
    thetalist = np.array(thetalist_current).copy()
    Tsb = FKinSpace(M,Slist, thetalist)
    Vs = np.dot(Adjoint(Tsb), \
                se3ToVec(MatrixLog6(np.dot(TransInv(Tsb), T))))
    theta_vel = np.dot(np.linalg.pinv(JacobianSpace(Slist, \
                                                    thetalist)), Vs)
    return theta_vel


class ModifiedInterbotixRobot(InterbotixRobot):
    def set_ee_pose_matrix_fast(self, T_sd, custom_guess=None, execute=True):
        """
        this version of set_ee_pose_matrix does not set the velocity profie registers in the servos and therefore runs faster
        """
        if (custom_guess is None):
            initial_guesses = self.initial_guesses
        else:
            initial_guesses = [custom_guess]

        for guess in initial_guesses:
            theta_list, success = mr.IKinSpace(self.robot_des.Slist, self.robot_des.M, T_sd, guess, 0.001, 0.001)
            solution_found = True

            # Check to make sure a solution was found and that no joint limits were violated
            if success:
                theta_list = [int(elem * 1000)/1000.0 for elem in theta_list]
                for x in range(self.resp.num_joints):
                    if not (self.resp.lower_joint_limits[x] <= theta_list[x] <= self.resp.upper_joint_limits[x]):
                        solution_found = False
                        break
            else:
                solution_found = False

            if solution_found:
                if execute:
                    self.publish_positions_fast(theta_list)
                    self.T_sb = T_sd
                return theta_list, True
            else:
                rospy.loginfo("Guess failed to converge...")

        rospy.loginfo("No valid pose could be found")
        return theta_list, False

    def publish_positions_fast(self, positions):
        self.joint_positions = list(positions)
        joint_commands = JointCommands(positions)
        self.pub_joint_commands.publish(joint_commands)
        self.T_sb = mr.FKinSpace(self.robot_des.M, self.robot_des.Slist, positions)


class WidowX250S_Controller(RobotController):
    def __init__(self, robot_name, print_debug, enable_rotation='6dof', gripper_attached='custom'):
        """
        gripper_attached: either "custom" or "default"
        """
        self.arm = ModifiedInterbotixRobot(robot_name="wx250s", mrd=mrd)
        self.arm.set_joint_operating_mode('position')
        super(WidowX250S_Controller, self).__init__(robot_name, print_debug, gripper_attached=gripper_attached, init_rosnode=False)

        self._joint_lock = Lock()
        self._angles, self._velocities = {}, {}
        rospy.Subscriber("/wx250s/joint_states", JointState, self._joint_callback)
        time.sleep(1)
        self._n_errors = 0

        self._lower_joint_limits = np.array([-3.1, -1.9, -1.6, 0.8, -1.9, -2.6])
        self._upper_joint_limits = np.array([3.1, 1.9, 1.6, 10, 1.8, 2.2])
        self.joint_names = self.arm.resp.joint_names
        self._joint_lock = Lock()
        self.default_rot = np.array([[-0.0198258 , -0.04785726, -0.99865741],
                                    [-0.03134369, -0.99833302,  0.04846396],
                                    [-0.99931202,  0.03226245,  0.01829272]])
        self.enable_rotation = enable_rotation

    def move_to_state(self, target_xyz, target_zangle, duration=1.5):
        new_pose = np.eye(4)
        new_pose[:3, -1] = target_xyz
        new_quat = Quaternion(axis=np.array([0.0, 0.0, 1.0]), angle=target_zangle) * Quaternion(matrix=self.default_rot)
        new_pose[:3, :3] = new_quat.rotation_matrix
        self.move_to_eep(new_pose, duration)

    def move_to_eep(self, target_pose, duration=1.5):
        try:
            solution, success = self.arm.set_ee_pose_matrix(target_pose, custom_guess=self.get_joint_angles()[:6],
                                                            moving_time=duration, accel_time=duration * 0.45)
        except rospy.service.ServiceException:
            print('stuck during move')
            import pdb;
            pdb.set_trace()
            self.move_to_neutral()
        if not success:
            print('no IK solution found')
            raise Environment_Exception

    def move_to_neutral(self, duration=4):
        print('moving to neutral..')
        des = np.array([-5.36893308e-02, -4.70932126e-01, -4.34116572e-01, 3.11091304e+00,
                        1.60300994e+00, 3.06796166e-03])
        if self.get_joint_angles()[3] < 0:
            print('j4 is negative')
            import pdb; pdb.set_trace()
        try:
            self.arm.set_joint_commands(des, accel_time=duration*0.45, moving_time=duration, delay=duration)
        except rospy.service.ServiceException:
            print('stuck during reset')
            import pdb; pdb.set_trace()
            self.move_to_neutral()

    def _joint_callback(self, msg):
        with self._joint_lock:
            for name, position, velocity in zip(msg.name, msg.position, msg.velocity):
                self._angles[name] = position
                self._velocities[name] = velocity

    def get_joint_angles(self):
        '''
        Returns current joint angles
        '''
        with self._joint_lock:
            try:
                return np.array([self._angles[k] for k in self.joint_names])
            except KeyError:
                return None

    def get_joint_angles_velocity(self):
        '''
        Returns velocities for joints
        '''
        with self._joint_lock:
            try:
                return np.array([self._velocities[k] for k in self.joint_names])
            except KeyError:
                return None

    def get_cartesian_pose(self, matrix=False):
        #Returns cartesian end-effector pose
        joint_positions = list(self.arm.joint_states.position[self.arm.waist_index:(self.arm.resp.num_joints + self.arm.waist_index)])
        pose = mr.FKinSpace(self.arm.robot_des.M, self.arm.robot_des.Slist, joint_positions)
        if matrix:
            return pose
        else:
            return np.concatenate([pose[:3, -1], np.array(Quaternion(matrix=pose[:3, :3]).elements)])

    def _init_gripper(self, gripper_attached):
        if gripper_attached == 'custom':
            self._gripper = GripperController(self.arm)
            self.custom_gripper_controller = True
        else:
            self.custom_gripper_controller = False

    def get_gripper_desired_state(self, integrate_force=False):
        # returns gripper joint angle, force reading (none if no force)
        return self._gripper.get_gripper_desired_state()

    def open_gripper(self, wait=False):
        if self.custom_gripper_controller:
            self._gripper.open()
        else:
            self.arm.open_gripper()

    def close_gripper(self, wait=False):
        if self.custom_gripper_controller:
            self._gripper.close()
        else:
            self.arm.close_gripper()


class VR_WidowX250S_Controller(WidowX250S_Controller):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.reader = OculusReader()
        rospy.Timer(rospy.Duration(0.02), self.update_robot_cmds)
        # rospy.Timer(rospy.Duration(0.3), self.update_robot_cmds)
        self.prev_grip_press = False
        self.reference_vr_transform = None
        self.reference_robot_transform = None


        self.do_reset = False
        self.task_stage = 0
        self.num_task_stages = 1e9

    def get_pose_and_button(self):
        poses, buttons = self.reader.get_arays_and_button()
        if poses == []:
            return None, None, None
        trigger = buttons['RTr']
        gripper_button = buttons['RG']
        right_controller_pose = poses[0]
        return right_controller_pose, trigger, gripper_button

    def update_robot_cmds(self, event):
        current_vr_transform, trigger, gripper_button = self.get_pose_and_button()
        if current_vr_transform is None:
            return
        else:
            if not self.prev_grip_press and gripper_button:
                print("resetting reference pose")
                self.reference_vr_transform = current_vr_transform
                self.reference_robot_transform = self.get_cartesian_pose(matrix=True)
                self.arm.set_trajectory_time(moving_time=0.2, accel_time=0.05)

            if not gripper_button:
                # print("stopping robot")
                self.reference_vr_transform = None
                self.reference_robot_transform = self.get_cartesian_pose(matrix=True)
                self.prev_grip_press = False
                return
        self.prev_grip_press = True

        delta_vr_transform = current_vr_transform.dot(tr.TransInv(self.reference_vr_transform))
        delta_vr_transform = tr.RpToTrans(Quaternion(axis=[0, 0, 1], angle=-np.pi/2).rotation_matrix, np.zeros(3)).dot(delta_vr_transform)
        delta_vr_transform[:3, :3] = np.eye(3)
        delta_vr_transform[:3, 3] *= 0.3
        print("delta transform", delta_vr_transform[:3, 3])
        new_robot_transform = delta_vr_transform.dot(self.reference_robot_transform)
        # print("new robot transform", new_robot_transform[:3, 3])

        try:
            solution, success = self.arm.set_ee_pose_matrix_fast(new_robot_transform, custom_guess=self.get_joint_angles()[:6])
        except rospy.service.ServiceException:
            print('stuck during move')
            import pdb;
            pdb.set_trace()
            self.move_to_neutral()
        if not success:
            print('no IK solution found')
            raise Environment_Exception



class WidowX250SVelocityController(WidowX250S_Controller):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.arm.set_joint_operating_mode('velocity')
        self.arm.set_trajectory_time(moving_time=0.2, accel_time=0.05)

        self.space_mouse = SpaceMouseRemoteReader()
        rospy.Timer(rospy.Duration(0.02), self.update_robot_cmds)
        self.last_update_cmd = time.time()
        self.enable_cmd_thread = False
        self.do_reset = False
        self.task_stage = 0
        self.num_task_stages = 1e9

    def update_robot_cmds(self, event):
        reading = self.space_mouse.get_reading()
        if reading is not None and self.enable_cmd_thread:
            # print('delta t cmd update, ', time.time() - self.last_update_cmd)
            self.last_update_cmd = time.time()
            if reading['left'] and reading['right'] or reading['left_and_right']:
                self.task_stage += 1
                self.task_stage = np.clip(self.task_stage, 0, self.num_task_stages)
                if self.task_stage == self.num_task_stages:
                    print('resetting!')
                    self.do_reset = True
                rospy.sleep(1.0)
            # t0 = time.time()
            self.apply_spacemouse_action(reading)
            # print('apply action time', time.time() - t0)

    def apply_spacemouse_action(self, readings):
        if readings is None:
            print('readings are None!')
            return
        if self.custom_gripper_controller:
            if readings['left']:
                self._gripper.open()
            if readings['right']:
                self._gripper.close()
        else:
            if readings['left']:
                self.arm.open_gripper()
            if readings['right']:
                self.arm.close_gripper()

        if self.enable_rotation:
            pose = self.get_cartesian_pose(matrix=True)
            current_quat = Quaternion(matrix=pose[:3, :3])
            translation_scale = 0.1
            commanded_translation_velocity = readings['xyz'] * translation_scale
            new_pos = pose[:3, 3] + commanded_translation_velocity

            rotation_scale = 0.3
            commanded_rotation_velocity = readings['rot'] * rotation_scale
            if self.enable_rotation == '4dof':
                commanded_rotation_velocity = commanded_rotation_velocity[2]
                new_rot = Quaternion(axis=[0, 0, 1], angle=commanded_rotation_velocity) * current_quat
            elif self.enable_rotation == '6dof':
                new_rot = Quaternion(axis=[1, 0, 0], angle=commanded_rotation_velocity[0]) * \
                          Quaternion(axis=[0, 1, 0], angle=commanded_rotation_velocity[1]) * \
                          Quaternion(axis=[0, 0, 1], angle=commanded_rotation_velocity[2]) * current_quat
            else:
                raise NotImplementedError

            new_transform = np.eye(4)
            new_transform[:3, :3] = new_rot.rotation_matrix
            new_transform[:3, 3] = new_pos
        else:
            new_transform = self.get_cartesian_pose(matrix=True)
            new_transform[:3, 3] += readings['xyz'] * 0.1

        joint_velocities = compute_joint_velocities_from_cartesian(self.arm.robot_des.Slist, self.arm.robot_des.M,
                                                                   new_transform, self.get_joint_angles()[:6])
        self.cap_joint_limits(joint_velocities)
        try:
            joint_commands = JointCommands(joint_velocities)
            self.arm.pub_joint_commands.publish(joint_commands)
        except:
            print('could not set joint velocity!')

    def stop_motors(self):
        self.arm.pub_joint_commands.publish(JointCommands(np.zeros(6)))
        # self.arm.set_joint_commands(np.zeros(6), moving_time=0.2, accel_time=0.05)

    def move_to_state(self, target_xyz, target_zangle, duration=2):
        pose = np.eye(4)
        rot = Quaternion(axis=[0, 0, 1], angle=target_zangle) * Quaternion(matrix=self.default_rot)
        pose[:3, :3] = rot.rotation_matrix
        pose[:3, 3] = target_xyz
        joint_pos, success = self.arm.set_ee_pose_matrix(pose, custom_guess=self.get_joint_angles()[:6], moving_time=2,
                                                         execute=False)
        if success:
            self.move_to_pos_with_velocity_ctrl(joint_pos)
            return True
        else:
            print('no kinematics solution found!')
            raise Environment_Exception

    def cap_joint_limits(self, ctrl):
        for i in range(6):
            if self.get_joint_angles()[i] < self._lower_joint_limits[i]:
                print('ctrl', ctrl)
                print('ja', self.get_joint_angles())
                print('limit', self._lower_joint_limits)
                print('lower joint angle limit violated for j{}'.format(i + 1))
                if ctrl[i] < 0:
                    print('setting to zero')
                    ctrl[i] = 0
            if self.get_joint_angles()[i] > self._upper_joint_limits[i]:
                print('ctrl', ctrl)
                print('ja', self.get_joint_angles())
                print('limit', self._lower_joint_limits)
                print('upper joint angle limit violated for j{}'.format(i + 1))
                if ctrl[i] > 0:
                    print('setting to zero')
                    ctrl[i] = 0

    def move_to_neutral(self, duration=4):
        des = np.array([-5.36893308e-02, -4.70932126e-01, -4.34116572e-01, 3.11091304e+00,
                        1.60300994e+00, 3.06796166e-03])
        self.move_to_pos_with_velocity_ctrl(des, duration=duration)

    def move_to_pos_with_velocity_ctrl(self, des, duration=3):
        if self.get_joint_angles()[3] < 0:
            print('j4 negative!')
            import pdb; pdb.set_trace()
            des[3] -= math.pi * 2

        nsteps = 30
        per_step = duration/nsteps
        for i in range(nsteps):
            current = self.get_joint_angles()[:6]
            error = des - current
            ctrl = error * 0.8
            # print('error {}'.format(error))
            # print('des {}'.format(des))
            # print('current {}'.format(current))
            max_speed = 0.5
            ctrl = np.clip(ctrl, -max_speed, max_speed)
            # print('ctrl {}'.format(ctrl))
            self.cap_joint_limits(ctrl)
            self.arm.pub_joint_commands.publish(JointCommands(ctrl))
            self._last_healthy_tstamp = rospy.get_time()
            rospy.sleep(per_step)
        # self.arm.set_joint_commands(np.zeros(6), moving_time=0.2, accel_time=0.05, delay=0.01)
        self.arm.pub_joint_commands.publish(JointCommands(np.zeros(6)))


if __name__ == '__main__':
    dir = '/mount/harddrive/spt/trainingdata/realworld/can_pushing_line/2020-09-04_09-28-29/raw/traj_group0/traj2'
    dict = pkl.load(open(dir + '/policy_out.pkl', "rb"))
    actions = np.stack([d['actions'] for d in dict], axis=0)
    dict = pkl.load(open(dir + '/obs_dict.pkl', "rb"))
    states = dict['raw_state']

    controller = WidowX250SVelocityController('widowx', True)
    rospy.sleep(2)
    controller.move_to_neutral()
    # controller.move_to_state(states[0, :3], target_zangle=states[0, 3])
    controller.move_to_state(states[0, :3], target_zangle=0.)
    # controller.redistribute_objects()

    prev_eef = controller.get_cartesian_pose()[:3]
    for t in range(20):
        # low_bound = np.array([1.12455181e-01, 8.52311223e-05, 3.23975718e-02, -2.02, -0.55]) + np.array([0, 0, 0.05, 0, 0])
        # high_bound = np.array([0.29880695, 0.22598613, 0.15609235, 1.52631092, 1.39])
        # x, y, z, theta = np.random.uniform(low_bound[:4], high_bound[:4])
        controller.apply_endeffector_velocity(actions[t]/0.2)


        new_eef = controller.get_cartesian_pose()[:3]
        print("current eef pos", new_eef[:3])
        print('desired eef pos', states[t, :3])
        print('delta', states[t, :3] - new_eef[:3])
        rospy.sleep(0.2)
