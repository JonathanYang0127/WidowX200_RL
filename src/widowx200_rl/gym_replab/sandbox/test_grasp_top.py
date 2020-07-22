import gym
import gym_replab
import numpy as np
from PIL import Image

images = []
env = gym.make('Widow200Drawer-v0', observation_mode='verbose', reward_type='sparse', \
    grasp_detector='background_subtraction', transpose_image=True)._start_rospy()
obs = env.reset()

open = False
lift = False
move_to_grasp = False
lower = False
gripper_closed = False

for i in range(50):
    images.append(Image.fromarray(np.uint8(obs['render'])))
    print(obs['achieved_goal'])
    if np.linalg.norm(obs['achieved_goal'][:2] - np.array([0.265, 0.7])) > 0.015 and not open:
        target = np.array([0.265, 0.7, 0.18])
        wrist_target = 0
        diff = target - obs['achieved_goal']
        wrist_diff = wrist_target -  obs['joints'][4]
        diff *= 5
        gripper = 0.7
        action = np.append(diff, [[wrist_diff * 3, gripper]])
    else:
        break

    #action = gym_replab.utils.add_noise_custom(action, noise_stds=np.array([0.1, 0.1, 0.1, 0.1, 0.1]) / 3)
    #action = gym_replab.utils.clip_action(action)
    next_obs, reward, done, info = env.step(action)
    obs = next_obs
