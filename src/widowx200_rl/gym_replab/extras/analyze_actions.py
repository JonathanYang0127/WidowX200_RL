import os
import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
import argparse


parser.add_argument("-f", "--file", type=str,
default="""/home/jonathan/Desktop/Projects/WidowX200_RL/src/widowx200_rl/
gym_replab/data/WidowX200GraspV5ShortCombined/combined_training_pool.pkl""")
args = parser.parse_args()


def read_data(data_file):
    with open(data_file, 'rb') as fp:
        data = pkl.load(fp)
    k = np.array([abs(i[0]) for i in data['actions'] if i[0] != 0])
    print(np.amin(k, axis=0))
    print(np.amin(np.abs(data['actions']), axis=0))
    print(np.amax(np.abs(data['actions']), axis=0))
    for i in range(6):
        plt.hist(data['actions'][:, i], bins=list(np.arange(-1, 1, 0.05)))
        plt.show()

read_data(args.file)
