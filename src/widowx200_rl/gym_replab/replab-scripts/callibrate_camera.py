import gym
import gym_replab
from widowx200_core.ik import InverseKinematics
from tqdm import tqdm
import numpy as np
import time
import argparse

ik = InverseKinematics()
env = gym.make('widowx200-v0')._start_rospy()

depth_image_service = gym_replab.utils.KinectImageService('sd_pts')

def scripted_grasp(env, ik, goal):
    env.set_goal(goal)
    obs = env.reset()
    quat = ik.get_cartesian_pose()[3:]

    low_clip = env.action_space.low[:5]
    high_clip = env.action_space.high[:5]

    gripper_closed = False
    for i in range(80):
        print(obs)
        if np.linalg.norm((obs['desired_goal'] - obs['achieved_goal'])[:2]) > 0.03 \
            and not gripper_closed:
            print( np.linalg.norm((obs['desired_goal'] - obs['achieved_goal'])[:2]) )
            diff = obs['desired_goal'] - obs['achieved_goal']
            diff[2] = 0.17 - obs['achieved_goal'][2]
            #print(diff[2])
            if np.linalg.norm(diff) < 0.06:
                diff[0] = diff[0] / np.linalg.norm(diff)
                diff[1] = diff[1] / np.linalg.norm(diff)
            diff *= 5
            action = gym_replab.utils.compute_ik_command(diff, low_clip, high_clip, quat, ik)
            action = np.append(action, 0.6)
            print('Moving to object')
        elif abs(obs['desired_goal'][2] - obs['achieved_goal'][2]) > 0.01 \
            and not gripper_closed:
            print(obs['desired_goal'][2], obs['achieved_goal'][2], abs(obs['desired_goal'][2] - obs['achieved_goal'][2]))
            diff = obs['desired_goal'] - obs['achieved_goal']
            diff[2] -= 0.005
            diff *= 5
            action = gym_replab.utils.compute_ik_command(diff, low_clip, high_clip, quat, ik)
            action = np.append(action, 0.6)
            print('Lowering arm')
        else:
            return obs

        action = np.clip(np.array(action, dtype=np.float32), \
            env.action_space.low, env.action_space.high)
        obs, reward, next_obs, done = env.step(action)
    return obs


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--option", type=str,
                        choices=("rgb", "depth", "both"),
                        required=True)
    parser.add_argument("-s", "--save_dir", type=str, default="")
    args = parser.parse_args()

    if args.option == 'rgb':
        env.move_to_neutral()
        next = input('Press t to get empty rgb image ')
        while next != 't':
            next = input('Press t to get empty rgb image ')
        image0 = gym_replab.utils.get_image(512, 512)[150:]
        

    goals = [[0.16, 0.13, 0.065],
    [0.26, 0.13, 0.065],
    [0.32, 0.13, 0.065],
    [0.16, -0.03, 0.065],
    [0.26, -0.03, 0.065],
    [0.32, -0.03, 0.065],
    [0.16, -0.18, 0.065],
    [0.26, -0.18, 0.065],
    [0.32, -0.18, 0.065]]
    robot_coords = []
    depth_coords = []
    rgb_coords = []

    for j in tqdm(range(len(goals))):
        obs = scripted_grasp(env, ik, goals[j])
        next = input('Press n to move to neutral')
        while (next != 'n'):
            next = input('Press n to move to neutral')
        env.move_to_neutral()
        next = input('Press c to callibrate')
        while (next != 'c'):
            next = input('Press c to callibrate')

        robot_coords.append(obs['achieved_goal'])
        if args.option == 'depth' or args.option == 'both':
            image = depth_image_service.pull_image(j)
            pc_center = gym_replab.utils.get_pc_cluster_center("pc{}.pcd".format(j))
            depth_coords.append(pc_center)
            if pc_center is None:
                print("ERROR: cannot detect object using point cloud!")
                break
        if args.option == 'rgb' or args.option == 'both':
            image1 = gym_replab.utils.get_image(512, 512)[150:]
            rgb_coords.append(gym_replab.utils.get_rgb_centroids(image0, image1, 1, \
                args.save_dir)[0])

        next = input('Press n for next point')
        while (next != 'n'):
            next = input('Press n for next point')

    print('Robot Coordinates: ')
    print(robot_coords)

    if args.option == 'rgb' or args.option == 'both':
        print('RGB Coordinates: ')
        print(rgb_coords)

    if args.option == 'depth' or args.option == 'both':
        print('Depth Coordinates: ')
        print(depth_coords)
        poly = PolynomialFeatures(1)
        depth_coords = poly.fit_transform(depth_coords)
        gym_replab.utils.compute_robot_transformation_matrix(np.array(depth_coords), np.array(robot_coords))
    print("\n")
