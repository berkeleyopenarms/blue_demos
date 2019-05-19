#!/usr/bin/python3
import numpy as np
import pickle
import time
import sys
from blue_interface import BlueInterface  # this is the API for the robot

if __name__ == '__main__':
    # motion file name
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        filename = "motion.pkl"
    frequency = 100 # In Hertz

    # Blue Python interface
    arm_side = "right"
    address = "127.0.0.1"
    blue = BlueInterface(arm_side, address)
    blue.disable_control() #this turns off any other control currently on the robot (leaves it in gravtiy comp mode)

    joint_angle_list = [] #Initialize the list to hold our joint positions
    pose_list = []
    gripper_list = []

    input("Press enter to start recording. To finish recording press <ctrl+c>.")
    try:
        last_time = 0.0
        while True:
            position = blue.get_joint_positions() #record the pose, this function returns a dictionary object
            joint_angle_list.append(position)
            pose = blue.get_cartesian_pose()
            pose_list.append(pose)
            gripper_pos = blue.get_gripper_position()
            gripper_list.append(gripper_pos)
            # print("Position recorded!")
            sleep_time = 1.0/frequency - (time.time() - last_time)
            if sleep_time > 0:
                time.sleep(sleep_time)
            last_time = time.time()
    except:
        print(joint_angle_list)

        if len(joint_angle_list)==0:
            print('You did not save any positions')
        else:
            pickle.dump((joint_angle_list, pose_list, gripper_list, frequency), open(filename, "wb")) #uses the pickle function to write a binary file
            print('Your position list has been saved in the directory')
        sys.exit()
