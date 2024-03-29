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

DRAWER_OPEN_AND_GRASP_ENVS = ['Widow200Drawer-v0']
DRAWER_OPEN_ENVS = ['Widow200DrawerOpen-v0']
DRAWER_GRASP_ENVS = ['Widow200DrawerGrasp-v0']
OBSTABLE_REMOVAL_ENVS = ['Widow200ObstacleRemoval-v0']


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


def scripted_drawer_open(env, data_xyz, data_joint, noise_stds, \
        save_video, policy=None, policy_rate=0.5, image_save_dir=""):

    obs = env.reset()
    images = []

    if policy is not None:
        try:
            action = policy(obs['image'])
            use_robot_state = False
        except:
            use_robot_state = True


    open = False
    lift = False
    move_to_grasp = False
    lower = False
    gripper_closed = False
    grasped = False
    neutral_command = False

    for i in range(args.num_timesteps):
        print(i)
        print("State:", obs['state'][2])
        finished_trajectory=False
        images.append(Image.fromarray(np.uint8(obs['render'])))
        if np.random.rand() < policy_rate:
            print("Checkpoint Policy")
            if use_robot_state:
                action, _ = policy(np.append(obs['image'], obs['state']))
            else:
                action, _ = policy(obs['image'])

        else:
            print("Scripted Policy1")
            images.append(Image.fromarray(np.uint8(obs['render'])))
            print(obs['achieved_goal'])
            if np.linalg.norm(obs['achieved_goal'][:2] - np.array([0.27, -0.06])) > 0.015 and not open:
                target = np.array([0.275, -0.06, 0.17])
                wrist_target = 0 if abs(obs['joints'][4]) < (obs['joints'][4] - 2.6) else 2.6
                diff = target - obs['achieved_goal']
                wrist_diff = wrist_target -  obs['joints'][4]
                wrist_diff *= 2
                diff *= 10
                gripper = 0.7
                neutral = 0.5
                print("MOVING TO HANDLE")
            elif np.linalg.norm(obs['achieved_goal'][2] - 0.068) > 0.013 and not open:
                target = np.array([0.28, -0.06, 0.068])
                wrist_target = 0 if abs(obs['joints'][4]) < (obs['joints'][4] - 2.6) else 2.6
                diff = target - obs['achieved_goal']
                wrist_diff = wrist_target -  obs['joints'][4]
                diff *= 6
                gripper = 0.7
                neutral = 0.5
                print("LOWERING")
            elif np.linalg.norm(obs['achieved_goal'][1] + 0.22) > 0.015 and not lift:
                target = np.array([0.24, -0.24, 0.07])
                wrist_target = 0 if abs(obs['joints'][4]) < (obs['joints'][4] - 2.6) else 2.6
                diff = target - obs['achieved_goal']
                wrist_diff = wrist_target -  obs['joints'][4]
                diff *= 5
                diff[1] *= 5
                gripper = 0.7
                open = True
                neutral = 0.5
                print("OPENING")
            elif obs['achieved_goal'][2] - 0.15 < -0.005 and not move_to_grasp:
                target = np.array([0.14, -0.14, 0.24])
                wrist_target = 0 if abs(obs['joints'][4]) < (obs['joints'][4] - 2.6) else 2.6
                diff = target - obs['achieved_goal']
                wrist_diff = wrist_target -  obs['joints'][4]
                diff *= 5
                diff[2] = 0.8
                gripper = 0.7
                lift = True
                neutral = 0.5
                print("LIFTING")
            elif not neutral_command:
                diff = np.array([0, 0, 1], dtype='float64')
                wrist_diff = 0
                gripper_closed = True
                gripper = 0.7
                neutral = -0.5
                neutral_command = True
                print("RESETING")
            else:
                break
                diff = np.array([0, 0, 0], dtype='float64')
                wrist_diff = 0
                gripper_closed = True
                gripper = 0.7
                neutral = 0.5
                finished_trajectory = True
                print("DONE!")

            action = np.append(diff, [[wrist_diff * 3, gripper, neutral]])
            action = gym_replab.utils.add_noise_custom(action, noise_stds=noise_stds)

        action = gym_replab.utils.clip_action(action)
        print(action)

        if action[4] < -0.5:
            gripper_closed = True
        elif action[4] > 0.5:
            gripper_closed = False


        next_obs, reward, done, info = env.step(action)
        print(obs['joints'][5], finished_trajectory)
        reward = 1 if finished_trajectory else 0
        print("REWARD:", reward)

        if info['timeout']:
            env.open_gripper()
            return None

        data_xyz.append([obs, action, next_obs, reward, done])
        data_joint.append([obs, info['joint_command'], next_obs, reward, done])
        obs = next_obs
       
        if done or action[5] < 0:
            env.open_gripper()
            break

    make_dirs()
    if save_video:
        images[0].save('{}/scripted_grasp.gif'.format(video_save_path),
                       format='GIF', append_images=images[1:],
                       save_all=True, duration=100, loop=0)


