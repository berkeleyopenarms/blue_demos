#!/usr/bin/env python3

from blue_interface import BlueInterface
import numpy as np
import time
import transformations as t
import spacemouse
import sys

if __name__ == '__main__':
    arm_side = "right"
    assert len(sys.argv) == 2
    address = sys.argv[1]

    # Python interface
    blue = BlueInterface(arm_side, address)
    home = [-0.433836, -1.16384, 0.75438465, -1.58150699, -0.05635529, -1.67967716, -0.13010218]
    home = [0.0, -1.571, 0.0, -1.571, 0.0, -1.571, 0.0]
    blue.set_joint_positions( # TODO: this sometimes fights with the IK solver, and makes the robot really jittery
        home,
        duration=1.0,
        # soft_position_control=True
    )
    position_control_mode = blue._control_mode # super sketchy


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

    # Gripper state
    gripper_closed = False

    #
    prev_input_button0 = False

    disabled = False

    print("Ready!")

    while True:
        if not mouse.input_button0 and prev_input_button0:
            print(disabled)
            disabled = not disabled

        if disabled:
            blue.disable_control()
            current_pose = blue.get_cartesian_pose()
            target_position = current_pose["position"]
            target_orientation = current_pose["orientation"]
        else:
            blue._set_control_mode(position_control_mode) # position control mode

            ## Read current state
            current_pose = blue.get_cartesian_pose()
            current_position = current_pose["position"]
            current_orientation = current_pose["orientation"]

            ## Compute new target pose
            if np.linalg.norm(mouse.input_pos) > 10:
                input_position = np.asarray([
                    mouse.input_pos[1],
                    mouse.input_pos[0],
                    -mouse.input_pos[2]
                ]) / 1000.0
                target_position = current_position + input_position

            if np.linalg.norm(mouse.input_rot) > 10:
                input_rot = t.quaternion_from_euler(*[
                    mouse.input_rot[1] / 200.0,
                    mouse.input_rot[0] / 200.0,
                    -mouse.input_rot[2] / 150.0
                ])
                target_orientation = t.quaternion_multiply(input_rot, current_orientation)

            ## Publishing target pose
            pose_target_msg = {
                "header": {
                    "frame_id": "base_link"
                },
                "pose": {
                    "position": dict(zip(
                        ("x", "y", "z"),
                        target_position
                    )),
                    "orientation": dict(zip(
                        ("x", "y", "z", "w"),
                        target_orientation
                    ))
                }
            }
            pose_target_publisher.publish(pose_target_msg)

            ## Gripper stuff
            if gripper_closed != mouse.input_button1:
                if gripper_closed:
                    # open gripper
                    blue.command_gripper(-1.0, 10.0)
                else:
                    # close gripper
                    blue.command_gripper(2.00, 30.0)
                gripper_closed = mouse.input_button1

        prev_input_button0 = mouse.input_button0

        ## Sleep
        time.sleep(0.01)
