from .color_pc_clusters import *
import os
import datetime
import numpy as np
import pickle
from distutils.util import strtobool
import math
import time
#from .color_pc_clusters import *
#from .kinect_image_service import *
from math import asin, sin, cos, sqrt, acos


def add_noise(diff):
    new_diff = np.copy(diff)
    new_diff += np.random.normal(0, 0.06, (3,)) - 0.0
    return new_diff


def enforce_normalization(diff):
    for i in range(3):
        sgn = np.sign(diff[i])
        if abs(diff[i]) > 1:
            diff[i] = sgn
        if abs(diff[i]) < 0.005:
            diff[i] = 0.005*sgn

    return diff


def compute_ik_command(action, low_clip, high_clip, quat=None, ik = None):
    action = np.array(action, dtype=np.float32)
    action /= 5
    pose = ik.get_cartesian_pose()
    pos = pose[:3]
    pos += action
    if quat is None:
        quat = pose[3:]

    return compute_ik_solution(pos, quat, low_clip, high_clip, ik)

def compute_ik_solution(pos, quat, low_clip, high_clip, ik):
    ik_command = ik._calculate_ik(pos, quat)[0][:5] - ik.get_joint_angles()[:5]

    ik_command /= 3.5
    if low_clip is not None:
        ik_command = np.clip(np.array(ik_command, dtype=np.float32), \
            low_clip, high_clip)

    for i in range(len(ik_command)):
        if abs(ik_command[i]) < 0.001:
            ik_command[i] = 0

    return ik_command

def timestamp(divider='-', datetime_divider='T'):
    now = datetime.datetime.now()
    return now.strftime(
        '%Y{d}%m{d}%dT%H{d}%M{d}%S'
        ''.format(d=divider, dtd=datetime_divider))

def str2bool(x):
    return bool(strtobool(x))

def get_rgb_image(kinect_image_service):
    return kinect_image_service.pull_image()

def get_center_and_second_pc(kinect_image_service):
    kinect_image_service.pull_image()
    return compute_center_and_pc()

def get_pc_object_center(kinect_image_service):
    kinect_image_service.pull_image()
    return get_pc_cluster_center()

def check_if_object_grasped(kinect_image_service):
    kinect_image_service.pull_image()
    return compute_center_and_pc() is None

def true_angle_diff(theta):
    """theta is before the absolute value is applied"""
    return min(abs(theta), abs(theta - 2 * np.pi))


class SafetyBox:
    def __init__(self):
        self.safety_box_low = np.array([-0.245, -0.225, 0.365], dtype='float32')
        self.safety_box_high = np.array([0.245, 0.225, 0.424], dtype='float32')
        self.action_space_low = 4 * np.array([-0.02, -0.01, -0.02, 0.0], dtype='float32')
        self.action_space_high = 4 * np.array([0.02, 0.01, 0.02, 0.5], dtype='float32')

    def clip_action(self, action):
        action = np.clip(np.array(action, dtype=np.float32), self.action_space_low, self.action_space_high)
        return action

    def enforce_safety_box(self, pose, action):
        curr_xyz_pos = pose[:3]
        clipped_commanded_next_xyz_pos = np.clip(curr_xyz_pos[:3] + action[:3], self.safety_box_low, self.safety_box_high)
        clipped_action = clipped_commanded_next_xyz_pos - curr_xyz_pos[:3]
        return np.append(clipped_action, np.array([[action[3]]], dtype='float32'))


class DemoPool:

    def __init__(self, max_size=1e6):
        self._keys = ('observations', 'actions', 'next_observations', 'rewards', 'terminals')
        self._fields = {}
        self._max_size = int(max_size)
        self._size = 0
        self._pointer = 0

    @property
    def size(self):
        return self._size


    def add_sample(self, *arrays):
        if self._size:
            self._add(arrays)
        else:
            self._init(arrays)

        self._advance()
        # print(self._size, self._pointer)

    def save(self, params, *savepath):
        savepath = os.path.join(*savepath)
        self._prune()
        save_info = [(key, self._fields[key].shape) for key in self._keys]
        print('[ DemoPool ] Saving to: {} | {}'.format(savepath, save_info))
        pickle.dump(self._fields, open(savepath, 'wb+'))

        ## save params
        params_path = savepath.replace('pool', 'params')
        pickle.dump(params, open(params_path, 'wb+'))

    def _add(self, arrays):
        for key, array in zip(self._keys, arrays):
            self._fields[key][self._pointer] = array

    def _init(self, arrays):
        for key, array in zip(self._keys, arrays):
            shape = array.shape if type(array) == np.ndarray else (1,)
            dtype = array.dtype if type(array) == np.ndarray else type(array)
            self._fields[key] = np.zeros((self._max_size, *shape), dtype=dtype)
            self._fields[key][self._pointer] = array
            # print(key, self._fields[key].shape, self._fields[key].dtype)

    def _advance(self):
        self._size = min(self._size + 1, self._max_size)
        self._pointer = (self._pointer + 1) % self._max_size

    def _prune(self):
        for key in self._keys:
            self._fields[key] = self._fields[key][:self._size]

    def get_samples(self):
        self._prune()
        return self._fields

class Meta:

    def __init__(self, fn, *args, **kwargs):
        self._fn = fn
        self._args = args
        self._kwargs = kwargs

    def __call__(self, *args, **kwargs):
        self._kwargs.update(**kwargs)
        return self._fn(*args, *self._args, **self._kwargs)
