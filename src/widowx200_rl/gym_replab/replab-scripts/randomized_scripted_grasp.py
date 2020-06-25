import gym
import gym_replab
from widowx200_core.ik import InverseKinematics
import numpy as np
import time
import argparse
import os
import sys
from PIL import Image

V5_GRASPING_ENVS = ['Widow200RealRobotGraspV5-v0']
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


def scripted_grasp_v5(env, data_xyz, data_joint, noise_stds):
    env.move_to_neutral()
    time.sleep(1.0)

    pc_loop_counter = 0
    pc_data = gym_replab.utils.get_center_and_second_pc(depth_image_service)
    while pc_data is None or pc_data[0][0] >= 0.45:
        env.drop_at_random_location()
        env.move_to_neutral()
        pc_data = gym_replab.utils.get_center_and_second_pc(depth_image_service)
        pc_loop_counter += 1
        if pc_loop_counter >= 5:
            sys.exit(0)

    goal, object_vector = pc_data
    goal = np.append(goal, 0.052)
    print(goal)
    #goal[0] += np.random.uniform(low = -0.03, high = 0.03)
    #goal[1] += np.random.uniform(low = -0.03, high = 0.03)
    goal[0] += np.random.normal(0, 0.012)
    goal[1] += np.random.normal(0, 0.012)

    goal[2] += np.random.uniform(low = 0.0, high = 0.03)

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
    images = []

    gripper_closed = False
    for i in range(args.num_timesteps):
        print(obs['observation'])
        images.append(Image.fromarray(np.uint8(obs['render'])))
        print(i)
        if np.linalg.norm((obs['desired_goal'] - obs['achieved_goal'])[:2]) > 0.06 \
            and not gripper_closed:
            diff = obs['desired_goal'] - obs['achieved_goal']
            diff[2] = 0.17 - obs['achieved_goal'][2]
            diff *= 5
            wrist_diff = wrist_rotate - obs['joints'][4]
            gripper = 0.7
            terminate = 0
            print('Moving to object')
        elif (abs(obs['desired_goal'][2] - obs['achieved_goal'][2]) > 0.01 \
             or np.linalg.norm(obs['desired_goal'] - obs['achieved_goal']) > 0.06) \
             and not gripper_closed:
            diff = obs['desired_goal'] - obs['achieved_goal']
            diff *= 2
            diff[2] *= 2
            wrist_diff = wrist_rotate - obs['joints'][4]
            gripper = 0.7
            terminate = 0
            print('Lowering arm')
        elif obs['joints'][5] > 0.3:
            diff = np.array([0, 0, 0], dtype='float64')
            diff *= 5
            wrist_diff = 0
            gripper_closed = True
            gripper = -0.7
            terminate = 0
            print('Grasping object')
        elif obs['achieved_goal'][2] < env.reward_height_thresh + 0.001:
            diff = np.array([0, 0, 0], dtype='float64')
            print(obs['achieved_goal'][2], "ADASD")
            diff[2] = 0.7
            wrist_diff = 0
            gripper = -0.7
            terminate = 0
            gripper_closed = True
            print('Lifting object')
        else:
            diff = np.array([0, 0, 1], dtype='float64')
            diff *= 5
            wrist_diff = 0
            gripper = -0.7
            terminate = 0.7
            print('Done!')


        diff = np.append(diff, [[wrist_diff * 3, gripper, terminate]])
        diff = gym_replab.utils.add_noise_custom(diff, noise_stds=noise_stds)
        diff = gym_replab.utils.clip_action(diff)
        print(diff)
        next_obs, reward, done, info = env.step(diff)

        if info['timeout']:
            env.open_gripper()
            return None, False

        data_xyz.append([obs, diff, next_obs, reward, done])
        data_joint.append([obs, info['joint_command'], next_obs, reward, done])
        obs = next_obs

        if done:
            env.open_gripper()
            break

    images[0].save('{}/scripted_grasp.gif'.format(video_save_path),
                       format='GIF', append_images=images[1:],
                       save_all=True, duration=100, loop=0)
    return goal, data_xyz[-1][3] == 1


