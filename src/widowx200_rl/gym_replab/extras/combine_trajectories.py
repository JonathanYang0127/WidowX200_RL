import os
import pickle as pkl
import gym_replab
import numpy as np
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-d','--data_dirs', nargs='+',
default=["""/home/jonathan/Desktop/Projects/WidowX200_RL/src/widowx200_rl/
gym_replab/data/WidowX200GraspV5ShortControlledNewHeight"""])
parser.add_argument('-s','--save_dir', default="""/home/jonathan/Desktop/Projects/
WidowX200_RL/src/widowx200_rl/gym_replab/data/WidowX200GraspV5ShortCombined""")
parser.add_argument("--success_only", dest="success_only",
    action="store_true", default=False)
parser.add_argument("--append_initial_image", dest="append_initial_image",
    action="store_true", default=False)
parser.add_argument("--batch_size", type=int, default=-1)
args = parser.parse_args()

data_dirs = args.data_dirs
save_dir = args.save_dir
training_pool = gym_replab.utils.DemoPool()
validation_pool = gym_replab.utils.DemoPool()
counter = 0
TRAINING_FREQUENCY = 1.0
buffer_number = 0


def is_successful(data_file):
    with open(data_file, 'rb') as fp:
        data = pkl.load(fp)
    return int(data['rewards'][len(data['rewards']) - 1]) == 1


def add_trajectory(data_file):
    global counter
    with open(data_file, 'rb') as fp:
        data = pkl.load(fp)

    pool_type = np.random.rand()
    initial_obs = data['observations'][0][0]['image']
    for arr_obs, arr_action, arr_nobs, arr_reward, arr_done in zip(data['observations'], data['actions'], \
        data['next_observations'], data['rewards'], data['terminals']):
        obs, action, nobs, reward, done = arr_obs[0], arr_action, arr_nobs[0], arr_reward[0], arr_done[0]
        if args.append_initial_image:
            obs['image'] = np.append(obs['image'], initial_obs, axis=0)
            nobs['image'] = np.append(nobs['image'], initial_obs, axis=0)
        if pool_type < TRAINING_FREQUENCY:
            training_pool.add_sample(obs, action, nobs, reward, done)
        else:
            validation_pool.add_sample(obs, action, nobs, reward, done)
    if pool_type < TRAINING_FREQUENCY:
        counter += 1

def combine_data(data_dirs):
    global training_pool, buffer
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    else:
        os.system('rm -rf {}'.format(save_dir))
        os.makedirs(save_dir)
    counter = 0
    for data_dir in data_dirs:
        for root, dirs, files in os.walk(data_dir):
            for d in dirs:
                for r1, d1, f1 in os.walk(os.path.join(root, d)):
                    for data_file in f1:
                        if 'pool' in data_file and 'xyz' in data_file:
                            print(data_file)
                            f = os.path.join(r1, data_file)
                            if args.success_only and not is_successful(f):
                                continue
                            counter += 1
                            if counter == args.batch_size:
                                counter = 0
                                training_pool.save(['s'], save_dir,
                                    'combined_training_pool_{}.pkl'.format(buffer_number))
                                buffer_number += 1
                                training_pool = gym_replab.utils.DemoPool()
                                #validation_pools.append(gym_replab.utils.DemoPool())
                            add_trajectory(f)
                    break
            break

    if args.batch_size == -1:
        print(save_dir)
        training_pool.save(['s'], save_dir,
            'combined_training_pool.pkl')
        #validation_pool.save(['s'], save_dir,
            #'combined_validation_pool.pkl')
    print(counter)


if __name__ == '__main__':
    combine_data(data_dirs)
