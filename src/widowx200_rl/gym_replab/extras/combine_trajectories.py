import os
import pickle as pkl
import gym_replab
import numpy as np

data_dir = '/home/jonathan/Desktop/Projects/WidowX200_RL/src/widowx200_rl/gym_replab/data/WidowX200GraspNew4'
save_dir = '/home/jonathan/Desktop/Projects/WidowX200_RL/src/widowx200_rl/gym_replab/data/WidowX200GraspNewJointCombined'
training_pool = gym_replab.utils.DemoPool()
validation_pool = gym_replab.utils.DemoPool()
counter = 0


def is_successful(data_file):
    with open(data_file, 'rb') as fp:
        data = pkl.load(fp)
    return int(data['rewards'][len(data['rewards']) - 1]) == 1


def add_trajectory(data_file):
    global counter
    with open(data_file, 'rb') as fp:
        data = pkl.load(fp)

    pool_type = np.random.rand()
    for arr_obs, arr_action, arr_nobs, arr_reward, arr_done in zip(data['observations'], data['actions'], \
        data['next_observations'], data['rewards'], data['terminals']):
        obs, action, nobs, reward, done = arr_obs[0], arr_action, arr_nobs[0], arr_reward[0], arr_done[0]
        if pool_type < 0.9:
            training_pool.add_sample(obs, action, nobs, reward, done)
        else:
            validation_pool.add_sample(obs, action, nobs, reward, done)
    if pool_type < 0.9:
        counter += 1

def combine_data():
    for root, dirs, files in os.walk(data_dir):
        for d in dirs:
            for r1, d1, f1 in os.walk(os.path.join(root, d)):
                for data_file in f1:
                    if 'pool' in data_file and 'joint' in data_file and is_successful(os.path.join(r1, data_file)):
                        add_trajectory(os.path.join(r1, data_file))
                break
        break


    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    else:
        os.system('rm -rf {}'.format(save_dir))
        os.makedirs(save_dir)

    training_pool.save(['s'], save_dir,
        'combined_training_pool.pkl')
    validation_pool.save(['s'], save_dir,
        'combined_validation_pool.pkl')
    print(counter)


if __name__ == '__main__':
    combine_data()
