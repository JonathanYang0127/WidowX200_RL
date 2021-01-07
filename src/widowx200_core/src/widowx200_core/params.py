import numpy as np

WIDOW200_PARAMS = dict(
NUM_JOINTS = 6,
JOINT_NAMES = ['waist', 'shoulder', 'elbow', 'wrist_angle', 'wrist_rotate', 'gripper'],
MOVE_TO_NEUTRAL =  [0.0, -317.42, -5000.33999, 0.0, 43.0400009],
GRIPPER_OPEN =  1.8,
GRIPPER_CLOSED =  -1.0,
NEUTRAL_JOINTS =  [1.57, -1.80, -0.62, -2.0, 0.00],
RESET_JOINTS_SLACK =  [1.57, -0.6, -0.62, -1.57, 0.00],
RESET_JOINTS =  [1.57, -0.6, -0.6, -1.57, 1.57],
RESET_JOINTS_FAR = [1.57, -0.3, -0.3, -1.57, 1.57],
JOINT_MIN = np.array([
    -3.1,
    -1.571,
    -1.571,
    -1.745,
    -2.617,
    -2.0
]),
JOINT_MAX = np.array([
    3.1,
    1.571,
    1.571,
    1.745,
    2.617,
    2.0
]),
MOVE_WAIT_TIME = 0.02,
GRIPPER_WAIT_TIME = 0.1,
)

WIDOW250_PARAMS = dict(
NUM_JOINTS = 7,
JOINT_NAMES = ['waist', 'shoulder', 'elbow', 'wrist_angle', 'wrist_rotate', 'gripper'],
MOVE_TO_NEUTRAL =  [0.0, -317.42, -5000.33999, 0.0, 43.0400009],
GRIPPER_OPEN =  1.8,
GRIPPER_CLOSED =  -1.0,
# NEUTRAL_JOINTS =  [1.57, -1.80, -0.62, -2.0, 0.00], # original
NEUTRAL_JOINTS = [0.4, -0.08, 0.15, -0.1, 1.25, -0.45],  # New
# position: [0.39576706290245056, -0.08283496648073196, 0.15800002217292786, 3.371689796447754, 1.2547962665557861, -0.4555923044681549, 0.07976700365543365, 0.02064103650471772, -0.02064103650471772]
RESET_JOINTS_SLACK =  [1.57, -0.6, -0.62, -1.57, 0.00],
# RESET_JOINTS =  [1.57, -0.6, -0.6, -1.57, 1.57], # original
RESET_JOINTS = [0.4, -0.08, 0.15, -0.1, 1.25, -0.45],  # New

RESET_JOINTS_FAR = [1.57, -0.3, -0.3, -1.57, 1.57],
JOINT_MIN = np.array([
    -3.1,
    -1.571,
    -1.571,
    -1.745,
    -2.617,
    -2.0,
]),
JOINT_MAX = np.array([
    3.1,
    1.571,
    1.571,
    1.745,
    2.617,
    2.0
]),
MOVE_WAIT_TIME = 0.02,
GRIPPER_WAIT_TIME = 0.1,
)

