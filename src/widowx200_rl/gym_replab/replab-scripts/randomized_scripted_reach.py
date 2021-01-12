import gym
import gym_replab
from widowx200_core.ik import InverseKinematics
import numpy as np
import time
import argparse
import os
import sys
from PIL import Image
import torch
import pickle

V6_GRASPING_ENVS = ['Widow200RealRobotGraspV6-v0']


def make_dirs():
    global data_save_path, video_save_path, timestamp
    timestamp = gym_replab.utils.timestamp()
    data_save_path = os.path.join(__file__, "../..", 'data',
                                  args.data_save_directory, timestamp)
    data_save_path = os.path.abspath(data_save_path)
    video_save_path = os.path.join(data_save_path, "videos")

    if not os.path.exists(data_save_path):
        os.makedirs(data_save_path)
    if not os.path.exists(video_save_path) and args.video_save_frequency > 0:
        os.makedirs(video_save_path)


def scripted_reach_v6(env, data_xyz, data_joint, noise_stds, \
    save_video, image_save_dir=""):

    env.move_to_neutral()

    time.sleep(1.0)

    loop_counter = 0
    goal = np.zeros(3)
    goal[0] = np.random.uniform(0.2, 0.3)
    goal[1] = np.random.uniform(-.15, .1)
    goal[2] = np.random.uniform(0.07, 0.12)
    print(goal)
    env.set_goal(goal)
    obs = env.reset()
    quat = ik.get_cartesian_pose()[3:]

    low_clip = env.action_space.low[:5]
    high_clip = env.action_space.high[:5]
    images = []

    for i in range(args.num_timesteps):
        print(obs['achieved_goal'], goal)
        images.append(Image.fromarray(np.uint8(obs['render'])))
        if np.linalg.norm((obs['desired_goal'] - obs['achieved_goal'])) > 0.01:
            diff = obs['desired_goal'] - obs['achieved_goal']
            diff *= 6
            #diff[2] /= 3
            print(diff, np.linalg.norm((obs['desired_goal'] - obs['achieved_goal'])))
            wrist_diff = 0
            gripper = 0.7
            reward = 0
            print('Moving to position')
        else:
            diff = obs['desired_goal'] - obs['achieved_goal']
            diff *= 6
            #diff[2] /= 3
            print(diff, np.linalg.norm((obs['desired_goal'] - obs['achieved_goal'])))
            wrist_diff = 0
            gripper = 0.7
            reward = 1
            print('Done')

        action = np.append(diff, [[wrist_diff * 3, gripper]])
        #action = gym_replab.utils.add_noise_custom(action, noise_stds=noise_stds)
        action = gym_replab.utils.clip_action(action)

        next_obs, _, done, info = env.step(action)
        print("REWARD:", reward)

        if info['timeout']:
            env.open_gripper()
            return None

        data_xyz.append([obs, action, next_obs, reward, done])
        data_joint.append([obs, info['joint_command'], next_obs, reward, done])
        obs = next_obs

        if done:
            break

    make_dirs()
    if save_video:
        images[0].save('{}/scripted_grasp.gif'.format(video_save_path),
                       format='GIF', append_images=images[1:],
                       save_all=True, duration=100, loop=0)
    return goal


def store_trajectory(data_xyz, data_joint, params=None):
    pool_xyz = gym_replab.utils.DemoPool()
    pool_joint = gym_replab.utils.DemoPool()

    for i in range(len(data_xyz)):
        obs, nobs = data_xyz[i][0], data_xyz[i][2]
        modified_obs = {'image': obs['image'], 'state': obs['state']}
        modified_nobs = {'image': nobs['image'], 'state': nobs['state']}

        data_xyz[i][0], data_xyz[i][2] = modified_obs, modified_nobs
        pool_xyz.add_sample(*(data_xyz[i]))

        obs, nobs = data_joint[i][0], data_joint[i][2]
        modified_obs = {'image': obs['image'], 'state': obs['state']}
        modified_nobs = {'image': nobs['image'], 'state': nobs['state']}

        data_joint[i][0], data_joint[i][2] = modified_obs, modified_nobs
        pool_joint.add_sample(*(data_joint[i]))

    pool_xyz.save(params, data_save_path,
          '{}_pool_{}_xyz.pkl'.format(timestamp, pool_xyz.size))
    pool_joint.save(params, data_save_path,
          '{}_pool_{}_joint.pkl'.format(timestamp, pool_joint.size))


def main(args):
    policy = None
    image0 = None

    for i in range(args.num_trajectories):
        #Make a new directory for each timestamp
        #make_dirs()

        data_xyz = []
        data_joint = []

        if args.env in V6_GRASPING_ENVS:
            noise_stds = [args.noise_std*3]*6
            noise_stds[4] = 0.1
            noise_stds[2] /= 3
            goal = scripted_reach_v6(env, data_xyz, data_joint, noise_stds, \
                (i%args.video_save_frequency) == 0, image_save_dir=args.image_save_dir)

        if goal is not None:
            store_trajectory(data_xyz, data_joint, {'goal': goal})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--env", type=str,
                        choices=tuple(V6_GRASPING_ENVS),
                        required=True)
    parser.add_argument("-d", "--data_save_directory", type=str, default="WidowX200GraspV5ShortTest")
    parser.add_argument("--noise_std", type=float, default=0.1)
    parser.add_argument("--num_trajectories", type=int, default=50000)
    parser.add_argument("--num_timesteps", type=int, default=15)
    parser.add_argument("--video_save_frequency", type=int,
                        default=1, help="Set to zero for no video saving")
    parser.add_argument("--image_save_dir", type=str, required=True)


    args = parser.parse_args()
    args.data_save_directory += "_noise_{}".format(args.noise_std)

    data_save_path = None
    video_save_path = None

    ik = InverseKinematics()
    env = gym.make(args.env, observation_mode='verbose', reward_type='sparse', \
        grasp_detector='background_subtraction', transpose_image=True)._start_rospy()
    env.set_default_firmware_gains()

    if args.image_save_dir != "":
        env.set_image_save_dir(args.image_save_dir)

    main(args)
