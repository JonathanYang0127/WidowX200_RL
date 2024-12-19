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

register(id='Widow200RealRobotGraspV5-v0',
         entry_point='gym_replab.envs:Widow200RealRobotGraspV5Env',
         )

register(id='Widow200RealRobotGraspV6-v0',
         entry_point='gym_replab.envs:Widow200RealRobotGraspV6Env',
         )

register(id='Widow200RealRobotGraspV7-v0',
         entry_point='gym_replab.envs:Widow200RealRobotGraspV7Env',
         )

register(id='Widow200ObstacleRemoval-v0',
         entry_point='gym_replab.envs:Widow200ObstacleRemovalEnv',
         )

register(id='Widow200Drawer-v0',
         entry_point='gym_replab.envs:Widow200DrawerEnv',
         )

register(id='Widow200DrawerOpen-v0',
         entry_point='gym_replab.envs:Widow200DrawerOpenEnv',
         )

register(id='Widow200DrawerGrasp-v0',
         entry_point='gym_replab.envs:Widow200DrawerGraspEnv',
         )


register(id='Widow200Place-v0',
         entry_point='gym_replab.envs:Widow200PlaceEnv',
         )

register(id='Widow200GraspV5-v0',
         entry_point='gym_replab.envs:Widow200GraspV5ProxyEnv',
         )


register(id='Widow200GraspV6-v0',
         entry_point='gym_replab.envs:Widow200GraspV6ProxyEnv',
         )

"""
Widow250 environments
"""

register(id='Widow250RealRobotGraspV6-v0',
         entry_point='gym_replab.envs:Widow250RealRobotGraspV6Env',
         )


def make(id, *args, **kwargs):
    return gym.make(id, *args, **kwargs)
