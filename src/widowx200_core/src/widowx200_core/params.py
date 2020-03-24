import numpy as np

JOINT_NAMES = ['waist', 'shoulder', 'elbow', 'wrist_angle', 'wrist_rotate', 'gripper']
MOVE_TO_NEUTRAL = [0.0, -317.42, -5000.33999, 0.0, 43.0400009]
GRIPPER_OPEN = 1.8
GRIPPER_CLOSED = -1.0
NEUTRAL_JOINTS = [0, -1.85, -1.5, -0.8, 0]
RESET_JOINTS = [0.0, -1.3, -1.3, 1.57, 0]
JOINT_MIN = np.array([
    -3.1,
    -1.571,
    -1.571,
    -1.745,
    -2.617,
    -1.0
])
JOINT_MAX = np.array([
    3.1,
    1.571,
    1.571,
    1.745,
    2.617,
    1.0
])
