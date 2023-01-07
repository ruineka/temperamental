#!/bin/python3
import pygame
import pygame_gui
import os
import subprocess
import os.path
import sys

system_id = open("/sys/devices/virtual/dmi/id/product_name", "r").read().strip()
print("Detected: " + system_id)

if system_id in (
        "ONEXPLAYER Mini Pro",
        "AOKZOE A1 AR07"
        ):
        MIN_TDP='5000'
        STEP_ONE='10000'
        STEP_TWO='15000'
        MAX_TDP='28000'
elif system_id == "Dev One Notebook PC":
   MIN_TDP="5000"
   STEP_ONE="10000"
   STEP_TWO='12000'
   MAX_TDP='15000'
elif system_id == "ONE XPLAYER":
   MIN_TDP="5000"
   STEP_ONE="10000"
   STEP_TWO='15000'
   MAX_TDP='25000'
else:
   print(system_id + " " + "is not currently compatible, if you know the limitations of your hardware you can add support on your own")
   sys.exit(-1)
