#!/bin/python3

import asyncio, evdev
import subprocess
from evdev import InputDevice, InputEvent, UInput, ecodes as e, list_devices, ff
controller_names = (
        'Microsoft X-Box 360 pad',
        'Generic X-Box pad',
        'OneXPlayer Gamepad',
        'Sony Interactive Entertainment Wireless Controller',
        )
global gamepad
# Identify system input event devices.
try:
    devices_original = [InputDevice(path) for path in list_devices()]
except:
    print("attempt failed")

async def print_events(device):
    async for event in device.async_read_loop():
        active = gamepad.active_keys()
        if active == [307, 315]:
           subprocess.run("./temperamental.py")


for device in devices_original:
    asyncio.ensure_future(print_events(device))
    if device.name in controller_names:
       gamepad = device


loop = asyncio.get_event_loop()
loop.run_forever()
