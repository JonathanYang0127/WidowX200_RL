import os
import pickle as pkl
import numpy as np
import gym_replab

data_dir = '/root/ros_ws/src/replab/replab_rl/gym_replab/data/WidowGraspX200GraspV5-2'

def read_data(data_file):
    pool = gym_replab.utils.DemoPool()
    with open(data_file, 'rb') as fp:
        data = pkl.load(fp)
    #print(data['observations'][0][0]['image'].shape)
    #print(data['actions'][100])
    #print(len(data['observations'][0][0]['state']))
    print(data['actions'][0])

#read_data('/root/ros_ws/src/replab/replab_rl/gym_replab/data/WidowGraspASDF/2020-02-02T22-01-08/2020-02-02T22-01-08_pool_70.pkl')
#read_data('/root/ros_ws/src/replab/replab_rl/gym_replab/data/WidowGraspModified/2020-02-01T05-02-09/2020-02-01T05-02-09_pool_70.pkl')
#read_data('/root/ros_ws/src/replab/replab_rl/gym_replab/data/asdf/2020-02-01T19-19-26/2020-02-01T19-19-26_pool_70.pkl')
read_data('/home/jonathan/Desktop/Projects/WidowX200_RL/src/widowx200_rl/gym_replab/data/WidowX200GraspV5-2/2020-05-21T14-07-01/2020-05-21T14-07-01_pool_24_xyz.pkl')


