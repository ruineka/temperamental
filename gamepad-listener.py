#!/bin/python3

import asyncio, evdev

gamepad = evdev.InputDevice('/dev/input/event17')

async def print_events(device):
    async for event in device.async_read_loop():
        print(device.path, evdev.categorize(event), sep=': ')

for device in gamepad,:
    asyncio.ensure_future(print_events(device))

loop = asyncio.get_event_loop()
loop.run_forever()