def scripted_grasp_v6(env, data_xyz, data_joint, noise_stds):
    env.move_to_neutral()
    time.sleep(1.0)

    pc_loop_counter = 0
    pc_data = gym_replab.utils.get_center_and_second_pc(depth_image_service)
    while pc_data is None or pc_data[0][0] >= 0.45:
        env.drop_at_random_location()
        env.move_to_neutral()
        pc_data = gym_replab.utils.get_center_and_second_pc(depth_image_service)
        pc_loop_counter += 1
        if pc_loop_counter >= 5:
            sys.exit(0)

    goal, object_vector = pc_data
    goal = np.append(goal, 0.052)
    print(goal)
    #goal[0] += np.random.uniform(low = -0.03, high = 0.03)
    #goal[1] += np.random.uniform(low = -0.03, high = 0.03)
    goal[0] += np.random.normal(0, 0.01) + 0.01
    if goal[0] > 0.3:
        goal[0] += 0.01
    if goal[1] < -0.14:
        goal[1] -= 0.01
    goal[1] += np.random.normal(0, 0.015)

    goal[2] += np.random.uniform(low = -0.012, high = 0.012)

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
    images = []

    gripper_closed = False
    for i in range(args.num_timesteps):
        print(i)
        print(obs['achieved_goal'][2], 'ASDASDA')
        images.append(Image.fromarray(np.uint8(obs['render'])))
        if np.linalg.norm((obs['desired_goal'] - obs['achieved_goal'])[:2]) > 0.1 \
            and not gripper_closed:
            diff = obs['desired_goal'] - obs['achieved_goal']
            diff[2] = 0.17 - obs['achieved_goal'][2]
            diff *= 5
            wrist_diff = wrist_rotate - obs['joints'][4]
            gripper = 0.7
            print('Moving to object')
        elif (abs(obs['desired_goal'][2] - obs['achieved_goal'][2]) > 0.01 \
             or np.linalg.norm(obs['desired_goal'] - obs['achieved_goal']) > 0.1) \
             and not gripper_closed:
            diff = obs['desired_goal'] - obs['achieved_goal']
            diff *= 2
            diff[2] *= 2
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
        elif obs['achieved_goal'][2] < env.reward_height_thresh + 0.001:
            diff = np.array([0, 0, 0], dtype='float64')
            print(obs['achieved_goal'][2], "ADASD")
            diff[2] = 1
            wrist_diff = 0
            gripper = -0.7
            gripper_closed = True
            print('Lifting object')
        else:
            diff = np.array([0, 0, 1], dtype='float64')
            diff *= 5
            wrist_diff = 0
            gripper = -0.7
            print('Done!')


        diff = np.append(diff, [[wrist_diff * 3, gripper]])
        diff = gym_replab.utils.add_noise_custom(diff, noise_stds=noise_stds)
        diff = gym_replab.utils.clip_action(diff)
        print(diff)
        next_obs, reward, done, info = env.step(diff)
        print("REWARD:", reward)

        if info['timeout']:
            env.open_gripper()
            return None

        data_xyz.append([obs, diff, next_obs, reward, done])
        data_joint.append([obs, info['joint_command'], next_obs, reward, done])
        obs = next_obs

        if done:
            env.open_gripper()
            break

    images[0].save('{}/scripted_grasp.gif'.format(video_save_path),
                       format='GIF', append_images=images[1:],
                       save_all=True, duration=100, loop=0)
    return goal


def augment_data_v6(data_xyz, data_joint):
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

    for i in range(args.num_trajectories):
        #Make a new directory for each timestamp
        make_dirs()

        data_xyz = []
        data_joint = []

        if args.env in V5_GRASPING_ENVS:
            goal = scripted_grasp_v5(env, data_xyz, data_joint, args.noise_std)
        if args.env in V6_GRASPING_ENVS:
            noise_stds = [args.noise_std*3]*6
            noise_stds[4] = 0.1
            noise_stds[2] /= 3
            goal = scripted_grasp_v6(env, data_xyz, data_joint, noise_stds)
            object_grasped = augment_data_v6(data_xyz, data_joint)

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
                        choices=tuple(V5_GRASPING_ENVS + V6_GRASPING_ENVS),
                        required=True)
    parser.add_argument("-d", "--data_save_directory", type=str, default="WidowX200GraspV5ShortTest")
    parser.add_argument("--noise_std", type=float, default=0.06)
    parser.add_argument("--num_trajectories", type=int, default=50000)
    parser.add_argument("--num_timesteps", type=int, default=15)
    parser.add_argument("--video_save_frequency", type=int,
                        default=1, help="Set to zero for no video saving")
    parser.add_argument("--plot_grasp_locations", dest="plot_grasp_locations",
                        action="store_true", default=False)


    args = parser.parse_args()
    args.data_save_directory += "_noise_{}".format(args.noise_std)

    data_save_path = None
    video_save_path = None

    ik = InverseKinematics()
    env = gym.make(args.env, observation_mode='verbose', reward_type='sparse', \
        grasp_detector='background_subtraction', transpose_image=True)._start_rospy()

    depth_image_service = env.depth_image_service
    rgb_image_service = gym_replab.utils.KinectImageService('rgb')
    main(args)
