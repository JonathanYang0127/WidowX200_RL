import os
import pickle as pkl
import gym_replab
import numpy as np

dirs = ['/home/jonathan/Desktop/Projects/WidowX200_RL/src/widowx200_rl/gym_replab/data/WidowX200GraspV5Short',
   '/home/jonathan/Desktop/Projects/WidowX200_RL/src/widowx200_rl/gym_replab/data/WidowX200GraspV5ShortPixelState']

save_dir = '/home/jonathan/Desktop/Projects/WidowX200_RL/src/widowx200_rl/gym_replab/data/WidowX200GraspV5ShortCombinedContinuous'
training_pool = gym_replab.utils.DemoPool()
validation_pool = gym_replab.utils.DemoPool()
counter = 0
TRAINING_FREQUENCY = 1.0
RELABEL = True



def add_trajectory(data_file):
    global counter
    #if 'WidowX200GraspV5Short' in data_file and 'modified' not in data_file:
    #    counter += 1
        #print("*SDFSDFSD", data_file)
        #print("HI")
        #return
    with open(data_file, 'rb') as fp:
        data = pkl.load(fp)

    if len(data['observations'][0][0]['state']) != 9:
        return

    pool_type = np.random.rand()
    object_grasped = data['rewards'][-1][0] == 1
    #print(object_grasped)
    for arr_obs, arr_action, arr_nobs, arr_reward, arr_done in zip(data['observations'], data['actions'], \
        data['next_observations'], data['rewards'], data['terminals']):
        obs, action, nobs, reward, done = arr_obs[0], arr_action, arr_nobs[0], arr_reward[0], arr_done[0]
        #print(len(nobs['state']), data_file)
        assert len(nobs['state']) == 9
        if RELABEL:
            if nobs['state'][2] > 0.14 and action[4] == -1 and object_grasped:
                reward = 1
            done = False

        if pool_type < TRAINING_FREQUENCY:
            training_pool.add_sample(obs, action, nobs, reward, done)
        else:
            validation_pool.add_sample(obs, action, nobs, reward, done)
    #if pool_type < TRAINING_FREQUENCY:
        #counter += 1


def combine_data(data_dirs):
    global counter
    for data_dir in data_dirs:
        for root, dirs, files in os.walk(data_dir):
            for d in dirs:
                c = False
                for r1, d1, f1 in os.walk(os.path.join(root, d)):
                    for data_file in f1:
                        if 'pool' in data_file and 'xyz' in data_file:
                            counter += 1
                            add_trajectory(os.path.join(r1, data_file))
                            c = True
                    break
            break


if __name__ == '__main__':
    combine_data(dirs)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    else:
        os.system('rm -rf {}'.format(save_dir))
        os.makedirs(save_dir)

    training_pool.save(['s'], save_dir,
        'combined_training_pool.pkl')
    #validation_pool.save(['s'], save_dir,
    #    'combined_validation_pool.pkl')
    print(counter)
