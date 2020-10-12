#!/usr/bin/python3
import pickle
import sys
import numpy as np
import time
import argparse
from blue_interface import BlueInterface

MIN_JOINTS = np.array([-3.5, -2.45, -2.6, -2.45, -2.6, -2.45, -2.6]) + 1
MAX_JOINTS = np.array([2.4, 0.6, 2.6, 0.6, 2.6, 0.6, 2.6]) - 1


if __name__ == '__main__':
    # Blue Python interface
    arm_side = "right"
    address = "127.0.0.1"
    blue = BlueInterface(arm_side, address)
    blue.disable_control()

    center_joints = (MIN_JOINTS + MAX_JOINTS) / 2
    joint_amplitude = MAX_JOINTS - center_joints
    blue.set_joint_positions(center_joints, duration=5.0, soft_position_control=True)
    frequency = 0.5
    w = 2 * np.pi/ 30
    def control_input(t):
        return np.array([np.sin(w * t * np.sqrt(i)) for i in range(1,8)])

    try:
        start_time = time.time()
        last_time = start_time
        while True:
            joints = control_input(last_time - start_time) * joint_amplitude + center_joints
            blue.set_joint_positions(joints, duration=1/frequency, soft_position_control=True) # tell the robot to go to a set of joint angles
            last_time = time.time()
    except Exception as e:
        print(e)
        print(sys.exc_info()[0])
        print("Something went wrong... exiting")
        pass
