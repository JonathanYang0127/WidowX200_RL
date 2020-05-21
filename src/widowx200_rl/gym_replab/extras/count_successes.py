import os
import pickle as pkl

data_dir = '/home/jonathan/Desktop/Projects/WidowX200_RL/src/widowx200_rl/gym_replab/data/WidowX200GraspV5'


def is_successful(data_file):
    with open(data_file, 'rb') as fp:
        data = pkl.load(fp)
    print(fp)
    return int(data['rewards'][len(data['rewards']) - 1]) == 1


def count_successes():
    #counts the success rate
    s = 0
    total = 0

    for root, dirs, files in os.walk(data_dir):
        for d in dirs:
            total += 1
            for r1, d1, f1 in os.walk(os.path.join(root, d)):
                for data_file in f1:
                    #total += 1
                    if 'pool' in data_file and 'joint' in data_file:
                        #total += 1
                        s += is_successful(os.path.join(r1, data_file))
                        break
                break
        break

    print('Success rate: {} / {}'.format(s, total))

count_successes()