def scripted_drawer_grasp(env, data_xyz, data_joint, noise_stds, \
        save_video, policy=None, policy_rate=0.5, image_save_dir=""):

    obs = env.reset(lift=True)
    images = []

    if policy is not None:
        try:
            action = policy(obs['image'])
            use_robot_state = False
        except:
            use_robot_state = True


    open = False
    lift = False
    move_to_grasp = False
    lower = False
    gripper_closed = False
    grasped = False
    finished_trajectory=False

    random_rotate = np.random.uniform(-0.7, 0.7)
    #random_rotate = 0.5
    #xyz_offset = np.random.uniform(0, 0.005)
    print('wrist', random_rotate)
    print(obs['joints'])
    wrist_target = obs['joints'][4] + random_rotate
    images = []
    vertical_offset = np.random.uniform(0, 0.022) - 0.02
    horizontal_offset = np.random.uniform(0, 0.01) - 0.005
    if np.abs(random_rotate) < 0.3:
        horizontal_offset = np.random.uniform(-0.01, 0.022)
    #vertical_offset = 0.02

    for i in range(args.num_timesteps):
        print(i)
        print("State:", obs['state'][2])
        images.append(Image.fromarray(np.uint8(obs['render'])))
        if np.random.rand() < policy_rate:
            print("Checkpoint Policy")
            if use_robot_state:
                action, _ = policy(np.append(obs['image'], obs['state']))
            else:
                action, _ = policy(obs['image'])
            if np.linalg.norm(obs['achieved_goal'][2] - 0.085) < 0.016:
                action[4] = -0.7
            action = gym_replab.utils.add_noise_custom(action, noise_stds=[0, 0, 0, 0, 0.1, 0])


        else:
            print("Scripted Policy1")
            images.append(Image.fromarray(np.uint8(obs['render'])))
            print(obs['achieved_goal'])
            if np.linalg.norm(obs['achieved_goal'][:2] - np.array([0.258 + vertical_offset / 2, -0.04 + horizontal_offset / 2])) > 0.01 and not lower and not grasped:
                target = np.array([0.257 + vertical_offset, -0.04 + horizontal_offset, 0.18])
                diff = target - obs['achieved_goal']
                wrist_diff = wrist_target -  obs['joints'][4]
                diff *= 7
                diff[0] *= 1.5
                gripper = 0.7
                move_to_grasp = True
                neutral = 0.5
            elif np.linalg.norm(obs['achieved_goal'][2] - 0.085) > 0.013 and not grasped:
                target = np.array([0.257 + vertical_offset, -0.04 + horizontal_offset, 0.085])
                diff = target - obs['achieved_goal']
                wrist_diff = wrist_target -  obs['joints'][4]
                diff *= 5
                diff[2] *= 20
                gripper = 0.7
                lower = True
                neutral = 0.5
            elif obs['joints'][5] > 0.3:
                diff = np.array([0, 0, 1], dtype='float64')
                wrist_diff = 0
                gripper_closed = True
                grasped = True
                gripper = -0.7
                neutral = 0.5
            else:
                diff = np.array([0, 0, 0.1], dtype='float64')
                wrist_diff = 0
                gripper_closed = True
                gripper = -0.7
                finished_trajectory=True
                neutral = 0.5

            action = np.append(diff, [[wrist_diff * 3, gripper, neutral]])
            action = gym_replab.utils.add_noise_custom(action, noise_stds=noise_stds)

        action[3] = (wrist_target -  obs['joints'][4]) * 3
        action = gym_replab.utils.clip_action(action)
        print(action)

        if action[4] < -0.5:
            grasped = True
            finished_trajectory=True
            gripper_closed = True
        elif action[4] > 0.5:
            gripper_closed = False


        next_obs, reward, done, info = env.step(action)
        print(obs['joints'][5], finished_trajectory)
        reward = 1 if finished_trajectory else 0
        print("REWARD:", reward)

        if info['timeout']:
            env.open_gripper()
            return None

        data_xyz.append([obs, action, next_obs, reward, done])
        data_joint.append([obs, info['joint_command'], next_obs, reward, done])
        obs = next_obs

        if done:
            env.open_gripper()
            break

    make_dirs()
    if save_video:
        images[0].save('{}/scripted_grasp.gif'.format(video_save_path),
                       format='GIF', append_images=images[1:],
                       save_all=True, duration=100, loop=0)


