from railrl.data_management.obs_dict_replay_buffer import \
    ObsDictReplayBuffer
import pickle
import numpy as np

file = '/home/jonathan/Desktop/Projects/WidowX200_RL/src/widowx200_rl/gym_replab/data/WidowX200GraspV5Combined/combined_training_pool.pkl'
with open(file, 'rb') as f:
    data = pickle.load(f)


new_data = dict()

observations = []
next_observations = []
actions = []
rewards = []
terminals = []


for arr_obs, arr_action, arr_nobs, arr_reward, arr_done in zip(data['observations'], data['actions'], \
    data['next_observations'], data['rewards'], data['terminals']):
    o, a, next_o, r, d = arr_obs[0], arr_action, arr_nobs[0], arr_reward[0], arr_done[0]
    observations.append(o)
    rewards.append(r)
    terminals.append(d)
    actions.append(a)
    next_observations.append(next_o)

actions = np.array(actions)
if len(actions.shape) == 1:
    actions = np.expand_dims(actions, 1)
observations = np.array(observations)
next_observations = np.array(next_observations)

rewards = np.array(rewards)
if len(rewards.shape) == 1:
    rewards = rewards.reshape(-1, 1)
data = dict(
    observations=observations,
    actions=actions,
    rewards=rewards,
    next_observations=next_observations,
    terminals=np.array(terminals).reshape(-1, 1),
)
with open(file, 'wb') as f:
    pickle.dump(data, f)
