#!/usr/bin/python3
import pickle
import sys
import numpy as np
import time
import argparse
from blue_interface import BlueInterface


if __name__ == '__main__':
    # Blue Python interface
    arm_side = "right"
    address = "127.0.0.1"
    blue = BlueInterface(arm_side, address)
    blue.disable_control()
