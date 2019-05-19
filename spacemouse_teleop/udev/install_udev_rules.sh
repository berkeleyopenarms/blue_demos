set -x

# Copy rules
sudo cp 50-spacemouse.rules /lib/udev/rules.d

# Reload
sudo udevadm control --reload
sudo udevadm trigger

# Add to group
sudo adduser $USER plugdev
