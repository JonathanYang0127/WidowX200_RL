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
                        if 'gif' in data_file:
                    break
            break

    if args.batch_size == -1:
        training_pool.save(['s'], save_dir,
            'combined_training_pool.pkl')
        #validation_pool.save(['s'], save_dir,
            #'combined_validation_pool.pkl')
    print(counter)


if __name__ == '__main__':
    combine_data(data_dirs)
