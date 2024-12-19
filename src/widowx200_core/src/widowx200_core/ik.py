from threading import Lock

import numpy as np
import pybullet as p
import rospy
from sensor_msgs.msg import JointState
from widowx200_core.params import *


class InverseKinematics():
    def __init__(self, robot_params, robot_type='wx200'):
        p.connect(p.DIRECT)
        self.robot_params = robot_params
        self.robot_type = robot_type

        if self.robot_type == 'wx200':
            widow_x_urdf = '/'.join(
                __file__.split('/')[:-1]) + '/../../widowx200_urdf/wx200.urdf'
            self.ee_link_index = 5
        elif self.robot_type == 'wx250s':
            widow_x_urdf = '/'.join(
                __file__.split('/')[:-1]) + '/../../widowx200_urdf/wx250s.urdf'
            self.ee_link_index = 6
        else:
            raise NotImplementedError

        self._armID = p.loadURDF(widow_x_urdf, useFixedBase=True)
        p.resetBasePositionAndOrientation(self._armID, [0, 0, 0],
                                          p.getQuaternionFromEuler(
                                              [np.pi, np.pi, np.pi]))

        self._joint_lock = Lock()
        self._angles, self._velocities = {}, {}
        joint_state_subscriber = rospy.Subscriber(
            "/{}/joint_states".format(self.robot_type), JointState,
            self._joint_callback)
        rospy.sleep(2.0)

    def _reset_pybullet(self, joint_angles=None):
        '''
        Reset pybullet sim to current joint angles
        '''
        if joint_angles is None:
            joint_angles = self.get_joint_angles()
        for i, angle in enumerate(joint_angles):
            p.resetJointState(self._armID, i, angle)

    def _joint_callback(self, msg):
        with self._joint_lock:
            for name, position, velocity in zip(msg.name, msg.position,
                                                msg.velocity):
                self._angles[name] = position
                self._velocities[name] = velocity

    def get_joint_angles(self):
        '''
        Returns current joint angles
        '''
        with self._joint_lock:
            try:
                return np.array(
                    [self._angles[k] for k in self.robot_params['JOINT_NAMES']])
            except KeyError:
                return None

    def get_joint_angles_velocity(self):
        '''
        Returns velocities for joints
        '''
        with self._joint_lock:
            try:
                return np.array([self._velocities[k] for k in
                                 self.robot_params['JOINT_NAMES']])
            except KeyError:
                return None

    def get_gripper_state(self, integrate_force=False):
        '''#Returns cartesian end-effector pose
        Return current gripper state, force reading
        TODO: add force reading
        '''
        with self._joint_lock:
            joint_angle = self._angles['gripper']
        return joint_angle, None

    def get_cartesian_pose(self, joint_angles=None):
        '''
        Get xyz pose for arm (computes from simulation)
        '''
        self._reset_pybullet(joint_angles)
        position, quat = p.getLinkState(self._armID, self.ee_link_index,
                                        computeForwardKinematics=1)[4:6]
        return np.array(list(position) + list(quat), dtype='float32')

    def _calculate_ik(self, targetPos, targetQuat, threshold=1e-5, maxIter=1000,
                      nJoints=6):
        '''
        Compute ik solution given pose
        '''
        closeEnough = False
        iter_count = 0
        dist2 = None

        best_ret, best_dist = None, float('inf')
        # p.resetJointState(self._armID, 0, -self.get_joint_angles()[0])]

        while (not closeEnough) and iter_count < maxIter:
            jointPoses = list(p.calculateInverseKinematics(
                self._armID, self.ee_link_index, targetPos, targetQuat,
                self.robot_params['JOINT_MAX'], self.robot_params['JOINT_MIN']))
            for i in range(nJoints):
                jointPoses[i] = max(min(jointPoses[i],
                                        self.robot_params['JOINT_MAX'][i]),
                                    self.robot_params['JOINT_MIN'][i])
                p.resetJointState(self._armID, i, jointPoses[i])

            ls = p.getLinkState(self._armID, self.ee_link_index,
                                computeForwardKinematics=1)
            newPos, newQuat = ls[4], ls[5]
            dist2 = sum([(targetPos[i] - newPos[i]) ** 2 for i in range(3)])
            closeEnough = dist2 < threshold
            iter_count += 1

            if dist2 < best_dist:
                best_ret, best_dist = (jointPoses, newPos, newQuat), dist2

        return best_ret

    def _ik_wrapper(self, targetPos, targetQuat, threshold=1e-5, maxIter=1000,
                    nJoints=6):
        pos, quat = self.get_cartesian_pose()


if __name__ == '__main__':
    rospy.init_node('IK_Node')
    k = InverseKinematics()
    # rospy.spin()
    pose = k.get_cartesian_pose()
    print(pose)
    print('Neutral Pose', k._calculate_ik(pose[:3], [pose][4:]))
