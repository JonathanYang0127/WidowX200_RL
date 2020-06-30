import gym_replab
from railrl.data_management.obs_dict_replay_buffer import \
    ObsDictReplayBuffer
import pdb
import pickle

with open('/home/jonathan/Desktop/Projects/WidowX200_RL/src/widowx200_rl/gym_replab/data/Widow200RealRobotGraspV6Combined/combined_training_pool.pkl', 'rb') as f:
    data = pickle.load(f)

replay_buffer = ObsDictReplayBuffer(
    1000000,
    gym_replab.make('Widow200GraspV6-v0'),
    observation_keys=('image', 'state'))

replay_buffer.add_path(data)
pdb.set_trace()
