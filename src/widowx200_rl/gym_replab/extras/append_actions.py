import os
import pickle as pkl
import gym_replab
import numpy as np

data_dir = '/home/jonathan/Desktop/Projects/WidowX200_RL/src/widowx200_rl/gym_replab/data/WidowX200GraspTrue'
pool = gym_replab.utils.DemoPool()
counter = 0


def add_trajectory(data_file):
    pool = gym_replab.utils.DemoPool()
    global counter
    with open(data_file, 'rb') as fp:
        data = pkl.load(fp)
    data1_file = data_file[:-7] + 'joint.pkl'
    with open(data1_file, 'rb') as fp:
        data1 = pkl.load(fp)

    pool_type = np.random.rand()
    for arr_obs, arr_action, arr_nobs, arr_reward, arr_done, arr_action1 in zip(data['observations'], data['actions'], \
        data['next_observations'], data['rewards'], data['terminals'], data1['actions']):
        obs, action, nobs, reward, done, action1 = arr_obs[0], arr_action, arr_nobs[0], arr_reward[0], arr_done[0], arr_action1
        pool.add_sample(obs, np.append(action, action1[5]), nobs, reward, done)


    pool.save(None, os.path.dirname(data_file),
          os.path.basename(data_file))

def combine_data():
    for root, dirs, files in os.walk(data_dir):
        for d in dirs:
            for r1, d1, f1 in os.walk(os.path.join(root, d)):
                for data_file in f1:
                    if 'pool' in data_file and 'xyz' in data_file:
                        add_trajectory(os.path.join(r1, data_file))
                break
        break

combine_data()
