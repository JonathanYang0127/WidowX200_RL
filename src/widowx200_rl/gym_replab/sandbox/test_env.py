import gym
import gym_replab

env = gym.make('widow200graspv5-v0', observation_mode='verbose', reward_type='sparse', \
    grasp_detector='background_subtraction', transpose_image = True)._start_rospy()
env.reset()
env.step([0, 0, 0, 0, -1, 0])
env.step([0, 0, 0, 0, 1, 0])
env.step([0, 0, 0, 0, -1, 0])
