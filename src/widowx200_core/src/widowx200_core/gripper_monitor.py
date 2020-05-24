#!/usr/bin/env python
import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64
from interbotix_sdk.msg import SingleCommand

import numpy as np
import time

class WidowXGripper:

    def __init__(self, boundaries=False):
        self.joints_sub = rospy.Subscriber('/wx200/joint_states', JointState, self.joint_callback)
        self._gripper_pub = rospy.Publisher('/wx200/single_joint/command', SingleCommand, queue_size=1)
        self._gripper_desired_sub = rospy.Subscriber('/wx200/single_joint/command', SingleCommand, self.gripper_desired_callback)
        self._joint_states = None
        self._desired_position = None
        self._desired_position_changed = False
        rospy.sleep(2)
        self.monitor_gripper()


    def monitor_gripper(self):
        prev_desired_position = None
        while(True):
            if self._desired_position_changed:
                self._desired_position_changed = False
                time.sleep(0.1)
            if self._joint_states is None:
                time.sleep(0.5)
                continue
            i = self._joint_states.name.index('gripper')
            print({'Velocity': self._joint_states.velocity[i], 'Gripper State': \
                 self._joint_states.position[i], 'Desired Position': self._desired_position})
            if (self._desired_position is not None and
                self._joint_states.velocity[i] == 0.0 and
                abs(self._joint_states.position[i] - self._desired_position) > 0.015):
                # Sometimes, when we just give the gripper a commmand, the velocity might be 0
                self._gripper_pub.publish(SingleCommand('gripper', self._joint_states.position[i] + 0.01))
            time.sleep(1)
            prev_desired_position = self._joint_states.effort[i]


    def joint_callback(self, data):
        self._joint_states = data

    def gripper_desired_callback(self, data):
        if data.joint_name != 'gripper':
            return
        if self._desired_position is None or data.cmd != self._desired_position:
            self._desired_position_changed = True
        self._desired_position = data.cmd


def main():
    rospy.init_node("replab_gripper_monitor")
    gripper = WidowXGripper()
    rospy.spin()

if __name__ == '__main__':
    main()
