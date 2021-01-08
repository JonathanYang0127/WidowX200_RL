import sys

import numpy as np
import rospy
from gym import spaces, utils
from gym_replab.envs.widow200_base import Widow250RealRobotBaseEnv
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats

sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
sys.path.append('/opt/ros/kinetic/lib/python2.7/dist-packages')

from .. import utils

REWARD_FAIL = 0.0
REWARD_SUCCESS = 1.0


class Widow250RealRobotGraspV6Env(Widow250RealRobotBaseEnv):
    def __init__(self, reward_type='sparse', **kwargs):
        super().__init__(**kwargs)
        self._reward_type = reward_type

        self.goal = None
        self.quat = np.array([0.5, 0.5, -0.5, 0.5], dtype=np.float32)

        self._is_gripper_open = True
        self._upwards_bias = 0.08

        self._gripper_closed = -0.3
        self._gripper_open = 0.6
        self.reward_height_thresh = 0.14

    def _set_action_space(self):
        # Normalized action space
        self.action_space = spaces.Box(low=np.array([-1, -1, -1, -1, -1]),
                                       high=np.array([1, 1, 1, 1, 1]),
                                       dtype=np.float32)

    def check_if_object_grasped(self):
        if self._grasp_detector == 'background_subtraction':
            self.move_to_background_subtract()
            rospy.sleep(0.5)
            print("Getting Image")
            # np.linalg.norm((obs['desired_goal'] - obs['achieved_goal'])[:2])
            image0 = utils.get_image(512, 512)[150:]
            rospy.sleep(0.2)
            self.drop_at_random_location(False)
            self.move_to_background_subtract()
            # self._image_puller = None
            # self._image_puller = utils.USBImagePuller()
            rospy.sleep(1.0)
            image1 = utils.get_image(512, 512)[150:]
            rospy.sleep(0.5)
            object_grasped = utils.grasp_success_sliding_window(
                image0, image1, True, save_path=self.image_save_dir)
            if object_grasped:
                print(
                    "**************Object Grasp Succeeded!!!*****************")
                return True
            else:
                print(
                    "****************Object Grasp Failed!!!******************")
                return False
        elif self._grasp_detector == 'depth':
            if utils.check_if_object_grasped_pc(self.depth_image_service):
                print(
                    "***************Object Grasp Succeeded!!!****************")
                return True
            else:
                print(
                    "****************Object Grasp Failed!!!******************")
                return False
        else:
            raise NotImplementedError

    def get_reward(self):
        if self.current_pos[
            2] > self.reward_height_thresh and not self._is_gripper_open:
            return REWARD_SUCCESS
        else:
            return REWARD_FAIL

    def get_observation(self):
        '''
        TODO: Set image obs
        '''
        # assert self.original_image is not None
        obs = {}

        if self._obs_mode == 'verbose':
            obs['observation'] = self.current_pos[:3]
            obs['joints'] = self.current_pos[3:3 + self.num_joints]
            obs['desired_goal'] = self.goal
            obs['achieved_goal'] = self.current_pos[:3]
            obs['gripper'] = self.current_pos[2 + self.num_joints]
            obs['image'] = self.pull_image()
            obs['render'] = self.render()
            obs['state'] = self.current_pos[3:3 + self.num_joints]
        elif self._obs_mode == 'pixel_state':
            obs['image'] = self.pull_image()
            obs['state'] = self.current_pos[3:3 + self.num_joints]
        elif self._obs_mode == 'pixels':
            obs['image'] = self.pull_image()
        return obs

    def _gripper_simulate(self, gripper_action):
        '''
        Determines gripper action given ik_command
        '''
        # is_gripper_open = self._is_gripper_open()
        is_gripper_open = self._is_gripper_open
        lift = False

        if gripper_action > 0.5 and is_gripper_open:
            # keep it open
            gripper = self._gripper_open
        elif gripper_action > 0.5 and not is_gripper_open:
            # gripper is currently closed and we want to open it
            gripper = self._gripper_open
            self._is_gripper_open = True
            self.open_gripper()
        elif gripper_action < -0.5 and not is_gripper_open:
            # keep it closed
            gripper = self._gripper_closed
        elif gripper_action < -0.5 and is_gripper_open:
            # gripper is open and we want to close it
            gripper = self._gripper_closed
            # we will also lift the object up a little
            lift = True
            self._is_gripper_open = False
            self.close_gripper()
        elif gripper_action <= 0.5 and gripper_action >= -0.5:
            # maintain current status
            if is_gripper_open:
                gripper = self._gripper_open
            else:
                gripper = self._gripper_closed
        else:
            raise NotImplementedError

        return gripper, lift

    def step(self, action):
        '''
        TODO: Change quaternion based on wrist rotation
        action: [x, y, z, wrist, gripper]
        '''
        action = np.array(action, dtype='float32')
        action = np.clip(action, self.action_space.low, self.action_space.high)
        gripper_command = action[4]

        action /= 3
        action[2] *= 4
        wrist = action[3]

        pos = self.ik.get_cartesian_pose()[:3]
        pos += action[:3]
        pos[2] += self._upwards_bias  # ik has a downwards bias for some reason
        pos = np.clip(np.array(pos, dtype=np.float32), self._safety_box.low,
                      self._safety_box.high)
        joint_action = utils.compute_ik_solution(pos, self.quat,
                                                 self.joint_space.low,
                                                 self.joint_space.high, self.ik)
        joint_action[self.num_joints - 2] = wrist

        gripper, lift = self._gripper_simulate(gripper_command)

        self.action_publisher.publish(joint_action)

        try:
            self.current_pos = np.array(rospy.wait_for_message(
                "/widowx_env/action/observation", numpy_msg(Floats),
                timeout=5).data)
            for i in range(3):
                if self.current_pos[i] < self._safety_box.low[i] or \
                        self.current_pos[i] > self._safety_box.high[i]:
                    print(i, self.current_pos[i], "SAFETY BOX VIOLATION")
                    return None, None, None, {'timeout': True}
        except:
            return None, None, None, {'timeout': True}

        if lift:
            rospy.sleep(0.2)
            moved = self.lift_object()
            print(self.current_pos[2])
            if not moved:
                return None, None, None, {'timeout': True}

        step_tuple = self._generate_step_tuple()

        # Add joint information to step tuple
        step_tuple[3]['joint_command'] = np.append(
            joint_action[:self.num_joints - 1],
            np.array([[gripper_command]], dtype='float32'))
        return step_tuple

    def set_goal(self, goal):
        self.goal = goal

    def _generate_step_tuple(self):
        info = {'timeout': False}

        reward = self.get_reward()

        return self.get_observation(), reward, False, info

    def reset(self, gripper=True):
        self.move_to_neutral()
        if gripper:
            self._is_gripper_open = True
            self.reset_publisher.publish("OPEN_GRIPPER")
        else:
            self.reset_publisher.publish("NO_GRIPPER")
        rospy.sleep(1.0)
        while True:
            try:
                self.get_observation_publisher.publish("GET_OBSERVATION")
                self.current_pos = np.array(rospy.wait_for_message(
                    "/widowx_env/action/observation", numpy_msg(Floats),
                    timeout=5).data)
                break
            except:
                continue
        return self.get_observation()