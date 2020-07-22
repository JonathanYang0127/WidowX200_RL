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

    env.move_to_neutral()
    time.sleep(1.5)

    obs = env.reset()
    quat = ik.get_cartesian_pose()[3:]

    low_clip = env.action_space.low[:5]
    high_clip = env.action_space.high[:5]

    #termination_height = np.random.uniform(0.11, 0.13)
    random_rotate = np.random.uniform(-1.5, 1.5)
    print(random_rotate)
    wrist_rotate = obs['joints'][5] + random_rotate
    wrist_rotate = min(2.6, wrist_rotate)
    images = []

    if policy is not None:
        try:
            action = policy(obs['image'])
            use_robot_state = False
        except:
            use_robot_state = True


    gripper_closed = False
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
            elif obs['joints'][5] > 0.3:
                diff = np.array([0, 0, 0], dtype='float64')
                diff *= 5
                wrist_diff = 0
                gripper_closed = True
                gripper = -0.7
                print('Grasping object')
            else:
                lift_target = np.array([0.23, -0.04, env.reward_height_thresh + 0.02])
                diff = (lift_target - obs['achieved_goal']) / 2
                wrist_diff = 0
                #diff = np.array([0, 0, 0])
                gripper = -0.7
                reduce_noise = True
                print('Lifting object')

            action = np.append(diff, [[wrist_diff * 3, gripper]])
            if reduce_noise:
                action = gym_replab.utils.add_noise_custom(action, noise_stds=np.array(noise_stds) / 3)
            else:
                action = gym_replab.utils.add_noise_custom(action, noise_stds=noise_stds)


        action = gym_replab.utils.clip_action(action)

        if action[4] < -0.5:
            gripper_closed = True
        elif action[4] > 0.5:
            gripper_closed = False

        if obs['achieved_goal'][1] + action[1] > 0.04 and not gripper_closed:
            action[1] = 0.04 - obs['achieved_goal'][1]

        next_obs, reward, done, info = env.step(action)
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
    return goal


def augment_data_continuous(data_xyz, data_joint):
    if len(data_xyz) == 0:
        return False
    object_grasped = env.check_if_object_grasped()
    if not object_grasped:
        for i in range(len(data_xyz)):
            data_xyz[i][3] = 0
            data_joint[i][3] = 0

    return object_grasped


def store_trajectory(data_xyz, data_joint, params):
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

    if args.plot_grasp_locations:
        plt = gym_replab.utils.plt
        goals_success = [[], []]
        goals_fail = [[], []]
        plt.ion()
        fig, ax = plt.subplots()
        sc1 = ax.scatter(goals_success[1], goals_success[0], color='g')
        sc2 = ax.scatter(goals_fail[1], goals_fail[0], color='r')
        plt.xlim(-0.24, 0.16)
        plt.ylim(0.14, 0.38)
        plt.gca().invert_xaxis()
        plt.draw()
        plt.pause(0.1)

    if args.checkpoint != "":
        with open(args.checkpoint, 'rb') as f:
    	    params = pickle.load(f)
        params['evaluation/policy'].stochastic_policy.cpu()
        policy = params['evaluation/policy'].get_action
        params = None

    for i in range(args.num_trajectories):
        #Make a new directory for each timestamp
        #make_dirs()

        data_xyz = []
        data_joint = []

        if args.env in V7_GRASPING_ENVS:
            noise_stds = [args.noise_std*3]*6
            noise_stds[4] = 0.1
            noise_stds[2] /= 3
            goal = scripted_grasp_v7(env, data_xyz, data_joint, noise_stds, args.detection_mode, \
                image0, args.num_objects, (i%args.video_save_frequency) == 0, policy=policy, \
                policy_rate=args.policy_rate, image_save_dir=args.image_save_dir)
            object_grasped = augment_data_continuous(data_xyz, data_joint)

        if args.image_save_dir != "" and object_grasped:
            image0 = gym_replab.utils.cv2.imread(args.image_save_dir + '/image0.png')

        if goal is not None:
            if args.plot_grasp_locations:
                if object_grasped:
                    goals_success[0].append(goal[0])
                    goals_success[1].append(goal[1])
                else:
                    goals_fail[0].append(goal[0])
                    goals_fail[1].append(goal[1])
                sc1.set_offsets(np.c_[goals_success[1], goals_success[0]])
                sc2.set_offsets(np.c_[goals_fail[1], goals_fail[0]])
                fig.canvas.draw_idle()
                plt.pause(0.1)
            store_trajectory(data_xyz, data_joint, {'goal': goal})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--env", type=str,
                        choices=tuple(V5_GRASPING_ENVS + V6_GRASPING_ENVS + V7_GRASPING_ENVS),
                        required=True)
    parser.add_argument("-d", "--data_save_directory", type=str, default="WidowX200GraspV5ShortTest")
    parser.add_argument("--noise_std", type=float, default=0.1)
    parser.add_argument("--detection_mode", type=str, default='depth')
    parser.add_argument("--num_objects", type=int, default=1)
    parser.add_argument("--num_trajectories", type=int, default=50000)
    parser.add_argument("--num_timesteps", type=int, default=15)
    parser.add_argument("--video_save_frequency", type=int,
                        default=1, help="Set to zero for no video saving")
    parser.add_argument("--plot_grasp_locations", dest="plot_grasp_locations",
                        action="store_true", default=False)
    parser.add_argument("--no_rgb_query", dest="no_rgb_query",
                        action="store_true", default=False)
    parser.add_argument("--image_save_dir", type=str, required=True)
    parser.add_argument("--checkpoint", type=str, default="")
    parser.add_argument("--policy_rate", type=float, default=0.5)


    args = parser.parse_args()
    args.data_save_directory += "_noise_{}".format(args.noise_std)
    if args.checkpoint != "":
        args.data_save_directory += "_rate_{}".format(args.policy_rate)

    data_save_path = None
    video_save_path = None

    ik = InverseKinematics()
    env = gym.make(args.env, observation_mode='verbose', reward_type='sparse', \
        grasp_detector='background_subtraction', transpose_image=True)._start_rospy()

    depth_image_service = env.depth_image_service
    rgb_image_service = gym_replab.utils.KinectImageService('rgb')


    if args.checkpoint == "":
        args.policy_rate = 0.0
    print("ASDASDASDADASDA")
    if args.image_save_dir != "":
        env.set_image_save_dir(args.image_save_dir)

    main(args)
