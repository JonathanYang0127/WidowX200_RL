import gym
import gym_replab
from widowx200_core.ik import InverseKinematics
import numpy as np
import time
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--data_save_directory", type=str, default="WidowX200Grasp")
parser.add_argument("--num_trajectories", type=int, default=1000)
parser.add_argument("--num_timesteps", type=int, default=40)
parser.add_argument("--video_save_frequency", type=int,
                    default=1, help="Set to zero for no video saving")

args = parser.parse_args()
timestamp = gym_replab.utils.timestamp()
data_save_path = os.path.join(__file__, "../..", 'data',
                              args.data_save_directory, timestamp)
data_save_path = os.path.abspath(data_save_path)
video_save_path = os.path.join(data_save_path, "videos")

if not os.path.exists(data_save_path):
    os.makedirs(data_save_path)
if not os.path.exists(video_save_path) and args.video_save_frequency > 0:
    os.makedirs(video_save_path)


ik = InverseKinematics()
env = gym.make('widowx200-v0')._start_rospy()

depth_image_service = gym_replab.utils.KinectImageService('sd_pts')
rgb_image_service = gym_replab.utils.KinectImageService('rgb')


def drop_at_random_location(env):
    env.move_to_neutral()
    time.sleep(2.0)
    grasped = gym_replab.utils.check_if_object_grasped(depth_image_service)
    #grasped = env.check_if_object_grasped_gripper()
    if not grasped:
        return True
    goal = [0, 0, 0]
    goal[0] = np.random.uniform(low=0.18, high=0.28)
    goal[1] = np.random.uniform(low=-0.15, high=0.1)
    goal[2] = 0.065
    env.set_goal(goal)
    obs = env.reset(gripper=False)
    quat = ik.get_cartesian_pose()[3:]

    print(ik.get_cartesian_pose())

    for i in range(args.num_timesteps):
        print(i)
        print(obs)
        if np.linalg.norm((obs['desired_goal'] - obs['achieved_goal'])[:2]) > 0.03:
            print( np.linalg.norm((obs['desired_goal'] - obs['achieved_goal'])[:2]) )
            diff = obs['desired_goal'] - obs['achieved_goal']
            diff[2] = 0.17 - obs['achieved_goal'][2]
            #print(diff[2])
            if np.linalg.norm(diff) < 0.06:
                diff[0] = diff[0] / np.linalg.norm(diff)
                diff[1] = diff[1] / np.linalg.norm(diff)
            action = gym_replab.utils.compute_ik_command(diff, quat, ik) / 4
            action = np.append(action, -0.3)
            print('Moving to random position')
        elif abs(obs['desired_goal'][2] - obs['achieved_goal'][2]) > 0.01:
            print(obs['desired_goal'][2], obs['achieved_goal'][2], abs(obs['desired_goal'][2] - obs['achieved_goal'][2]))
            diff = obs['desired_goal'] - obs['achieved_goal']
            diff[2] -= 0.005
            action = gym_replab.utils.compute_ik_command(diff, quat, ik) / 3
            action = np.append(action, obs['gripper'])
            print('Lowering arm')
        else:
            diff = [0, 0, 0.05]
            action = gym_replab.utils.compute_ik_command(diff, quat, ik) / 3
            action = np.append(action, 0.6)
            print('Dropping object')
            obs, reward, next_obs, done = env.step(action)
            time.sleep(1)
            return False

        action = np.clip(np.array(action, dtype=np.float32), \
            env.action_space.low, env.action_space.high)
        obs, reward, next_obs, done = env.step(action)
    return False


