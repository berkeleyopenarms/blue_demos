#!/usr/bin/env python3

from blue_interface import BlueInterface
import numpy as np
import time
import transformations as t
import spacemouse

if __name__ == '__main__':
    arm_side = "right"
    address = "127.0.0.1"

    # Python interface
    blue = BlueInterface(arm_side, address)
    blue.set_joint_positions(blue.get_joint_positions())

    # Set up a publisher for our cartesian pose command (a little sketchy)
    RBC = blue._RBC
    pose_target_publisher = RBC.publisher(
        "/{}_arm/pose_target/command".format(arm_side),
        "geometry_msgs/PoseStamped"
    )

    # 3D mouse ~~~
    mouse = spacemouse.SpaceMouse()

    # Initial position
    target_pose = blue.get_cartesian_pose()
    target_position = target_pose["position"]
    target_orientation = target_pose["orientation"]

    while True:
        ## Mouse coordinate frame stuff
        input_pos = np.asarray([
            mouse.input_pos[1],
            mouse.input_pos[0],
            -mouse.input_pos[2]
        ]) / 1000.0

        input_rot = t.quaternion_from_euler(*[
            mouse.input_rot[1] / 200.0,
            mouse.input_rot[0] / 200.0,
            -mouse.input_rot[2] / 150.0
        ])
        input_rot /= input_rot[3]

        ## Publishing stuff
        pose_target_msg = {
            "header": {
                "frame_id": "base_link"
            },
            "pose": {
                "position": dict(zip(
                    ("x", "y", "z"),
                    target_position + input_pos
                )),
                "orientation": dict(zip(
                    ("x", "y", "z", "w"),
                    t.quaternion_multiply(input_rot, target_orientation)
                ))
            }
        }
        pose_target_publisher.publish(pose_target_msg)

        ## Sleep
        time.sleep(0.01)
