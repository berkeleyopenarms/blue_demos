# Mercilessly kill any existing tmux session with the same name :)
tmux kill-session -t blue_demo_stack

# Create session
tmux new-session -d -s blue_demo_stack

# Make windows pre-populated with all the commands we need
tmux rename-window 'CORE'
sleep 0.2
tmux send-keys 'roslaunch blue_bringup right.launch param_file:=blue_configs/blue_right_v2.yaml version:=2 on_stand:=false'

tmux new-window -t blue_demo_stack -n 'RVIZ'
sleep 0.2
tmux send-keys 'roslaunch blue_bringup rviz.launch'

tmux new-window -t blue_demo_stack -n 'INVERSE KINEMATICS'
sleep 0.2
tmux send-keys 'roslaunch blue_teleop teleop_right.launch'

tmux new-window -t blue_demo_stack -n 'SPACEMOUSE'
sleep 0.2
tmux send-keys 'roslaunch marshmello_bringup camera_drivers.launch'

# Attach!
tmux select-window -t blue_demo_stack:0
tmux -2 attach-session -t blue_demo_stack
