import numpy as np

WIDOW200_PARAMS = dict(
    NUM_JOINTS=6,
    JOINT_NAMES=['waist', 'shoulder', 'elbow', 'wrist_angle', 'wrist_rotate',
                 'gripper'],
    MOVE_TO_NEUTRAL=[0.0, -317.42, -5000.33999, 0.0, 43.0400009],
    GRIPPER_OPEN=1.8,
    GRIPPER_CLOSED=-1.0,
    NEUTRAL_JOINTS=[1.57, -1.80, -0.62, -2.0, 0.00],
    RESET_JOINTS_SLACK=[1.57, -0.6, -0.62, -1.57, 0.00],
    RESET_JOINTS=[1.57, -0.6, -0.6, -1.57, 1.57],
    RESET_JOINTS_FAR=[1.57, -0.3, -0.3, -1.57, 1.57],
    JOINT_MIN=np.array([
        -3.1,
        -1.571,
        -1.571,
        -1.745,
        -2.617,
        -2.0
    ]),
    JOINT_MAX=np.array([
        3.1,
        1.571,
        1.571,
        1.745,
        2.617,
        2.0
    ]),
    MOVE_WAIT_TIME=0.02,
    GRIPPER_WAIT_TIME=0.1,
)

WIDOW250_PARAMS = dict(
    NUM_JOINTS=7,
    JOINT_NAMES=['waist', 'shoulder', 'elbow', 'forearm_roll', 'wrist_angle',
                 'wrist_rotate', 'gripper'],
    MOVE_TO_NEUTRAL=[0.0, -317.42, -5000.33999, 0.0, 43.0400009],
    GRIPPER_OPEN=1.8,
    GRIPPER_CLOSED=-1.0,
    NEUTRAL_JOINTS=[-1.6, -0.3, -0.4, -0., -1.5, 0],
    RESET_JOINTS_SLACK=[1.57, -0.6, -0.62, -1.57, 0.00],
    RESET_JOINTS=[-1.6, -0.3, -0.4, -0., -1.5, 0],

    RESET_JOINTS_FAR=[1.57, -0.3, -0.3, -1.57, 1.57],
    JOINT_MIN=np.array([
        -3.1,
        -1.571,
        -1.571,
        -1.745,
        -2.617,
        -3.0,
    ]),
    JOINT_MAX=np.array([
        3.1,
        1.571,
        1.571,
        1.745,
        2.617,
        3.0
    ]),
    MOVE_WAIT_TIME=0.02,
    GRIPPER_WAIT_TIME=0.1,
)
