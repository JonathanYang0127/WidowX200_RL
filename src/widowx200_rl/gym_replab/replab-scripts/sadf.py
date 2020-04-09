
import gym_replab
from widowx200_core.ik import InverseKinematics
import numpy as np
import time
import argparse
import os
from PIL import Image
depth_image_service = gym_replab.utils.KinectImageService('sd_pts')
pc_data = gym_replab.utils.get_center_and_second_pc(depth_image_service)
