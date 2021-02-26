import numpy as np 
import gym_replab
from PIL import Image
import time
env_name = "Widow200DrawerOpen-v0"
env = gym_replab.make(env_name)._start_rospy()
for i in range(5):
    print("reset")
    obs = env.reset()
    time.sleep(3)
    print("reach 0")
    env.step([0,0,-0.3,0,0,0])
    env.step([0,0,-0.3,0,0,0])
    print("Close gripper")
    env.step([0,0,-0.3,0,-0.8,0])
    env.step([0,0,-0.3,0,0,0])

