import gym
import gym_replab
import numpy as np
from PIL import Image

images = []
env = gym.make('Widow200Drawer-v0', observation_mode='verbose', reward_type='sparse', \
    grasp_detector='background_subtraction', transpose_image=True)._start_rospy()
obs = env.reset()
for i in range(10):
    images.append(Image.fromarray(np.uint8(obs['render'])))
    print(obs['achieved_goal'])
    target = np.array([0.26, -0.07, 0.16])
    wrist_target = 0
    diff = target - obs['achieved_goal']
    wrist_diff = wrist_target -  obs['joints'][4]
    diff *= 5
    gripper = 0.7
    action = np.append(diff, [[wrist_diff * 3, gripper]])
    next_obs, reward, done, info = env.step(action)
    obs = next_obs

for i in range(5):
    images.append(Image.fromarray(np.uint8(obs['render'])))
    print(obs['achieved_goal'])
    target = np.array([0.26, -0.07, 0.08])
    wrist_target = 0
    diff = target - obs['achieved_goal']
    wrist_diff = wrist_target -  obs['joints'][4]
    diff *= 5
    gripper = 0.7
    action = np.append(diff, [[wrist_diff * 3, gripper]])
    next_obs, reward, done, info = env.step(action)
    obs = next_obs

for i in range(10):
    images.append(Image.fromarray(np.uint8(obs['render'])))
    print(obs['achieved_goal'])
    target = np.array([0.26, -0.17, 0.08])
    wrist_target = 0
    diff = target - obs['achieved_goal']
    wrist_diff = wrist_target -  obs['joints'][4]
    diff *= 5
    diff[1] *= 3
    gripper = 0.7
    action = np.append(diff, [[wrist_diff * 3, gripper]])
    next_obs, reward, done, info = env.step(action)
    obs = next_obs


for i in range(10):
    images.append(Image.fromarray(np.uint8(obs['render'])))
    print(obs['achieved_goal'])
    target = np.array([0.14, -0.1, 0.24])
    wrist_target = 0
    diff = target - obs['achieved_goal']
    wrist_diff = wrist_target -  obs['joints'][4]
    diff *= 5
    diff[2] *= 5
    gripper = 0.7
    action = np.append(diff, [[wrist_diff * 3, gripper]])
    next_obs, reward, done, info = env.step(action)
    obs = next_obs



images[0].save('scripted_grasp.gif',
               format='GIF', append_images=images[1:],
               save_all=True, duration=2000, loop=0)
