import gym
import gym_replab
import numpy as np
from PIL import Image

images = []
env = gym.make('Widow200Drawer-v0', observation_mode='verbose', reward_type='sparse', \
    grasp_detector='background_subtraction', transpose_image=True)._start_rospy()

env.reset()
env.set_low_firmware_gains()
env.close_drawer()
obs = env.reset()

open = False
lift = False
move_to_grasp = False
lower = False
gripper_closed = False

for i in range(50):
    images.append(Image.fromarray(np.uint8(obs['render'])))
    print(obs['achieved_goal'])
    if np.linalg.norm(obs['achieved_goal'][:2] - np.array([0.265, -0.06])) > 0.015 and not open:
        target = np.array([0.265, -0.06, 0.16])
        wrist_target = 0 if abs(obs['joints'][4]) < (obs['joints'][4] - 2.6) else 2.6
        diff = target - obs['achieved_goal']
        wrist_diff = wrist_target -  obs['joints'][4]
        diff *= 5
        gripper = 0.7
        action = np.append(diff, [[wrist_diff * 3, gripper]])
    elif np.linalg.norm(obs['achieved_goal'][2] - 0.07) > 0.015 and not open:
        target = np.array([0.265, -0.06, 0.07])
        wrist_target = 0 if abs(obs['joints'][4]) < (obs['joints'][4] - 2.6) else 2.6
        diff = target - obs['achieved_goal']
        wrist_diff = wrist_target -  obs['joints'][4]
        diff *= 5
        gripper = 0.7
        action = np.append(diff, [[wrist_diff * 3, gripper]])
    elif np.linalg.norm(obs['achieved_goal'][:2] -  np.array([0.265, -0.18])) > 0.01 and not lift:
         target = np.array([0.265, -0.18, 0.07])
         wrist_target = 0 if abs(obs['joints'][4]) < (obs['joints'][4] - 2.6) else 2.6
         diff = target - obs['achieved_goal']
         wrist_diff = wrist_target -  obs['joints'][4]
         diff *= 5
         diff[1] *= 5
         gripper = 0.7
         action = np.append(diff, [[wrist_diff * 3, gripper]])
         open = True
    elif obs['achieved_goal'][2] - 0.17 < -0.01 and not move_to_grasp:
         target = np.array([0.14, -0.13, 0.24])
         wrist_target = 0 if abs(obs['joints'][4]) < (obs['joints'][4] - 2.6) else 2.6
         diff = target - obs['achieved_goal']
         wrist_diff = wrist_target -  obs['joints'][4]
         diff *= 5
         diff[2] *= 4
         gripper = 0.7
         action = np.append(diff, [[wrist_diff * 3, gripper]])
         lift = True
    elif np.linalg.norm(obs['achieved_goal'][:2] - np.array([0.259, -0.04])) > 0.006 and not lower:
        target = np.array([0.26, -0.04, 0.17])
        wrist_target = 1.2
        diff = target - obs['achieved_goal']
        wrist_diff = wrist_target -  obs['joints'][4]
        diff *= 5
        gripper = 0.7
        action = np.append(diff, [[wrist_diff * 3, gripper]])
        move_to_grasp = True
    elif np.linalg.norm(obs['achieved_goal'][2] - 0.058) > 0.01 and not gripper_closed:
        target = np.array([0.26, -0.04, 0.06])
        wrist_target = 1.2
        diff = target - obs['achieved_goal']
        wrist_diff = wrist_target -  obs['joints'][4]
        diff *= 5
        gripper = 0.7
        action = np.append(diff, [[wrist_diff * 3, gripper]])
        lower = True
        print("LOWERING")
    elif obs['joints'][5] > 0.3:
        diff = np.array([0, 0, 1], dtype='float64')
        wrist_diff = 0
        gripper_closed = True
        gripper = -0.7
        action = np.append(diff, [[wrist_diff * 3, gripper]])
    else:
        break

    action = gym_replab.utils.add_noise_custom(action, noise_stds=np.array([0.1, 0.1, 0.1, 0.1, 0.1]) / 3)
    action = gym_replab.utils.clip_action(action)
    next_obs, reward, done, info = env.step(action)
    obs = next_obs
