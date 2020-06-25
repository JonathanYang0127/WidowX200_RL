import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--data_dir", type=str,
default="""/home/jonathan/Desktop/Projects/WidowX200_RL/src/widowx200_rl/
gym_replab/data/WidowX200GraspV5""")
args = parser.parse_args()

data_dir = args.data_dir

def remove_bad_data():
    #removes empty directories
    delete = []
    count = 0

    for root, dirs, files in os.walk(data_dir):
        for d in dirs:
            count += 1
            for r1, d1, f1 in os.walk(os.path.join(root, d)):
                if len(d1)+len(f1) < 3:
                    delete.append(os.path.join(root, d))
                break
        break

    print(delete)
    for d in delete:
        os.system('rm -rf {}'.format(d))

    print(count)

remove_bad_data()
