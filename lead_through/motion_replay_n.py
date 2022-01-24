#!/usr/bin/python3
import pickle
import sys
import numpy as np
import time
import argparse
from blue_interface import BlueInterface


if __name__ == '__main__':
    # load file name
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        filename = "motion.pkl"

    # Blue Python interface
    arm_side = "right"
    address = "127.0.0.1"

    blue0 = BlueInterface(arm_side, address, port="9090")
    blue0.disable_control()
    blue1 = BlueInterface(arm_side, address, port="9091")
    blue1.disable_control()
    blue2 = BlueInterface(arm_side, address, port="9092")
    blue2.disable_control()

    data = pickle.load( open(filename, "rb")) #uses the pickle function to read the binary file created in record_poses.py
    joint_angle_list, _, gripper_list, frequency = data

    # If no argument is passed for replay frequency, play the recording at the rate it was recorded.
    input("Press enter to start replay. To exit, press <ctrl+c>.")
    while True:
        try:
            last_time = 0.0
            for i in range (len(joint_angle_list)):
                #if len(joint_angle_list[i]) == 7:
                blue0.set_joint_positions(np.array(joint_angle_list[i])) # tell the robot to go to a set of joint angles
                blue1.set_joint_positions(np.array(joint_angle_list[i])) # tell the robot to go to a set of joint angles
                blue2.set_joint_positions(np.array(joint_angle_list[i])) # tell the robot to go to a set of joint angles
                if gripper_list[i] < -0.2:
                    blue0.command_gripper(-1.3, 15.0)
                    blue1.command_gripper(-1.3, 15.0)
                    blue2.command_gripper(-1.3, 15.0)
                else:
                    blue0.command_gripper(0, 2.0)
                    blue1.command_gripper(0, 2.0)
                    blue2.command_gripper(0, 2.0)
                sleep_time = 1.0/frequency - (time.time() - last_time)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                last_time = time.time()

        except:
            print (sys.exc_info()[0])
            print ("Something went wrong... exiting")
            exit()
            pass
