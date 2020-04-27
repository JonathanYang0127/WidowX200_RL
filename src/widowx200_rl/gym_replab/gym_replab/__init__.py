from gym.envs.registration import register
import gym
from . import envs
from . import utils

register(id='widowx200-v0',
         entry_point='gym_replab.envs:WidowX200EnvJoint',
         )

register(id='widowx200jointhacked-v0',
         entry_point='gym_replab.envs:WidowX200EnvJointHacked',
         )

register(id='widowx200xyzhacked-v0',
         entry_point='gym_replab.envs:WidowX200EnvXYZHacked',
         )

def make(id, *args, **kwargs):
    return gym.make(id, *args, **kwargs)
