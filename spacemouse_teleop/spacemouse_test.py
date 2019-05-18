import time
import spacemouse

mouse = spacemouse.SpaceMouse()
while True:
    print(mouse.input_pos)
    time.sleep(0.1)
mouse.shutdown()

# from __future__ import print_function
# import usb.core
# import usb.util
# import sys
# import time
#
# # Look for SpaceNavigator
# usb_ids = [
# #   (idVendor, idProduct)
#     (0x46d, 0xc626),
#     (0x256f, 0xc635)
# ]
# dev = None
# while dev is None:
#     if usb_ids:
#         vendor_id, product_id = usb_ids.pop()
#         dev = usb.core.find(idVendor=vendor_id, idProduct=product_id)
#     else:
#         raise SystemError('SpaceNavigator not found');
#
# print('SpaceNavigator found!')
# # print(dev)
#
# # cfg = dev.get_active_configuration()
# # print('cfg is ', cfg)
# # intf = cfg[(0,0)]
# # print('intf is ', intf)
# # ep = usb.util.find_descriptor(intf, custom_match = lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN)
# # print('ep is ', ep)
#
# reattach = False
# if dev.is_kernel_driver_active(0):
#     reattach = True
#     dev.detach_kernel_driver(0)
#
# ep_in = dev[0][(0,0)][0]
# ep_out = dev[0][(0,0)][1]
#
# print('')
# print('Exit by pressing any button on the SpaceNavigator')
# print('')
#
# run = True
# while run:
#     try:
#         data = dev.read(ep_in.bEndpointAddress, ep_in.bLength, 0)
#         # raw data
#         # print(data)
#
#         # print(it correctly T: x,y,z R: x,y,z)
#         if data[0] == 1:
#             # translation packet
#             tx = data[1] + (data[2]*256)
#             ty = data[3] + (data[4]*256)
#             tz = data[5] + (data[6]*256)
#
#             if data[2] > 127:
#                 tx -= 65536
#             if data[4] > 127:
#                 ty -= 65536
#             if data[6] > 127:
#                 tz -= 65536
#             # print("T: ", tx, ty, tz, end="")
#
#         if data[0] == 2:
#             # rotation packet
#             rx = data[1] + (data[2]*256)
#             ry = data[3] + (data[4]*256)
#             rz = data[5] + (data[6]*256)
#
#             if data[2] > 127:
#                 rx -= 65536
#             if data[4] > 127:
#                 ry -= 65536
#             if data[6] > 127:
#                 rz -= 65536
#             # print("R: ", rx, ry, rz)
#
#         if data[0] == 3 and data[1] == 0:
#             # button packet - exit on the release
#             run = False
#
#         print("\r T: \t {} \t {} \t {} \t R: \t {} \t {} \t {}".format(
#             tx, ty, tz,
#             rx, ry, rz
#         ))
#     except usb.core.USBError:
#         print("USB error")
#     except:
#         print("read failed")
#
#     time.sleep(0.01)
#
# # end while
# usb.util.dispose_resources(dev)
#
# if reattach:
#     dev.attach_kernel_driver(0)