def scripted_drawer_open_and_grasp(env, data_xyz, data_joint, noise_stds, \
        save_video, policy=None, policy_rate=0.5, image_save_dir=""):

    obs = env.reset()
    images = []

    if policy is not None:
        try:
            action = policy(obs['image'])
            use_robot_state = False
        except:
            use_robot_state = True


    open = False
    lift = False
    move_to_grasp = False
    lower = False
    gripper_closed = False
    grasped = False

    for i in range(args.num_timesteps):
        print(i)
        print("State:", obs['state'][2])
        finished_trajectory=False
        images.append(Image.fromarray(np.uint8(obs['render'])))
        if np.random.rand() < policy_rate:
            print("Checkpoint Policy")
            if use_robot_state:
                action, _ = policy(np.append(obs['image'], obs['state']))
            else:
                action, _ = policy(obs['image'])

        else:
            print("Scripted Policy1")
            images.append(Image.fromarray(np.uint8(obs['render'])))
            print(obs['achieved_goal'])
            if np.linalg.norm(obs['achieved_goal'][:2] - np.array([0.265, -0.06])) > 0.015 and not open:
                target = np.array([0.26, -0.06, 0.17])
                wrist_target = 0 if abs(obs['joints'][4]) < (obs['joints'][4] - 2.6) else 2.6
                diff = target - obs['achieved_goal']
                wrist_diff = wrist_target -  obs['joints'][4]
                wrist_diff *= 2
                diff *= 10
                gripper = 0.7
            elif np.linalg.norm(obs['achieved_goal'][2] - 0.07) > 0.015 and not open:
                target = np.array([0.26, -0.06, 0.07])
                wrist_target = 0 if abs(obs['joints'][4]) < (obs['joints'][4] - 2.6) else 2.6
                diff = target - obs['achieved_goal']
                wrist_diff = wrist_target -  obs['joints'][4]
                diff *= 6
                gripper = 0.7
            elif np.linalg.norm(obs['achieved_goal'][1] + 0.19) > 0.01 and not lift:
                target = np.array([0.265, -0.2, 0.07])
                wrist_target = 0 if abs(obs['joints'][4]) < (obs['joints'][4] - 2.6) else 2.6
                diff = target - obs['achieved_goal']
                wrist_diff = wrist_target -  obs['joints'][4]
                diff *= 5
                diff[1] *= 5
                gripper = 0.7
                open = True
            elif obs['achieved_goal'][2] - 0.1 < -0.005 and not move_to_grasp:
                target = np.array([0.14, -0.12, 0.24])
                wrist_target = 0 if abs(obs['joints'][4]) < (obs['joints'][4] - 2.6) else 2.6
                diff = target - obs['achieved_goal']
                wrist_diff = wrist_target -  obs['joints'][4]
                diff *= 5
                diff[2] = 0.8
                gripper = 0.7
                lift = True
            elif obs['joints'][5] > 0.3 and not move_to_grasp:
                diff = np.array([0, 0, 1], dtype='float64')
                wrist_diff = 0
                gripper_closed = True
                gripper = -0.7
            elif np.linalg.norm(obs['achieved_goal'][:2] - np.array([0.258, -0.04])) > 0.008 and not lower:
                target = np.array([0.256, -0.04, 0.18])
                wrist_target = 1.2
                diff = target - obs['achieved_goal']
                wrist_diff = wrist_target -  obs['joints'][4]
                diff *= 7
                diff[0] *= 1.5
                gripper = -0.7
                move_to_grasp = True
            elif np.linalg.norm(obs['achieved_goal'][2] - 0.06) > 0.01 and not grasped:
                target = np.array([0.258, -0.04, 0.06])
                wrist_target = 1.2
                diff = target - obs['achieved_goal']
                wrist_diff = wrist_target -  obs['joints'][4]
                diff *= 5
                diff[2] *= 20
                gripper = 0.7
                lower = True
            elif obs['joints'][5] > 0.3:
                diff = np.array([0, 0, 1], dtype='float64')
                wrist_diff = 0
                gripper_closed = True
                grasped = True
                gripper = -0.7
            else:
                diff = np.array([0, 0, 0.1], dtype='float64')
                wrist_diff = 0
                gripper_closed = True
                gripper = -0.7
                finished_trajectory=True

            action = np.append(diff, [[wrist_diff * 3, gripper]])
            action = gym_replab.utils.add_noise_custom(action, noise_stds=noise_stds)

        action = gym_replab.utils.clip_action(action)
        print(action)

        if action[4] < -0.5:
            gripper_closed = True
        elif action[4] > 0.5:
            gripper_closed = False


        next_obs, reward, done, info = env.step(action)
        print(obs['joints'][5], finished_trajectory)
        reward = 1 if finished_trajectory else 0
        print("REWARD:", reward)

        if info['timeout']:
            env.open_gripper()
            return None

        data_xyz.append([obs, action, next_obs, reward, done])
        data_joint.append([obs, info['joint_command'], next_obs, reward, done])
        obs = next_obs

        if done:
            env.open_gripper()
            break

    make_dirs()
    if save_video:
        images[0].save('{}/scripted_grasp.gif'.format(video_save_path),
                       format='GIF', append_images=images[1:],
                       save_all=True, duration=100, loop=0)


