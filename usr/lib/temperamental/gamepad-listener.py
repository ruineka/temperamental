#!/bin/python3

import asyncio, evdev
import subprocess
import time
from evdev import InputDevice, InputEvent, categorize, UInput, ecodes as e, list_devices, ff

## Wait for a bit to let services start
time.sleep(5)

controller_names = (
        'Microsoft X-Box 360 pad',
        'Generic X-Box pad',
        'OneXPlayer Gamepad',
        'Sony Interactive Entertainment Wireless Controller',
        'Handheld Controller',
        'Microsoft Controller',
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
        
        if event.type == 1 and active != []:
           print("Currently pressed button IDs")
           print(active)
        if active == [314, 315] and event.type == 1 and active != []:
           subprocess.run("/usr/lib/temperamental/./inject-gamescope.sh")


for device in devices_original:
    asyncio.ensure_future(print_events(device))
    if device.name in controller_names:
       gamepad = device


loop = asyncio.get_event_loop()
loop.run_forever()
