# Using the space mouse
Setup instructions are below

## Ubuntu
* `cd blue_demos/spacemouse_teleop/udev`
* `./install_udev_rules.sh`
* Then log out and log back in.

## Windows
* Install libusb for windows
    * Follow the instructions here https://github.com/pyusb/pyusb/issues/120#issuecomment-322058585

## Mac (untested)
* `brew install libusb`

## Testing your mouse
After following the above instructions, make sure the mouse works.
* `cd blue_demos/spacemouse_teleop`
* `python spacemouse_test.py`
You should see a print out every second of the current state of the space mouse.
Try using your mouse and make sure the print out values change!
