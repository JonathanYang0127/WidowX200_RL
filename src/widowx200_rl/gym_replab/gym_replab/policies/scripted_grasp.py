import numpy as np
import time
from .. import utils

class ScriptedGraspV6:
    def __init__(self, env, num_objects=1, noise_stds=None, goal_noise=[0.02, 0.02], image_save_dir=''):
        self.env = env
        self.num_objects = num_objects
        self.image_save_dir = image_save_dir
        self.noise_stds = noise_stds
        self.goal_noise = goal_noise
        self.background_image = None

        if self.noise_stds is None:
            self.noise_stds = [0, 0, 0, 0, 0, 0]


    def reset(self, requery_background=False, update_background=False):
        '''
        Scripted reach. Returns True is object found and False otherwise
        '''

        self.env.move_to_background_subtract()
        time.sleep(2.0)
        if self.background_image is not None and not requery_background and \
                self.env.failed_rollout_counter < self.env.failed_rollout_thresh:
            if update_background:
                self.background_image = utils.cv2.imread(self.image_save_dir + '/image0.png')
        else:
            self.env.failed_rollout_counter = 0
            next = input('Press t to take empty rgb image ')
            while next != 't':
                next = input('Press t to take empty rgb image ')
            self.background_image = utils.get_image(512, 512)[150:]
            next = input('Place object on tray and press c to continue ')
            while next != 'c':
                next = input('Place object on tray and press c to continue ')

        self.goal = utils.get_random_object_center(self.env, background_image=self.background_image,
                                                   num_objects=self.num_objects,
                                                   detection_mode='rgb', save_dir=self.image_save_dir)
        if self.goal is None:
            return False

        self.gripper_closed = False
        self.goal = self.finetune_goal(self.goal)
        self.env.set_goal(self.goal)

        self.random_rotate = np.random.uniform(-1.5, 1.5)

        return True


    def get_action(self, obs):
        print(obs['desired_goal'], obs['achieved_goal'])
        self.wrist_rotate = obs['joints'][5] + self.random_rotate
        self.wrist_rotate = min(2.6, self.wrist_rotate)

        self.gripper_closed = not self.env._is_gripper_open

        reduce_noise = False
        if np.linalg.norm((obs['desired_goal'] - obs['achieved_goal'])[:2]) > 0.09 \
                and not self.gripper_closed:
            diff = obs['desired_goal'] - obs['achieved_goal']
            diff[2] = 0.17 - obs['achieved_goal'][2]
            diff *= 5
            wrist_diff = self.wrist_rotate - obs['joints'][4]
            gripper = 0.7
        elif obs['achieved_goal'][2] - obs['desired_goal'][2] > 0.01 \
                and not self.gripper_closed:
            diff = obs['desired_goal'] - obs['achieved_goal']
            diff *= 2
            diff[2] *= 2
            wrist_diff = self.wrist_rotate - obs['joints'][4]
            gripper = 0.7
            reduce_noise = True
        elif obs['joints'][5] > 0.3:
            diff = np.array([0, 0, 0], dtype='float64')
            diff *= 5
            wrist_diff = 0
            gripper_closed = True
            gripper = -0.7
            reduce_noise = True
        elif obs['achieved_goal'][2] < self.env.reward_height_thresh + 0.001:
            diff = np.array([0, 0, 0], dtype='float64')
            diff[2] = 1
            wrist_diff = 0
            gripper = -0.7
        else:
            diff = np.array([0, 0, 1], dtype='float64')
            diff *= 5
            wrist_diff = 0
            gripper = -0.7
            reduce_noise = True

        action = np.append(diff, [[wrist_diff * 3, gripper]])
        if reduce_noise:
            action = utils.add_noise_custom(action, noise_stds=np.array(self.noise_stds) / 1.5)
        else:
            action = utils.add_noise_custom(action, noise_stds=self.noise_stds)

        action = utils.clip_action(action)

        return action, {'goal': obs['desired_goal']}


    def finetune_goal(self, goal):
        if goal[0] < 0.205:
            goal[0] += 0.01
        if goal[1] > 0:
            goal[1] += 0.035
        if goal[1] > 0.04:
            goal[1] += 0.01
        if goal[1] > 0.09:
            goal[0] -= 0.01
            goal[1] += 0.015
        if goal[1] < -0.04:
            goal[1] -= 0.02
        if goal[1] < -0.09:
            goal[1] -= 0.01
        if goal[1] < -0.14:
            goal[1] -= 0.01
        if goal[0] > 0.28:
            goal[0] += 0.025
        if goal[0] < 0.21:
            if goal[1] < -0.015:
                goal[1] -= 0.02
            if goal[1] > 0.09:
                goal[1] += 0.01
                goal[0] -= 0.01

        goal[0] += np.random.normal(0, self.goal_noise[0])
        goal[1] += np.random.normal(0, self.goal_noise[1])
        goal = np.append(goal[:2], 0.074)

        return goal