def scripted_obstacle_removal(env, data_xyz, data_joint, noise_stds, detection_mode, image0, num_objects, \
    save_video, policy=None, policy_rate=0.5, image_save_dir=""):

    env.move_to_neutral()
    time.sleep(1.0)

    loop_counter = 0
    if detection_mode == 'depth':
        pc_data = gym_replab.utils.get_center_and_second_pc(depth_image_service)
        while pc_data is None or pc_data[0][0] >= 0.45:
            env.drop_at_random_location()
            env.move_to_neutral()
            pc_data = gym_replab.utils.get_center_and_second_pc(depth_image_service)
            loop_counter += 1
            if loop_counter >= 5:
                sys.exit(0)
        goal, object_vector = pc_data
    elif detection_mode == 'rgb':
        goal = gym_replab.utils.get_random_center_rgb(image0, num_objects, image_save_dir)
        while goal is None or goal[0] >= 0.45:
            env.drop_at_random_location()
            env.move_to_neutral()
            goal = gym_replab.utils.get_random_center_rgb(image0, num_objects, image_save_dir)
            loop_counter += 1
            if loop_counter >= 5:
                sys.exit(0)

    goal = np.append(goal, 0.055)
    print(goal)
    #goal[0] += np.random.uniform(low = -0.03, high = 0.03)
    #goal[1] += np.random.uniform(low = -0.03, high = 0.03)

    goal[0] += np.random.normal(0, 0.005)
    if goal[0] > 0.3:
        goal[0] += 0.02
    #if goal[0] < 0.22:
        #goal[0] -= 0.01
    if goal[1] < -0.03:
        goal[1] -= 0.02
    if goal[1] < -0.17:
        goal[1] -= 0.02
    if goal[1] > 0.04:
        goal[1] += 0.02
    goal[1] += np.random.normal(0, 0.006) #0.015

    goal[2] += np.random.uniform(low = -0.002, high = 0.005)


    print("GOAL HEIGHT: ", goal[2])
    goal = np.clip(goal, env._safety_box.low, env._safety_box.high)
    env.set_goal(goal)
    obs = env.reset()
    quat = ik.get_cartesian_pose()[3:]

    low_clip = env.action_space.low[:5]
    high_clip = env.action_space.high[:5]

    #termination_height = np.random.uniform(0.11, 0.13)
    random_rotate = np.random.uniform(-1.5, 1.5)
    print(random_rotate)
    wrist_rotate = obs['joints'][5] + random_rotate
    wrist_rotate = min(2.6, wrist_rotate)
    end_wrist_target = -0.4 if abs(-0.4 - wrist_rotate) > abs(2.2 - wrist_rotate) else 2.2
    images = []

    if policy is not None:
        try:
            action = policy(obs['image'])
            use_robot_state = False
        except:
            use_robot_state = True


    gripper_closed = False
    dropping = False
    augment_gripper_action = False
    for i in range(args.num_timesteps):
        print(i)
        print("State:", obs['state'])
        images.append(Image.fromarray(np.uint8(obs['render'])))
        if np.random.rand() < policy_rate:
            print("Checkpoint Policy")
            if use_robot_state:
                action, _ = policy(np.append(obs['image'], obs['state']))
            else:
                action, _ = policy(obs['image'])

        else:
            print("Scripted Policy")
            reduce_noise = False
            if np.linalg.norm((obs['desired_goal'] - obs['achieved_goal'])[:2]) > 0.09 \
                and not gripper_closed:
                diff = obs['desired_goal'] - obs['achieved_goal']
                diff[2] = 0.17 - obs['achieved_goal'][2]
                diff *= 5
                wrist_diff = wrist_rotate - obs['joints'][4]
                gripper = 0.7
                print('Moving to object')
            elif (abs(obs['desired_goal'][2] - obs['achieved_goal'][2]) > 0.01 \
                 or abs(obs['desired_goal'][2] - obs['achieved_goal'][2]) > 0.01) \
                 and not gripper_closed:
                diff = obs['desired_goal'] - obs['achieved_goal']
                diff *= 2
                diff[2] *= 4
                wrist_diff = wrist_rotate - obs['joints'][4]
                gripper = 0.7
                print('Lowering arm')
            elif obs['joints'][5] > 0.5:
                diff = np.array([0, 0, 0], dtype='float64')
                diff *= 5
                wrist_diff = 0
                gripper_closed = True
                gripper = -0.7
                print('Grasping object')
            elif np.linalg.norm(obs['achieved_goal'] - np.array([0.23, -0.3, 0.16])) > 0.03 \
                and not dropping:
                target = np.array([0.23, -0.31, 0.16])
                diff = target - obs['achieved_goal']
                wrist_diff = end_wrist_target - obs['joints'][4]
                diff *= 10
                diff[2] *= 4
                gripper = -0.7
                action = np.append(diff, [[wrist_diff * 3, gripper]])
                print('Moving out of tray')
            else:
                target = np.array([0.23, -0.35, 0.16])
                diff = target - obs['achieved_goal']
                wrist_diff = end_wrist_target - obs['joints'][4]
                diff *= 5
                gripper = -0.7
                action = np.append(diff, [[wrist_diff * 3, gripper]])
                augment_gripper_action = True
                print('Dropping')

            action = np.append(diff, [[wrist_diff * 3, gripper]])
            if reduce_noise:
                action = gym_replab.utils.add_noise_custom(action, noise_stds=np.array(noise_stds) / 3)
            else:
                action = gym_replab.utils.add_noise_custom(action, noise_stds=noise_stds)

        print(action)
        action = gym_replab.utils.clip_action(action)

        if action[4] < -0.5:
            gripper_closed = True
        elif action[4] > 0.5:
            gripper_closed = False

        if obs['achieved_goal'][1] + action[1] > 0.04 and not gripper_closed:
            action[1] = 0.04 - obs['achieved_goal'][1]

        next_obs, reward, done, info = env.step(action)

        if info['timeout']:
            env.open_gripper()
            return None

        if augment_gripper_action:
            action[4] = 0.7 + np.random.uniform(0.1)
            reward = 1
        else:
            reward = 0

        print("REWARD:", reward)
        data_xyz.append([obs, action, next_obs, reward, done])
        data_joint.append([obs, info['joint_command'], next_obs, reward, done])
        obs = next_obs

        if done:
            env.open_gripper()
            break

    make_dirs()
    if save_video:
        images[0].save('{}/scripted_grasp.gif'.format(video_save_path),
                       format='GIF', append_images=images[1:],
                       save_all=True, duration=100, loop=0)
    return goal


