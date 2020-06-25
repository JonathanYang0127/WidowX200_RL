import os
import pickle as pkl
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str,
default="""/home/jonathan/Desktop/Projects/WidowX200_RL/src/widowx200_rl/
gym_replab/data/WidowX200GraspV5ShortCombined/combined_training_pool.pkl""")
args = parser.parse_args()


def read_data(data_file):
    with open(data_file, 'rb') as fp:
        data = pkl.load(fp)
    print(len(data['observations']) / 15)
    #print(data['observations'][10][0]['image'])
    #print(len(data['observations']))
    #print(data['actions'][100])
    #print(len(data['observations'][0][0]['state']))
    #print(data['actions'][10])
    c = 0
    d = 0
    for i in range(len(data['terminals'])):
        if data['terminals'][i]:
            c += 1
        if data['rewards'][i]:
            d += 1
        for k in range(len(data['actions'][i])):
            if abs(data['actions'][i][k]) > 1:
                print("Magnitude greater than 1", k)
    #print(len(data['terminals'])/c
    print(c, d)

read_data(args.file)
