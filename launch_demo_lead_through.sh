# Mercilessly kill any existing tmux session with the same name :)
tmux kill-session -t blue_demo_stack

# Create session
tmux new-session -d -s blue_demo_stack -c ~

# Make windows pre-populated with all the commands we need
tmux rename-window 'ARM1'
sleep 0.2
tmux send-keys 'export ROS_MASTER_URI=http://localhost:11311' Enter
tmux send-keys 'roslaunch blue_bringup right.launch param_file:=blue_configs/blue_right_v2.yaml version:=2 on_stand:=false rosbridge_port:=9091'

tmux new-window -t blue_demo_stack -n 'ARM2' -c ~
sleep 0.2
tmux send-keys 'export ROS_MASTER_URI=http://localhost:11312' Enter
tmux send-keys 'roslaunch blue_bringup right.launch param_file:=blue_configs/blue_right_v2.yaml version:=2 on_stand:=false rosbridge_port:=9092'

tmux new-window -t blue_demo_stack -n 'ARM3' -c ~
sleep 0.2
tmux send-keys 'export ROS_MASTER_URI=http://localhost:11313' Enter
tmux send-keys 'roslaunch blue_bringup right.launch param_file:=blue_configs/blue_right_v2.yaml version:=2 on_stand:=false rosbridge_port:=9093'

tmux new-window -t blue_demo_stack -n 'SPACEMOUSE' -c ~/blue_demos/lead_through/motion_replay.py wave_many.py
sleep 0.2
tmux send-keys 'python3 spacemouse_teleop.py'

# Attach!
tmux select-window -t blue_demo_stack:0
tmux -2 attach-session -t blue_demo_stack
