import gym
import gym_replab
from widowx200_core.ik import InverseKinematics

ik = InverseKinematics()
env = gym.make('widowx200-v0')._start_rospy()
env.reset()
#for i in range(9):
#    env.step([1, 0, 0, 0, 0, 0.6])
print(ik.get_cartesian_pose()[3:])
