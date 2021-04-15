import torch
import argparse
import pickle as pkl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--checkpoint", type=str, default="")
parser.add_argument("-f", "--file", type=str)
args = parser.parse_args()


def analyze_trajectory(data_file):
    with open(data_file, 'rb') as fp:
        data = pkl.load(fp)
    for i in range(len(data['observations'])):
        print(data['actions'][i])
        grid = np.zeros((20, 20))
        for j in range(20):
            for k in np.arange(20):
                data['actions'][i][:2] = [-1 + 0.1 * k, -1 + 0.1 * j]
                grid[j][k] = qf1(torch.FloatTensor([data['observations'][i][0]['image']]).cuda(), torch.FloatTensor([data['observations'][i][0]['state']]).cuda(),
                    torch.FloatTensor([data['actions'][i]]).cuda())
        sns.heatmap(grid)
        plt.show()

with open(args.checkpoint, 'rb') as f:
    checkpoint = torch.load(f)

qf1 = checkpoint['trainer/trainer'].qf1
analyze_trajectory(args.file)


