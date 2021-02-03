import numpy as np


JOINT_NAMES = ['waist', 'shoulder', 'elbow', 'wrist_angle', 'wrist_rotate', 'gripper']
MOVE_TO_NEUTRAL = [0.0, -317.42, -5000.33999, 0.0, 43.0400009]
GRIPPER_OPEN = 1.8
GRIPPER_CLOSED = -1.0
NEUTRAL_JOINTS = [1.57, -1.80, -0.62, -2.0, 0.00]
RESET_JOINTS_SLACK = [1.57, -0.6, -0.62, -1.57, 0.00]
RESET_JOINTS = [1.57, -0.6, -0.6, -1.57, 0]
RESET_JOINTS_FAR = [1.57, -0.3, -0.3, -1.57, 0]
JOINT_MIN = np.array([
    -3.1,
    -1.571,
    -1.571,
    -1.745,
    -2.617,
    -2.0
])
JOINT_MAX = np.array([
    3.1,
    1.571,
    1.571,
    1.745,
    2.617,
    2.0
])
MOVE_WAIT_TIME = 0.5
VEL_MOVE_WAIT_TIME = 1
ACCEL_TIME = 0.1
GRIPPER_WAIT_TIME = 0.1

NEUTRAL_JOINTS = RESET_JOINTS
