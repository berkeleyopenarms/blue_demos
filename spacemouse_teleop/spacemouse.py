#!/usr/bin/env python3
import usb.core
import usb.util
import sys
import time
import atexit
import threading
import os

class SpaceMouse:
    def __init__(self):
        space_mouse_ids = [
        #   (idVendor, idProduct)
            (0x46d, 0xc626),
            (0x256f, 0xc635),
        ]
        space_mouse_pro_ids = [
            (0x46d, 0xc62b),
        ]

        _device = None
        self._is_pro = False
        while _device is None:
            if space_mouse_ids:
                vendor_id, product_id = space_mouse_ids.pop()
                _device = usb.core.find(idVendor=vendor_id, idProduct=product_id)
            elif space_mouse_pro_ids:
                vendor_id, product_id = space_mouse_pro_ids.pop()
                _device = usb.core.find(idVendor=vendor_id, idProduct=product_id)
                self._is_pro = True
            else:
                raise SystemError('SpaceNavigator not found');

        self._reattach = False
        # is_kernel_driver_active is not supported for windows
        if os.name != "nt" and _device.is_kernel_driver_active(0):
            self._reattach = True
            _device.detach_kernel_driver(0)

        self._ep_in = _device[0][(0,0)][0]
        self._ep_out = _device[0][(0,0)][1]

        self._device = _device
        atexit.register(self.shutdown)

        self.input_pos = [0, 0, 0]
        self.input_rot = [0, 0, 0]
        self.input_button0 = False
        self.input_button1 = False

        self._alive = True

        threading.Thread(target=self._worker).start()

    def _worker(self):
        while self._alive:
            try:
                data = self._device.read(self._ep_in.bEndpointAddress, self._ep_in.bLength, timeout=1000)

                if data[0] == 1:
                    # translation packet
                    tx = data[1] + (data[2]*256)
                    ty = data[3] + (data[4]*256)
                    tz = data[5] + (data[6]*256)

                    if data[2] > 127:
                        tx -= 65536
                    if data[4] > 127:
                        ty -= 65536
                    if data[6] > 127:
                        tz -= 65536

                    self.input_pos = [tx, ty, tz]

                if data[0] == 2:
                    # rotation packet
                    rx = data[1] + (data[2]*256)
                    ry = data[3] + (data[4]*256)
                    rz = data[5] + (data[6]*256)

                    if data[2] > 127:
                        rx -= 65536
                    if data[4] > 127:
                        ry -= 65536
                    if data[6] > 127:
                        rz -= 65536

                    self.input_rot = [rx, ry, rz]

                if data[0] == 3:
                    # button packet
                    self.input_button0 = ((data[1] & 0b1) == 0b1)
                    self.input_button1 = ((data[1] >> 1 & 0b1) == 0b1)

            except usb.core.USBError:
                pass # timeout, probably

    def shutdown(self):
        print("Cleaning up USB stuff...")
        self._alive = False
        usb.util.dispose_resources(self._device)
        if os.name != "nt" and self._reattach:
            self._device.attach_kernel_driver(0)

