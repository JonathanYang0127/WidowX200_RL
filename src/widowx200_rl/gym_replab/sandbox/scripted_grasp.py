import gym
import gym_replab
from widowx200_core.ik import InverseKinematics
import numpy as np

ik = InverseKinematics()
env = gym.make('widowx200-v0')._start_rospy()
print(ik.get_cartesian_pose())
env.set_goal([0.18, -0.1, 0.39])
obs = env.reset()
print(ik.get_cartesian_pose())
print(obs)

gripper_closed = False
for i in range(80):
    print(obs)
    if np.linalg.norm((obs['desired_goal'] - obs['achieved_goal'])[:2]) > 0.03 \
        and not gripper_closed:
        print( np.linalg.norm((obs['desired_goal'] - obs['achieved_goal'])[:2]) )
        diff = obs['desired_goal'] - obs['achieved_goal']
        diff[2] = 0.3 - obs['achieved_goal'][2]
        action = gym_replab.utils.compute_ik_command(diff, ik) / 4
        action = np.append(action, 0.6)
    elif abs(obs['desired_goal'][2] - obs['achieved_goal'][2]) > 0.01 \
        and not gripper_closed:
        print(obs['desired_goal'][2], obs['achieved_goal'][2], abs(obs['desired_goal'][2] - obs['achieved_goal'][2]))
        diff = obs['desired_goal'] - obs['achieved_goal']
        diff[2] = 0.01
        action = gym_replab.utils.compute_ik_command(diff, ik) / 3
        action = np.append(action, 0.6)
    elif obs['joints'][5] > 0:
        print(obs['desired_goal'][2], obs['achieved_goal'], abs(obs['desired_goal'][2] - obs['achieved_goal'][2]))
        action = np.array([0, 0, 0, 0, 0, -0.3])
        gripper_closed = True
    elif obs['achieved_goal'][2] > 0.30:
        print("HI", obs['desired_goal'][2], obs['achieved_goal'][2], abs(obs['desired_goal'][2] - obs['achieved_goal'][2]))
        diff = [0, 0, -0.1]
        action = gym_replab.utils.compute_ik_command(diff, ik) / 3
        action = np.append(action, -0.3)
    else:
        break
    action = np.clip(np.array(action, dtype=np.float32), \
        env.action_space.low, env.action_space.high)
    obs, reward, next_obs, done = env.step(action)
