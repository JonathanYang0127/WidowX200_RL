from gym.envs.registration import register
from . import envs

register(id='widowx200-v0',
         entry_point='gym_replab.envs:WidowX200EnvJoint',
         )

print("HI")