def zero_rewards(data_xyz, data_joint):
    for i in range(len(data_xyz)):
        data_xyz[i][3] = 0
        data_joint[i][3] = 0


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

    if args.detection_mode == 'rgb':
        file_read_failed = False
        if args.no_rgb_query:
            image0 = gym_replab.utils.cv2.imread(args.image_save_dir + '/image_empty.png')
            if image0 is None:
                print("Cannot find image_empty.png file! Querying rgb image!")
                file_read_failed = True
        if not args. no_rgb_query or file_read_failed:
            env.move_to_neutral()
            next = input('Press t to take empty rgb image ')
            while next != 't':
                next = input('Press t to take empty rgb image ')
            image0 = gym_replab.utils.get_image(512, 512)[150:]

            next = input('Place object on tray and press c to continue ')
            while next != 'c':
                next = input('Place object on tray and press c to continue ')
            print(args.image_save_dir)
            gym_replab.utils.cv2.imwrite(args.image_save_dir + '/image_empty.png', image0)


    if args.checkpoint != "":
        import railrl.torch.pytorch_util as ptu
        ptu.set_gpu_mode(True)
        with open(args.checkpoint, 'rb') as f:
    	    params = pickle.load(f)
        policy = params['trainer/trainer'].policy.get_action
        params = None

    for i in range(args.num_trajectories):
        #Make a new directory for each timestamp
        #make_dirs()

        data_xyz = []
        data_joint = []
        goal = np.array([0, 0, 0])

        if args.env in DRAWER_OPEN_AND_GRASP_ENVS:
            args.num_timesteps = 20
            noise_stds = [args.noise_std*3]*6
            noise_stds[4] = args.noise_std
            scripted_drawer_open_and_grasp(env, data_xyz, data_joint, noise_stds, \
                (i%args.video_save_frequency) == 0, policy=policy, policy_rate=args.policy_rate, image_save_dir="")
            env.close_drawer()
        elif args.env in DRAWER_OPEN_ENVS:
            args.num_timesteps = 25
            noise_stds = [args.noise_std*3]*6
            noise_stds[4] = args.noise_std
            scripted_drawer_open(env, data_xyz, data_joint, noise_stds, \
                (i%args.video_save_frequency) == 0, policy=policy, policy_rate=args.policy_rate, image_save_dir="")
            env.close_drawer()
        elif args.env in DRAWER_GRASP_ENVS:
            args.num_timesteps = 15
            noise_stds = [args.noise_std*3]*6
            noise_stds[4] = args.noise_std
            scripted_drawer_grasp(env, data_xyz, data_joint, noise_stds, \
                (i%args.video_save_frequency) == 0, policy=policy, policy_rate=args.policy_rate, image_save_dir="")
            if data_xyz[-1][3] != 0:
                env.lift_object()
                env.move_to_xyz([0.257, -0.05, 0.18])
                env.close_gripper()
                time.sleep(0.5)
                #env.move_to_background_subtract()
                i0 = gym_replab.utils.get_image(512, 512)[150:]
                env.open_gripper()
                #env.move_to_background_subtract()
                env.close_gripper()
                i1 = gym_replab.utils.get_image(512, 512)[150:]
                if not gym_replab.utils.extract_points_success_detector(i0, i1):
                    print("GRASP FAILED!")
                    zero_rewards(data_xyz, data_joint)
                else:
                    print("GRASP SUCCEEDED!")
        elif args.env in OBSTABLE_REMOVAL_ENVS:
            noise_stds = [args.noise_std*3]*6
            noise_stds[4] = 0.1
            noise_stds[2] /= 3
            goal = scripted_obstacle_removal(env, data_xyz, data_joint, noise_stds, args.detection_mode, \
                image0, args.num_objects, (i%args.video_save_frequency) == 0, policy=policy, \
                policy_rate=args.policy_rate, image_save_dir=args.image_save_dir)
            object_grasped = augment_data_continuous(data_xyz, data_joint)

            if args.image_save_dir != "" and object_grasped:
                image0 = gym_replab.utils.cv2.imread(args.image_save_dir + '/image0.png')

        if goal is not None:
            store_trajectory(data_xyz, data_joint, {'goal': goal})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--env", type=str,
                        choices=tuple(DRAWER_OPEN_AND_GRASP_ENVS + DRAWER_OPEN_ENVS \
                        + DRAWER_GRASP_ENVS + OBSTABLE_REMOVAL_ENVS),
                        required=True)
    parser.add_argument("-d", "--data_save_directory", type=str, default="WidowX200GraspV5ShortTest")
    parser.add_argument("--noise_std", type=float, default=0.01)
    parser.add_argument("--detection_mode", type=str, default='depth')
    parser.add_argument("--num_objects", type=int, default=1)
    parser.add_argument("--num_trajectories", type=int, default=50000)
    parser.add_argument("--num_timesteps", type=int, default=40)
    parser.add_argument("--video_save_frequency", type=int,
                        default=1, help="Set to zero for no video saving")
    parser.add_argument("--no_rgb_query", dest="no_rgb_query",
                        action="store_true", default=False)
    parser.add_argument("--image_save_dir", type=str, required=True)
    parser.add_argument("--checkpoint", type=str, default="")
    parser.add_argument("--policy_rate", type=float, default=0.5)
    parser.add_argument("--lift", dest="lift", \
                            action="store_true", default=False)


    args = parser.parse_args()
    args.data_save_directory += "_noise_{}".format(args.noise_std)
    if args.checkpoint != "":
        args.data_save_directory += "_rate_{}".format(args.policy_rate)

    data_save_path = None
    video_save_path = None

    ik = InverseKinematics()
    env = gym.make(args.env, observation_mode='verbose', reward_type='sparse', \
        grasp_detector='background_subtraction', transpose_image=True)._start_rospy()
    env.reset()
    #env.set_low_firmware_gains()
    env.set_custom_firmware_gains(1.2)

    if args.lift:
        env.lift_object()

    depth_image_service = env.depth_image_service

    if args.checkpoint == "":
        args.policy_rate = 0.0
    if args.image_save_dir != "":
        env.set_image_save_dir(args.image_save_dir)

    main(args)
