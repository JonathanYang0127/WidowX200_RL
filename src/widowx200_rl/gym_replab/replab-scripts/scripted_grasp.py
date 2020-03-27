import gym
import gym_replab
from widowx200_core.ik import InverseKinematics
import numpy as np

ik = InverseKinematics()
env = gym.make('widowx200-v0')._start_rospy()

def scripted_grasp(env, ik):
    env.set_goal([0.13, 0.08, 0.065])
    obs = env.reset()
    quat = ik.get_cartesian_pose()[3:]

    print(ik.get_cartesian_pose())

    gripper_closed = False
    for i in range(80):
        print(obs)
        if np.linalg.norm((obs['desired_goal'] - obs['achieved_goal'])[:2]) > 0.03 \
            and not gripper_closed:
            print( np.linalg.norm((obs['desired_goal'] - obs['achieved_goal'])[:2]) )
            diff = obs['desired_goal'] - obs['achieved_goal']
            diff[2] = 0.17 - obs['achieved_goal'][2]
            #print(diff[2])
            if np.linalg.norm(diff) < 0.06:
                diff[0] = diff[0] / np.linalg.norm(diff)
                diff[1] = diff[1] / np.linalg.norm(diff)
            action = gym_replab.utils.compute_ik_command(diff, quat, ik) / 4
            action = np.append(action, 0.6)
            print('Moving to object')
        elif abs(obs['desired_goal'][2] - obs['achieved_goal'][2]) > 0.01 \
            and not gripper_closed:
            print(obs['desired_goal'][2], obs['achieved_goal'][2], abs(obs['desired_goal'][2] - obs['achieved_goal'][2]))
            diff = obs['desired_goal'] - obs['achieved_goal']
            diff[2] -= 0.005
            action = gym_replab.utils.compute_ik_command(diff, quat, ik) / 3
            action = np.append(action, 0.6)
            print('Lowering arm')
        elif obs['joints'][5] > 0:
            print(obs['desired_goal'][2], obs['achieved_goal'], abs(obs['desired_goal'][2] - obs['achieved_goal'][2]))
            diff = np.array([0, 0, 0])
            action = gym_replab.utils.compute_ik_command(diff, quat, ik) / 3
            action = np.append(action, -0.3)
            gripper_closed = True
            print('Grasping object')
        elif obs['achieved_goal'][2] < 0.10:
            print(obs['desired_goal'][2], obs['achieved_goal'][2], abs(obs['desired_goal'][2] - obs['achieved_goal'][2]))
            diff = [0, 0, 0.1]
            action = gym_replab.utils.compute_ik_command(diff, quat, ik) / 3
            action = np.append(action, -0.3)
            print('Lifting object')
        else:
            diff = np.array([0, 0, 0.05])
            action = gym_replab.utils.compute_ik_command(diff, quat, ik) / 3
            action = np.append(action, -0.3)
            print('Done!')

        action = np.clip(np.array(action, dtype=np.float32), \
            env.action_space.low, env.action_space.high)
        next_obs, reward, done, info = env.step(action)
        obs = next_obs

if __name__ == '__main__':
    scripted_grasp(env, ik)
