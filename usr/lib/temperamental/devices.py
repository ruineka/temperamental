#!/bin/python3

import sys

system_id = open("/sys/devices/virtual/dmi/id/product_name",
                 "r").read().strip()
print("Detected: " + system_id)

if system_id in (
        "ONEXPLAYER Mini Pro",
        "ONEXPLAYER 2"
):
    SYSTEM_NAME = "ONE XPLAYER"
    MIN_TDP = '5000'
    STEP_ONE = '10000'
    STEP_TWO = '15000'
    MAX_TDP = '28000'
    QUIET_FAN_CONFIG = "/usr/share/temperamental/profiles/AOKZOE-MINIPRO-QUIET.yaml"
    BALANCED_FAN_CONFIG = "/usr/share/temperamental/profiles/AOKZOE-MINIPRO-BALANCED.yaml"
    PERF_FAN_CONFIG = "/usr/share/temperamental/profiles/AOKZOE-MINIPRO-PERF.yaml"
elif system_id == "Dev One Notebook PC":
    SYSTEM_NAME = system_id
    MIN_TDP = "5000"
    STEP_ONE = "10000"
    STEP_TWO = '12000'
    MAX_TDP = '15000'
    QUIET_FAN_CONFIG = ""
    BALANCED_FAN_CONFIG = ""
    PERF_FAN_CONFIG = ""
elif system_id in (
        "ONE XPLAYER",
        "ONEXPLAYER mini A07",
):
    SYSTEM_NAME = "ONE XPLAYER"
    MIN_TDP = "5000"
    STEP_ONE = "10000"
    STEP_TWO = '15000'
    MAX_TDP = '25000'
    QUIET_FAN_CONFIG = ""
    BALANCED_FAN_CONFIG = ""
    PERF_FAN_CONFIG = ""
elif system_id == "Jupiter":
    SYSTEM_NAME = system_id
    MIN_TDP = "5000"
    STEP_ONE = "10000"
    STEP_TWO = '12000'
    MAX_TDP = '15000'
    QUIET_FAN_CONFIG = ""
    BALANCED_FAN_CONFIG = ""
    PERF_FAN_CONFIG = ""
elif system_id == "AIR":
    SYSTEM_NAME = "AYA NEO AIR"
    MIN_TDP = "5000"
    STEP_ONE = "10000"
    STEP_TWO = '12000'
    MAX_TDP = '15000'
    QUIET_FAN_CONFIG = ""
    BALANCED_FAN_CONFIG = ""
    PERF_FAN_CONFIG = ""
elif system_id == "AIR PRO":
    SYSTEM_NAME = "AYA NEO AIR"
    MIN_TDP = "5000"
    STEP_ONE = "10000"
    STEP_TWO = '12000'
    MAX_TDP = '18000'
    QUIET_FAN_CONFIG = ""
    BALANCED_FAN_CONFIG = ""
    PERF_FAN_CONFIG = ""
elif system_id in (
        "AYA NEO FOUNDER",
        "AYA NEO 2021",
        "AYANEO 2021",
        "AYANEO 2021 Pro",
        "AYANEO 2021 Pro Retro Power",
):
    SYSTEM_NAME = "AYA NEO"
    MIN_TDP = '5000'
    STEP_ONE = '10000'
    STEP_TWO = '15000'
    MAX_TDP = '25000'
    QUIET_FAN_CONFIG = ""
    BALANCED_FAN_CONFIG = ""
    PERF_FAN_CONFIG = ""
elif system_id in (
        "AYANEO NEXT",
        "AYANEO NEXT PRO",
        "NEXT PRO",
        "NEXT"
):
    SYSTEM_NAME = "AYA NEO NEXT"
    MIN_TDP = '5000'
    STEP_ONE = '10000'
    STEP_TWO = '15000'
    MAX_TDP = '28000'
    QUIET_FAN_CONFIG = ""
    BALANCED_FAN_CONFIG = ""
    PERF_FAN_CONFIG = ""
elif system_id == "AOKZOE A1 AR07":
    SYSTEM_NAME = system_id
    MIN_TDP = "5000"
    STEP_ONE = "10000"
    STEP_TWO = '15000'
    MAX_TDP = '28000'
    QUIET_FAN_CONFIG = "/usr/share/temperamental/profiles/AOKZOE-MINIPRO-QUIET.yaml"
    BALANCED_FAN_CONFIG = "/usr/share/temperamental/profiles/AOKZOE-MINIPRO-BALANCED.yaml"
    PERF_FAN_CONFIG = "/usr/share/temperamental/profiles/AOKZOE-MINIPRO-PERF.yaml"
else:
    print(system_id + " " + "is not currently compatible, if you know the limitations of your hardware you can add support on your own")
    sys.exit(-1)
