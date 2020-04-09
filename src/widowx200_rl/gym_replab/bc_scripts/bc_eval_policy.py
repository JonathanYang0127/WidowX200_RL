import torch
import numpy as np
import time
import pickle
import skvideo.io

import gym_replab
import argparse
from widowx200_core.ik import InverseKinematics


ik = InverseKinematics()
depth_image_service = gym_replab.utils.KinectImageService('sd_pts')

def drop_at_random_location(env):
    env.move_to_neutral()
    time.sleep(1.0)
    #grasped = gym_replab.utils.check_if_object_grasped(depth_image_service)
    #grasped = env.check_if_object_grasped_gripper()
    #if not grasped:
    #    return False
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



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', type=str)
    parser.add_argument('--num_timesteps', type=int, default=50)
    args = parser.parse_args()
    filepath = args.filepath
    torch.cuda.empty_cache()
    #filepath = ('/home/huihanl/batch_rl_prev/data/BC-grasp-pixel-loss-type-mse-epoch-100/BC_grasp_pixel-loss-type-mse-epoch-100_2020_01_18_01_11_07_0000--s-0/params_policy.pkl')
    #filepath = ('/home/huihanl/batch_rl_prev/data/BC-grasp-pixel-loss-type-mse/test/params_policy.pkl')
    checkpoint = torch.load(filepath)
    #env = checkpoint['evaluation/env']

    env =  gym_replab.envs.WidowX200EnvJoint()._start_rospy()

    policy = checkpoint['trainer/policy'].to("cpu")

    #with open(filepath, 'rb') as f:
     #   policy = pickle.load(f)


    for j in range(10):
        obs = env.reset()
        rollout_return = 0
        images = []
        for i in range(args.num_timesteps):
            images.append(obs['image'])

            obs_transpose = np.transpose(obs['image'], (2, 0, 1))
            obs_flat = np.concatenate(
                (obs_transpose.astype(np.float64).flatten()/255.0, obs['state'])
            )
            obs = obs_flat

            act, _ = policy.get_action(torch.from_numpy(obs.astype(np.float32)))
            #print("act before: ", act)
            #xyz_remap=[1, 0, 2]
            #xyz_scale=[-1, 1, 1]
            #act[:3] = act[:3][xyz_remap] * xyz_scale
            #print("act after: ", act)
            #print(act)
            #print(i)
            obs, rew, done, info = env.step(act)
            rollout_return += rew
            #time.sleep(0.05)
            print('Return: {}'.format(rollout_return))

        drop_at_random_location(env)

    """
    filename = 'test_crop.mp4'
    writer = skvideo.io.FFmpegWriter(
        filename,
        inputdict={"-r": "10"},
        outputdict={
            '-vcodec': 'libx264',
        })

    for j in range(len(images)):
        writer.writeFrame(images[j])
    writer.close()


    """
