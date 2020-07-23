import gym
import gym_replab
from widowx200_core.ik import InverseKinematics
import numpy as np
import time
import argparse
import os
from PIL import Image

gym.make('Widow200RealRobotGraspV7-v0')._start_rospy().reset()