def scripted_grasp(env, trajectories):
    env.move_to_neutral()
    time.sleep(2.0)
    pc_data = gym_replab.utils.get_center_and_second_pc(depth_image_service)
    if pc_data is None:
        return None
    else:
        goal, object_vector = pc_data
    goal = np.append(goal, 0.065)
    print(goal)
    goal[0] += np.random.uniform(low = -0.03, high = 0.03)
    goal[1] += np.random.uniform(low = -0.03, high = 0.03)
    goal[2] += np.random.uniform(low = -0.05, high = 0.015)

    env.set_goal(goal)
    obs = env.reset()
    quat = ik.get_cartesian_pose()[3:]

    print(ik.get_cartesian_pose())

    gripper_closed = False
    for i in range(args.num_timesteps):
        print(i)
        print(obs)
        if np.linalg.norm((obs['desired_goal'] - obs['achieved_goal'])[:2]) > 0.03 \
            and not gripper_closed:
            #print( np.linalg.norm((obs['desired_goal'] - obs['achieved_goal'])[:2]) )
            diff = obs['desired_goal'] - obs['achieved_goal']
            diff[2] = 0.17 - obs['achieved_goal'][2]
            #print(diff[2])
            if np.linalg.norm(diff) < 0.06:
                diff[0] = diff[0] / np.linalg.norm(diff)
                diff[1] = diff[1] / np.linalg.norm(diff)
            action = gym_replab.utils.compute_ik_command(diff, quat, ik) / 4
            action = np.append(action, 0.6)
            print('Moving to object')
        elif (abs(obs['desired_goal'][2] - obs['achieved_goal'][2]) > 0.01 \
             or np.linalg.norm(obs['desired_goal'] - obs['achieved_goal']) > 0.03) \
             and not gripper_closed:
            #print(obs['desired_goal'][2], obs['achieved_goal'][2], abs(obs['desired_goal'][2] - obs['achieved_goal'][2]))
            diff = obs['desired_goal'] - obs['achieved_goal']
            diff[2] -= 0.005
            action = gym_replab.utils.compute_ik_command(diff, quat, ik) / 3
            action = np.append(action, 0.6)
            print('Lowering arm')
        elif obs['joints'][5] > 0:
            #print(obs['desired_goal'][2], obs['achieved_goal'], abs(obs['desired_goal'][2] - obs['achieved_goal'][2]))
            diff = np.array([0, 0, 0])
            action = gym_replab.utils.compute_ik_command(diff, quat, ik) / 3
            action = np.append(action, -0.3)
            gripper_closed = True
            print('Grasping object')
        elif obs['achieved_goal'][2] < 0.10:
            #print(obs['desired_goal'][2], obs['achieved_goal'][2], abs(obs['desired_goal'][2] - obs['achieved_goal'][2]))
            diff = [0, 0, 0.3]
            action = gym_replab.utils.compute_ik_command(diff, quat, ik) / 3
            action = np.append(action, obs['gripper'])
            print('Lifting object')
        else:
            diff = np.array([0, 0, 0.05])
            action = gym_replab.utils.compute_ik_command(diff, quat, ik) / 3
            action = np.append(action, obs['gripper'])
            print('Done!')

        action = np.clip(np.array(action, dtype=np.float32), \
            env.action_space.low, env.action_space.high)
        print(action)
        for i in range(len(action)):
            if abs(action[i]) < 0.001:
                action[i] = 0
        next_obs, reward, done, info = env.step(action)
        trajectories.append([obs, action, next_obs, reward, done])
        obs = next_obs
    return goal


def store_trajectory(object_grasped, data, params):
    pool = gym_replab.utils.DemoPool()
    data[args.num_timesteps - 1][3] = 1 if object_grasped else 0
    for i in range(args.num_timesteps):
        obs, nobs = data[i][0], data[i][2]
        modified_obs = {'image': obs['image'], 'state': obs['state']}
        modified_nobs = {'image': nobs['image'], 'state': nobs['state']}

        data[i][0], data[i][2] = modified_obs, modified_nobs
        pool.add_sample(*(data[i]))

    pool.save(params, data_save_path,
          '{}_pool_{}.pkl'.format(timestamp, pool.size))


grasp_successful = False
if __name__ == '__main__':
    for i in range(100):
        data = []
        goal = scripted_grasp(env, data)
        object_grasped = drop_at_random_location(env)
        if goal is not None:
            store_trajectory(object_grasped, data, {'state': goal})
