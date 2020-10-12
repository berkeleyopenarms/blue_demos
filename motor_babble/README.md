On the computer connected to the robot.
 * Run `roslaunch blue_bringup right.launch param_file:=blue_params.yaml`


On any computer on the network
 * `python play_motion.py`

Back on the computer connected to the robot.
 * `rosbag record -O sys_id_joint_data /joint_states /right_arm/motor_states`

Let the robot run for ~2 min
 * Then ctrl-c on the rosbag record
