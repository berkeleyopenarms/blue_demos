#!/usr/bin/env python3

# A basic example of using BlueInterface for joint positions control.

from blue_interface import BlueInterface
import numpy as np
import sys

assert len(sys.argv) == 2

side = "right"
ip = sys.argv[1]
blue = BlueInterface(side, ip)

current_joints = blue.get_joint_positions()
blue.set_joint_positions(current_joints, duration=3.0)

while True:
    pass

# When this script terminates (eg via Ctrl+C), the robot will automatically
# stop all controllers and go back to gravity compensation mode

