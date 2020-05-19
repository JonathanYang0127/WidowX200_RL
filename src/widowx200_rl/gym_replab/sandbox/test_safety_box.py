import gym
import gym_replab
from widowx200_core.ik import InverseKinematics
import numpy as np
import time
import argparse
import os
import sys
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("--data_save_directory", type=str, default="WidowX200GraspNewHacked")
parser.add_argument("--num_trajectories", type=int, default=1000)
parser.add_argument("--num_timesteps", type=int, default=40)
parser.add_argument("--video_save_frequency", type=int,
                    default=1, help="Set to zero for no video saving")

args = parser.parse_args()
data_save_path = None
video_save_path = None

ik = InverseKinematics()
env = gym.make('widowx200xyzhacked-v0')._start_rospy()
env.reset()


depth_image_service = env.depth_image_service
rgb_image_service = gym_replab.utils.KinectImageService('rgb')

for i in range(20):
    env.step([0, -1, 0, 0])
