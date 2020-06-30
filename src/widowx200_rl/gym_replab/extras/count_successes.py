import os
import pickle as pkl
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--data_dir", type=str,
default="""/home/jonathan/Desktop/Projects/WidowX200_RL/src/widowx200_rl/
gym_replab/data/WidowX200GraspV5""")
parser.add_argument("--plot_grasp_locations", dest="plot_grasp_locations",
            action="store_true", default=False)
args = parser.parse_args()

data_dir = args.data_dir


def is_successful(data_file):
    with open(data_file, 'rb') as fp:
        data = pkl.load(fp)
    return int(data['rewards'][len(data['rewards']) - 1]) == 1


def add_goal(data_file, object_grasped):
    with open(data_file, 'rb') as fp:
        data = pkl.load(fp)
    goal = data['goal']
    if object_grasped:
        goals_success[0].append(goal[0])
        goals_success[1].append(goal[1])
    else:
        goals_fail[0].append(goal[0])
        goals_fail[1].append(goal[1])


def count_successes():
    #counts the success rate
    s = 0
    total = 0

    for root, dirs, files in os.walk(data_dir):
        for d in dirs:
            total += 1
            for r1, d1, f1 in os.walk(os.path.join(root, d)):
                if len(d1)+len(f1) < 3:
                    break
                for data_file in f1:
                    #total += 1
                    if 'pool' in data_file and 'joint' in data_file:
                        #total += 1
                        #print(data_file)
                        object_grasped = is_successful(os.path.join(r1, data_file))
                        s += object_grasped
                        if args.plot_grasp_locations:
                            ind = data_file.find('pool')
                            data_file = data_file[:ind] + 'params' + data_file[ind+4:]
                            add_goal(os.path.join(r1, data_file), object_grasped)
                break
        break

    print('Success rate: {} / {}'.format(s, total))

goals_success = [[], []]
goals_fail = [[], []]
count_successes()
if args.plot_grasp_locations:
    fig, ax = plt.subplots()
    sc1 = ax.scatter(goals_success[1], goals_success[0], color='g')
    #sc2 = ax.scatter(goals_fail[1], goals_fail[0], color='r')
    plt.xlim(-0.24, 0.16)
    plt.ylim(0.14, 0.38)
    plt.gca().invert_xaxis()
    plt.show()
    plt.pause(0.1)
