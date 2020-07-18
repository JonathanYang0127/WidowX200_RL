import gym
import numpy as np

env = gym.make('Widow200Drawer-v0', observation_mode='verbose', reward_type='sparse', \
    grasp_detector='background_subtraction', transpose_image=True)._start_rospy()
obs = env.reset()
for i in range(20):
    target = np.array(0.24, -0.04, 0.09)
    wrist_target = 1.2
    diff = target - obs['achieved_goal']
    wrist_diff = wrist_target -  obs['joints'][4]
    gripper = 0.7
    action = np.append(diff, [[wrist_diff * 3, gripper]])
    next_obs, reward, done, info = env.step(action)
    obs = next_obs
