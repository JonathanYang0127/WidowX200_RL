import os
import pickle as pkl
import numpy as np
from widowx200_core.ik import InverseKinematics
import gym_replab

ik = InverseKinematics()
data_dir = '/home/jonathan/Desktop/Projects/WidowX200_RL/src/widowx200_rl/gym_replab/data/WidowX200GraspV5Short'


def apply_forwards_kinematics(data_file):
    with open(data_file, 'rb') as fp:
        data = pkl.load(fp)

    pool = gym_replab.utils.DemoPool()
    if 'xyz' in data_file:
        data_type = 'xyz'
    else:
        return

    obs = data['observations']
    next_obs = data['next_observations']

    for arr_obs, arr_action, arr_nobs, arr_reward, arr_done in zip(data['observations'], data['actions'], \
        data['next_observations'], data['rewards'], data['terminals']):
        obs, action, nobs, reward, done = arr_obs[0], arr_action, arr_nobs[0], arr_reward[0], arr_done[0]

        assert len(obs['state']) == 6
        joint_observation = obs['state']
        pose = np.array(ik.get_cartesian_pose(joint_observation)[:3])

        obs['state'] = np.append(pose, nobs['state'])

        joint_observation = nobs['state']
        pose = np.array(ik.get_cartesian_pose(joint_observation)[:3])

        nobs['state'] = np.append(pose, nobs['state'])

        pool.add_sample(obs, action, nobs, reward, done)

    if data_type == 'xyz':
        pool.save(None, os.path.dirname(data_file),
          'pool_{}_xyz_modified.pkl'.format(pool.size))




def walk():
    counter = 0
    for root, dirs, files in os.walk(data_dir):
        for d in dirs:
            for r1, d1, f1 in os.walk(os.path.join(root, d)):
                for data_file in f1:
                    if 'pool' in data_file and ('xyz' in data_file) and 'modified' not in data_file:
                        apply_forwards_kinematics(os.path.join(r1, data_file))
                        counter += 1
                        break
                break
        break
    print(counter)


walk()

#read_data('/root/ros_ws/src/replab/replab_rl/gym_replab/data/WidowGraspASDF/2020-02-02T22-01-08/2020-02-02T22-01-08_pool_70.pkl')
#read_data('/root/ros_ws/src/replab/replab_rl/gym_replab/data/WidowGraspModified/2020-02-01T05-02-09/2020-02-01T05-02-09_pool_70.pkl')
#read_data('/root/ros_ws/src/replab/replab_rl/gym_replabread_data('/home/jonathan/Desktop/Projects/WidowX200_RL/src/widowx200_rl/gym_replab/data/WidowX200GraspV5-2/2020-05-21T14-07-01/2020-05-21T14-07-01_pool_24_xyz.pkl')
