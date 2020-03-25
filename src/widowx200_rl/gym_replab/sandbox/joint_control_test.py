import gym
import gym_replab
from widowx200_core.ik import InverseKinematics
import numpy as np

ik = InverseKinematics()
env = gym.make('widowx200-v0')._start_rospy()
env.reset()
env.step([1, 0, 0, 0, 0, 1.8/3])
pose = ik.get_cartesian_pose()
pos = pose[:3]
quat = pose[3:]
pos[1] -= 0.1
next_move = ik._calculate_ik(pos, quat)[0][:5] - ik.get_joint_angles()[:5]
next_move = np.append(next_move, 1.8/3)
env.step(next_move)
pose = ik.get_cartesian_pose()
pos = pose[:3]
quat = pose[3:]
pos[2] += 0.063
next_move = ik._calculate_ik(pos, quat)[0][:5] - ik.get_joint_angles()[:5]
next_move = np.append(next_move, 1.8/3)
env.step(next_move)
env.step([0, 0, 0, 0, 0, -0.8/3])
pose = ik.get_cartesian_pose()
pos = pose[:3]
quat = pose[3:]
pos[2] -= 0.7
next_move = ik._calculate_ik(pos, quat)[0][:5] - ik.get_joint_angles()[:5]
next_move = np.append(next_move, -0.8/3)
env.step(next_move)
