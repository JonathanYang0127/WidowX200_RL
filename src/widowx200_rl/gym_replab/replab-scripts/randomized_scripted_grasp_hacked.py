import gym
import gym_replab
from widowx200_core.ik import InverseKinematics
import numpy as np
import time
import argparse
import os
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("--data_save_directory", type=str, default="WidowX200GraspNew4")
parser.add_argument("--num_trajectories", type=int, default=1000)
parser.add_argument("--num_timesteps", type=int, default=40)
parser.add_argument("--video_save_frequency", type=int,
                    default=1, help="Set to zero for no video saving")

args = parser.parse_args()
data_save_path = None
video_save_path = None

ik = InverseKinematics()
env = gym.make('widowx200-v0')._start_rospy()

depth_image_service = gym_replab.utils.KinectImageService('sd_pts')
rgb_image_service = gym_replab.utils.KinectImageService('rgb')


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


def drop_at_random_location(env):
    env.move_to_neutral()
    time.sleep(1.0)
    grasped = gym_replab.utils.check_if_object_grasped(depth_image_service)
    #grasped = env.check_if_object_grasped_gripper()
    if not grasped:
        return False
    goal = [0, 0, 0]
    goal[0] = np.random.uniform(low=0.18, high=0.30)
    goal[1] = np.random.uniform(low=-0.17, high=0.13)
    goal[2] = 0.07
    env.set_goal(goal)
    obs = env.reset(gripper=False)
    quat = ik.get_cartesian_pose()[3:]

    low_clip = env.action_space.low[:5]
    high_clip = env.action_space.high[:5]

    gripper_opened = False
    for i in range(args.num_timesteps):
        #print(i)
        #print(obs)
        if np.linalg.norm((obs['desired_goal'] - obs['achieved_goal'])[:2]) > 0.03\
            and not gripper_opened:
            print( np.linalg.norm((obs['desired_goal'] - obs['achieved_goal'])[:2]) )
            diff = obs['desired_goal'] - obs['achieved_goal']
            diff[2] = 0.17 - obs['achieved_goal'][2]
            #print(diff[2])
            if np.linalg.norm(diff) < 0.06:
                diff[0] = diff[0] / np.linalg.norm(diff)
                diff[1] = diff[1] / np.linalg.norm(diff)
            diff *= 5
            action = gym_replab.utils.compute_ik_command(diff, low_clip, high_clip, quat, ik)
            action = np.append(action, -0.3)
            print('Moving to random position')
        elif abs(obs['desired_goal'][2] - obs['achieved_goal'][2]) > 0.01\
            and not gripper_opened:
            print(obs['desired_goal'][2], obs['achieved_goal'][2], abs(obs['desired_goal'][2] - obs['achieved_goal'][2]))
            diff = obs['desired_goal'] - obs['achieved_goal']
            diff[2] -= 0.005
            diff *= 5
            action = gym_replab.utils.compute_ik_command(diff, low_clip, high_clip, quat, ik)
            action = np.append(action, obs['gripper'])
            print('Lowering arm')
        elif obs['joints'][5] < 0:
            #print(obs['desired_goal'][2], obs['achieved_goal'], abs(obs['desired_goal'][2] - obs['achieved_goal'][2]))
            diff = np.array([0, 0, 0])
            diff *= 5
            action = gym_replab.utils.compute_ik_command(diff, low_clip, high_clip, quat, ik)
            action = np.append(action, 0.6)
            gripper_opened = True
            print('Dropping object')
        elif obs['achieved_goal'][2] < 0.10:
            #print(obs['desired_goal'][2], obs['achieved_goal'][2], abs(obs['desired_goal'][2] - obs['achieved_goal'][2]))
            diff = np.array([0, 0, 0.18])
            diff *= 5
            action = gym_replab.utils.compute_ik_command(diff, low_clip, high_clip, quat, ik)
            action = np.append(action, obs['gripper'])
            print('Lifting object')
        else:
            break

        print(diff)
        action = np.clip(np.array(action, dtype=np.float32), \
            env.action_space.low, env.action_space.high)
        obs, reward, next_obs, done = env.step(action)
    return True


