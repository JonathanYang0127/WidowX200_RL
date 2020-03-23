import gym
import gym_replab

env = gym.make('widowx200-v0')._start_rospy()
env.reset()

