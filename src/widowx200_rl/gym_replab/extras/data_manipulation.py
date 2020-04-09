import pickle as pkl
import os

data_dir = '/home/jonathan/Desktop/Projects/WidowX200_RL/src/widowx200_rl/gym_replab/data/WidowX200Grasp'


def is_successful(data_file):
    with open(data_file, 'rb') as fp:
        data = pkl.load(fp)
    return int(data['rewards'][len(data['rewards']) - 1]) == 1


def count_successes():
    #counts the success rate
    s = 0
    total = 0

    for root, dirs, files in os.walk(data_dir):
        for d in dirs:
            for r1, d1, f1 in os.walk(os.path.join(root, d)):
                for data_file in f1:
                    total += 1
                    if 'pool' in data_file:
                        s += is_successful(os.path.join(r1, data_file))
                break
        break

    print('Success rate: {} / {}'.format(s, total))


def compile_successes():
    #compiles the successful trajectories into data/WidowGraspSuccess
    os.system('rm -rf {}/*'.format(os.path.join(os.path.dirname(data_dir), 'WidowGraspSuccess')))

    successful = []
    for root, dirs, files in os.walk(data_dir):
        for d in dirs:
            for r1, d1, f1 in os.walk(os.path.join(root, d)):
                for data_file in f1:
                    if 'pool' in data_file:
                        if is_successful(os.path.join(r1, data_file)):
                            successful.append(os.path.join(root, d))
                break
        break

    for d in successful:
        print(d)
        os.system('cp -r {} {}'.format(d+'/', data_dir + '/../WidowGraspSuccess'))


remove_bad_data()
count_successes()
compile_successes()