def scripted_grasp(env, data_xyz, data_joint):
    env.move_to_neutral()
    time.sleep(1.0)
    pc_data = gym_replab.utils.get_center_and_second_pc(depth_image_service)
    if pc_data is None:
        return None
    else:
        goal, object_vector = pc_data
    goal = np.append(goal, 0.067)
    print(goal)
    goal[0] += np.random.uniform(low = -0.02, high = 0.03)
    goal[1] += np.random.uniform(low = -0.015, high = 0.015)
    goal[2] += np.random.uniform(low = 0, high = 0.01)

    env.set_goal(goal)
    obs = env.reset()
    quat = ik.get_cartesian_pose()[3:]

    low_clip = env.action_space.low[:5]
    high_clip = env.action_space.high[:5]


    images = []

    gripper_closed = False
    for i in range(args.num_timesteps):
        images.append(Image.fromarray(np.uint8(obs['image'])))
        #images.append(Image.fromarray(np.uint8(gym_replab.utils.get_rgb_image(rgb_image_service))))
        print(i)
        #print(obs)
        if np.linalg.norm((obs['desired_goal'] - obs['achieved_goal'])[:2]) > 0.04 \
            and not gripper_closed:
            #print( np.linalg.norm((obs['desired_goal'] - obs['achieved_goal'])[:2]) )
            diff = obs['desired_goal'] - obs['achieved_goal']
            diff[2] = 0.17 - obs['achieved_goal'][2]
            #print(diff[2])
            if np.linalg.norm(diff) < 0.06:
                diff[0] = diff[0] / np.linalg.norm(diff)
                diff[1] = diff[1] / np.linalg.norm(diff)
            diff = gym_replab.utils.add_noise(diff)
            diff *= 5
            diff = gym_replab.utils.enforce_normalization(diff)
            action = gym_replab.utils.compute_ik_command(diff, low_clip, high_clip, quat, ik)
            action = np.append(action, 0.6)
            gripper = 0.6
            print('Moving to object')
        elif (abs(obs['desired_goal'][2] - obs['achieved_goal'][2]) > 0.01 \
             or np.linalg.norm(obs['desired_goal'] - obs['achieved_goal']) > 0.04) \
             and not gripper_closed:
            #print(obs['desired_goal'][2], obs['achieved_goal'][2], abs(obs['desired_goal'][2] - obs['achieved_goal'][2]))
            diff = obs['desired_goal'] - obs['achieved_goal']
            diff[2] -= 0.005
            diff = gym_replab.utils.add_noise(diff)
            diff *= 5
            diff = gym_replab.utils.enforce_normalization(diff)
            action = gym_replab.utils.compute_ik_command(diff, low_clip, high_clip, quat, ik)
            action = np.append(action, 0.6)
            gripper = 0.6
            print('Lowering arm')
        elif obs['joints'][5] > 0.1:
            #print(obs['desired_goal'][2], obs['achieved_goal'], abs(obs['desired_goal'][2] - obs['achieved_goal'][2]))
            diff = np.array([0, 0, 0])
            diff *= 5
            diff = gym_replab.utils.enforce_normalization(diff)
            action = gym_replab.utils.compute_ik_command(diff, low_clip, high_clip, quat, ik)
            action = np.append(action, -0.3)
            gripper_closed = True
            gripper = -0.3
            print('Grasping object')
        elif obs['achieved_goal'][2] < 0.10:
            #print(obs['desired_goal'][2], obs['achieved_goal'][2], abs(obs['desired_goal'][2] - obs['achieved_goal'][2]))
            diff = np.array([0, 0, 0.18])
            diff *= 5
            diff = gym_replab.utils.enforce_normalization(diff)
            action = gym_replab.utils.compute_ik_command(diff, low_clip, high_clip, quat, ik)
            action = np.append(action, -0.3)
            gripper = -0.3
            gripper_closed = True
            print('Lifting object')
        else:
            diff = np.array([0, 0, 0.05])
            diff *= 5
            diff = gym_replab.utils.enforce_normalization(diff)
            action = gym_replab.utils.compute_ik_command(diff, low_clip, high_clip, quat, ik)
            action = np.append(action, -0.3)
            gripper = -0.3
            print('Done!')

        print(np.linalg.norm((obs['desired_goal'] - obs['achieved_goal'])[:2]))
        next_obs, reward, done, info = env.step(action)
        data_xyz.append([obs, np.append(diff, gripper), next_obs, reward, done])
        data_joint.append([obs, action, next_obs, reward, done])
        obs = next_obs

    images[0].save('{}/scripted_grasp.gif'.format(video_save_path),
                       format='GIF', append_images=images[1:],
                       save_all=True, duration=100, loop=0)
    return goal


def store_trajectory(object_grasped, data_xyz, data_joint, params):
    pool_xyz = gym_replab.utils.DemoPool()
    pool_joint = gym_replab.utils.DemoPool()
    data_xyz[args.num_timesteps - 1][3] = 1 if object_grasped else 0
    data_joint[args.num_timesteps - 1][3] = 1 if object_grasped else 0
    for i in range(args.num_timesteps):
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


grasp_successful = False
if __name__ == '__main__':
    for i in range(10000):
        data_xyz = []
        data_joint = []
        make_dirs()
        goal = scripted_grasp(env, data_xyz, data_joint)
        #image0 = gym_replab.utils.get_rgb_image(rgb_image_service)
        object_grasped = drop_at_random_location(env)
        #image1 = gym_replab.utils.get_rgb_image(rgb_image_service)
        #object_grasped = gym_replab.utils.grasp_success(image0, image1)
        if object_grasped:
            print("*****SUCCESS*****")
        else:
            print("*****FAIL*****")
        if goal is not None:
            store_trajectory(object_grasped, data_xyz, data_joint, {'goal': goal})
