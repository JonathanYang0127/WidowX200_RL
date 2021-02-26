from railrl.data_management.obs_dict_replay_buffer import \
    ObsDictReplayBuffer
import pickle
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str,
default="""/home/jonathan/Desktop/Projects/WidowX200_RL/src/widowx200_rl/
gym_replab/data/WidowX200GraspV5ShortCombined/combined_training_pool.pkl""")
parser.add_argument("--use_obs_dict_replay_buffer", dest="use_obs_dict_replay_buffer",
    action="store_true", default=False)
parser.add_argument("--e", "--env", type=str, required=True)
parser.add_argument('--s', type=str, default='buffer.pkl')
args = parser.parse_args()

file = args.file
with open(file, 'rb') as f:
    data = pickle.load(f)

new_data = dict()

observations = []
next_observations = []
actions = []
rewards = []
terminals = []

ret = 0
for arr_obs, arr_action, arr_nobs, arr_reward, arr_done in zip(data['observations'], data['actions'], \
    data['next_observations'], data['rewards'], data['terminals']):
    o, a, next_o, r, d = arr_obs[0], arr_action, arr_nobs[0], arr_reward[0], arr_done[0]
    observations.append(o)
    rewards.append(r)
    terminals.append(d)
    actions.append(a)
    next_observations.append(next_o)
    if r == 1:
        ret += 1

print(ret)

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


def add_buffer(b, buffer_data, path_length=1):
        buffer_size = len(buffer_data['actions'])
        assert buffer_size % path_length == 0

        for i in range(buffer_size // path_length):
            path = {}
            for key in buffer_data.keys():
                path[key] = buffer_data[key][path_length * i : path_length*(i + 1)]
            b.add_path(path)



if args.use_obs_dict_replay_buffer:
    from railrl.data_management.obs_dict_replay_buffer import \
        ObsDictReplayBuffer

    replay_buffer = ObsDictReplayBuffer(
        len(observations) + 1000,
        args.env,
        observation_keys=('image', 'state'),
    )

    add_buffer(replay_buffer, data)
    data = replay_buffer


with open(args.buffer, 'wb') as f:
    pickle.dump(data, f)
