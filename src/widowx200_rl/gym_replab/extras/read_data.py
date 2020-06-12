import os
import pickle as pkl
import numpy as np


def read_data(data_file):
    with open(data_file, 'rb') as fp:
        data = pkl.load(fp)
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
    #print(len(data['terminals'])/c)
    print(c, d)

#read_data('/root/ros_ws/src/replab/replab_rl/gym_replab/data/WidowGraspASDF/2020-02-02T22-01-08/2020-02-02T22-01-08_pool_70.pkl')
#read_data('/root/ros_ws/src/replab/replab_rl/gym_replab/data/WidowGraspModified/2020-02-01T05-02-09/2020-02-01T05-02-09_pool_70.pkl')
#read_data('/home/jonathan/Desktop/data_continuous/combined_training_pool.pkl')

#read_data('/home/jonathan/Desktop/Projects/WidowX200_RL/src/widowx200_rl/gym_replab/data/WidowX200GraspV5ShortCombined/combined_training_pool.pkl')
read_data('/home/jonathan/Desktop/Projects/WidowX200_RL/src/widowx200_rl/gym_replab/data/WidowX200GraspV5ShortCombined/combined_training_pool.pkl')
#read_data('/home/jonathan/Desktop/Projects/WidowX200_RL/src/widowx200_rl/gym_replab/data/WidowX200GraspV5ShortCombinedContinuous/combined_training_pool.pkl')
