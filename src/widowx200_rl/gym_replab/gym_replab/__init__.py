from gym.envs.registration import register
from . import envs
from . import utils

register(id='widowx200-v0',
         entry_point='gym_replab.envs:WidowX200EnvJoint',
         )

register(id='widowx200hacked-v0',
         entry_point='gym_replab.envs:WidowX200EnvJointHacked',
         )
