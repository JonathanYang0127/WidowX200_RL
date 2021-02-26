import numpy as np
from .. import utils

def scripted_reach(obs):
    if np.linalg.norm((obs['desired_goal'] - obs['achieved_goal'])) > 0.015:
        diff = obs['desired_goal'] - obs['achieved_goal']
        diff *= 6
        #diff[2] /= 3
        wrist_diff = 0
        gripper = 0.7
    else:
        diff = obs['desired_goal'] - obs['achieved_goal']
        diff *= 6
        #diff[2] /= 3
        wrist_diff = 0
        gripper = 0.7

    action = np.append(diff, [[wrist_diff * 3, gripper]])
    action = utils.clip_action(action)

    return action, {'goal': obs['desired_goal']}
