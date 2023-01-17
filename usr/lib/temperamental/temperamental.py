#!/bin/python3

import pygame
import pygame_gui
import os
import os.path
import subprocess
import sys
import GUI
import time
from os import path
from devices import MIN_TDP, STEP_ONE, STEP_TWO, MAX_TDP, QUIET_FAN_CONFIG, BALANCED_FAN_CONFIG, PERF_FAN_CONFIG

# Define variables

RYZENADJ = '/usr/bin/temperamental-polkit-helpers/ryzenadj-polkit-helper'
HHFC = 'hhfc -c'
FAN_PROFILE_DIR = "/usr/share/temperamental/profiles/"
PARAMS = ''
GUI.currentTDP = int(MIN_TDP) // 1000
MAX_PERFORMANCE = "--max-performance"
POWER_SAVER = "--power-saving"
STAPM_LIMIT = "--stapm-limit"
SLOW_LIMIT = "--slow-limit"
FAST_LIMIT = "--fast-limit"
TCTL_TEMP = "--tctl-temp"
TEMP_LIMIT = "90"
TARGET_TDP = MIN_TDP

# Default values based on Xbox Series X Controller
BUTTON_A = 0
BUTTON_B = 1
BUTTON_X = 2
BUTTON_Y = 3
BUTTON_LB = 6
BUTTON_RB = 7
BUTTON_LT = 4  # Axis
BUTTON_RT = 5  # Axis
BUTTON_L3 = 13
BUTTON_R3 = 14
BUTTON_START = 11
BUTTON_SELECT = 10

# Grab current values before changes
DEFAULT_SMT = subprocess.getoutput('cat /sys/devices/system/cpu/smt/control')
DEFAULT_BOOST = subprocess.getoutput(
    'cat /sys/devices/system/cpu/cpufreq/boost')
subprocess.run(RYZENADJ + ' ' + '-i', shell=True)


def get_profile():
    print("Grab profiles")


def set_gamepad_button(event):
    global controller_list
    global controller_type
    global gamepad
    controller_type = ""
    CONTROLLERS = {}
    i = 0
    while i < len(controller_list):
        CONTROLLERS[i] = (f"{pygame.joystick.Joystick(i).get_name()}")
        i = i + 1

    match CONTROLLERS[event.instance_id]:

        case "Xbox Series X Controller":
            controller_type = "Xbox Series X"
            controller_id = CONTROLLERS[event.instance_id]
            gamepad = pygame.joystick.Joystick(event.instance_id)

        case "Wireless Controller":
            controller_type = "PS5"
            controller_id = CONTROLLERS[event.instance_id]
            gamepad = pygame.joystick.Joystick(event.instance_id)
        case "Sony Interactive Entertainment Wireless Controller":
            controller_type = "PS5"
            controller_id = CONTROLLERS[event.instance_id]
            gamepad = pygame.joystick.Joystick(event.instance_id)
        case "Xbox 360 Controller":
            controller_type = "Xbox 360"
            controller_id = CONTROLLERS[event.instance_id]
            gamepad = pygame.joystick.Joystick(event.instance_id)
    try:
        if pygame.JOYAXISMOTION:
            get_axis(event, controller_type)
    except:
        print("Button wasn't an axis")
    try:
        if pygame.JOYHATMOTION:
            get_hat(event)
    except:
        print("Button wasn't a button")


def set_tdp_values(button_number):
    global TARGET_TDP
    match button_number:

        case 0:
            TARGET_TDP = MIN_TDP
            GUI.currentTDP = int(MIN_TDP) // 1000
            GUI.CURRENT_TDP_VALUE.set_text(
                "Current TDP Value:" + " " + str(int(MIN_TDP) // 1000) + "W TDP")

        case 1:
            TARGET_TDP = STEP_ONE
            GUI.currentTDP = int(STEP_ONE) // 1000
            GUI.CURRENT_TDP_VALUE.set_text(
                "Current TDP Value:" + " " + str(int(STEP_ONE) // 1000) + "W TDP")

        case 2:
            TARGET_TDP = STEP_TWO
            GUI.currentTDP = int(STEP_TWO) // 1000
            GUI.CURRENT_TDP_VALUE.set_text(
                "Current TDP Value:" + " " + str(int(STEP_ONE) // 1000) + "W TDP")
        case 3:
            TARGET_TDP = MAX_TDP
            GUI.currentTDP = int(MAX_TDP) // 1000
            GUI.CURRENT_TDP_VALUE.set_text(
                "Current TDP Value:" + " " + str(int(MAX_TDP) // 1000) + "W TDP")
        case 4:
            TARGET_TDP = str(int(TARGET_TDP) + 1000)
            GUI.currentTDP = TARGET_TDP
        case 5:
            TARGET_TDP = str(int(TARGET_TDP) - 1000)
            GUI.currentTDP = TARGET_TDP


def check_depends():
    # Check for dependencies
    if path.exists("/usr/bin/ryzenadj"):
        GUI.RYZENADJ_STATUS_LABEL.set_text("Ryzenadj: Found")
    else:
        GUI.RYZENADJ_STATUS_LABEL.set_text("Ryzenadj: Not Found")

    if path.exists("/usr/lib/systemd/system/handycon.service"):
        GUI.HHFC_LABEL.set_text("HHFC: Found")
    else:
        GUI.HHFC_LABEL.set_text("HHFC: Not Found")


def update_hud():
    # Update Hud Values
    if GUI.currentTDP != 0:
        GUI.CURRENT_TDP_VALUE.set_text(
            "Current TDP Target:" + " " + str(GUI.currentTDP) + "W")
        if GUI.SMT == "on":
            GUI.SMT_LABEL.set_text("SMT Enabled")
        else:
            GUI.SMT_LABEL.set_text("SMT Disabled")
        if GUI.BOOST == '1':
            GUI.BOOST_LABEL.set_text("Boost Enabled")
        else:
            GUI.BOOST_LABEL.set_text("Boost Disabled")


def gamepad_button_events(event):

    global controller_type

    match controller_type:
        case "Xbox Series X":

            if event.button == 0:
                button_number = 0
                set_tdp_values(button_number)

            if event.button == 1:
                button_number = 1
                set_tdp_values(button_number)

            if event.button == 3:
                button_number = 3
                set_tdp_values(button_number)
            if event.button == 4:
                button_number = 2
                set_tdp_values(button_number)

            if event.button == 6:
                if subprocess.getoutput('cat /sys/devices/system/cpu/cpufreq/boost') == '1':
                    GUI.BOOST = '0'
                else:
                    GUI.BOOST = '1'
                subprocess.run('/usr/bin/echo ' + GUI.BOOST +
                               ' | sudo tee /sys/devices/system/cpu/cpufreq/boost', shell=True)
            if event.button == 7:

                if subprocess.getoutput('cat /sys/devices/system/cpu/smt/control') == 'on':
                    GUI.SMT = 'off'
                else:
                    GUI.SMT = 'on'
                subprocess.run('/usr/bin/echo ' + GUI.SMT +
                               ' | sudo tee /sys/devices/system/cpu/smt/control', shell=True)
            if event.button == 10:
                sys.exit(0)
            if event.button == 11:
                print(RYZENADJ + ' ' + STAPM_LIMIT + "=" + TARGET_TDP + " " + FAST_LIMIT + "=" +
                      TARGET_TDP + " " + SLOW_LIMIT + "=" + TARGET_TDP + " " + TCTL_TEMP + "=" + TEMP_LIMIT)
                subprocess.run(RYZENADJ + ' ' + STAPM_LIMIT + "=" + TARGET_TDP + " " + FAST_LIMIT + "=" +
                               TARGET_TDP + " " + SLOW_LIMIT + "=" + TARGET_TDP + " " + TCTL_TEMP + "=" + TEMP_LIMIT, shell=True)
        case "Xbox 360":

            if event.button == 0:
                button_number = 0
                set_tdp_values(button_number)

            if event.button == 1:
                button_number = 1
                set_tdp_values(button_number)

            if event.button == 3:
                button_number = 2
                set_tdp_values(button_number)

            if event.button == 2:
                button_number = 3
                set_tdp_values(button_number)

            if event.button == 4:
                if subprocess.getoutput('cat /sys/devices/system/cpu/cpufreq/boost') == '1':
                    GUI.BOOST = '0'
                else:
                    GUI.BOOST = '1'
                subprocess.run('/usr/bin/echo ' + GUI.BOOST +
                               ' | sudo tee /sys/devices/system/cpu/cpufreq/boost', shell=True)

            if event.button == 5:
                if subprocess.getoutput('cat /sys/devices/system/cpu/smt/control') == 'on':
                    GUI.SMT = 'off'
                else:
                    GUI.SMT = 'on'
                subprocess.run('/usr/bin/echo ' + GUI.SMT +
                               ' | sudo tee /sys/devices/system/cpu/smt/control', shell=True)

            if event.button == 6:
                sys.exit(0)
            if event.button == 7:
                print(RYZENADJ + ' ' + STAPM_LIMIT + "=" + TARGET_TDP + " " + FAST_LIMIT + "=" +
                      TARGET_TDP + " " + SLOW_LIMIT + "=" + TARGET_TDP + " " + TCTL_TEMP + "=" + TEMP_LIMIT)
                subprocess.run(RYZENADJ + ' ' + STAPM_LIMIT + "=" + TARGET_TDP + " " + FAST_LIMIT + "=" +
                               TARGET_TDP + " " + SLOW_LIMIT + "=" + TARGET_TDP + " " + TCTL_TEMP + "=" + TEMP_LIMIT, shell=True)

        case "PS5":

            if event.button == 0:
                button_number = 0
                set_tdp_values(button_number)

            if event.button == 1:
                button_number = 1
                set_tdp_values(button_number)

            if event.button == 2:
                button_number = 2
                set_tdp_values(button_number)

            if event.button == 3:
                button_number = 3
                set_tdp_values(button_number)

            if event.button == 4:
                if subprocess.getoutput('cat /sys/devices/system/cpu/cpufreq/boost') == '1':
                    GUI.BOOST = '0'
                else:
                    GUI.BOOST = '1'
                subprocess.run('/usr/bin/echo ' + GUI.BOOST +
                               ' | sudo tee /sys/devices/system/cpu/cpufreq/boost', shell=True)

            if event.button == 5:
                if subprocess.getoutput('cat /sys/devices/system/cpu/smt/control') == 'on':
                    GUI.SMT = 'off'
                else:
                    GUI.SMT = 'on'
                subprocess.run('/usr/bin/echo ' + GUI.SMT +
                               ' | sudo tee /sys/devices/system/cpu/smt/control', shell=True)

            if event.button == 6:
                PARAMS = MAX_PERFORMANCE
                subprocess.run(RYZENADJ + ' ' + PARAMS, shell=True)
                GUI.POWER_PROFILE_LABEL.set_text("Power Profile: Performance")
            if event.button == 7:
                PARAMS = POWER_SAVER
                subprocess.run(RYZENADJ + ' ' + PARAMS, shell=True)
                GUI.POWER_PROFILE_LABEL.set_text("Power Profile: Power Saver")

            if event.button == 8:
                sys.exit(0)
            if event.button == 9:
                print(RYZENADJ + ' ' + STAPM_LIMIT + "=" + TARGET_TDP + " " + FAST_LIMIT + "=" +
                      TARGET_TDP + " " + SLOW_LIMIT + "=" + TARGET_TDP + " " + TCTL_TEMP + "=" + TEMP_LIMIT)
                subprocess.run(RYZENADJ + ' ' + STAPM_LIMIT + "=" + TARGET_TDP + " " + FAST_LIMIT + "=" +
                               TARGET_TDP + " " + SLOW_LIMIT + "=" + TARGET_TDP + " " + TCTL_TEMP + "=" + TEMP_LIMIT, shell=True)


def get_axis(event, controller_type):

    if pygame.joystick.Joystick(event.instance_id) and controller_type == "Xbox Series X" and pygame.JOYAXISMOTION and event.axis == 5:
        PARAMS = MAX_PERFORMANCE
        subprocess.run(RYZENADJ + ' ' + PARAMS, shell=True)
        GUI.POWER_PROFILE_LABEL.set_text("Power Profile: Performance")

    if pygame.joystick.Joystick(event.instance_id) and controller_type == "Xbox Series X" and pygame.JOYAXISMOTION and event.axis == 2:
        PARAMS = POWER_SAVER
        subprocess.run(RYZENADJ + ' ' + PARAMS, shell=True)
        GUI.POWER_PROFILE_LABEL.set_text("Power Profile: Power Saver")

    if pygame.joystick.Joystick(event.instance_id) and controller_type == "Xbox 360" and pygame.JOYAXISMOTION and event.axis == 5:
        PARAMS = MAX_PERFORMANCE
        subprocess.run(RYZENADJ + ' ' + PARAMS, shell=True)
        GUI.POWER_PROFILE_LABEL.set_text("Power Profile: Performance")

    if pygame.joystick.Joystick(event.instance_id) and controller_type == "Xbox 360" and pygame.JOYAXISMOTION and event.axis == 2:
        PARAMS = POWER_SAVER
        subprocess.run(RYZENADJ + ' ' + PARAMS, shell=True)
        GUI.POWER_PROFILE_LABEL.set_text("Power Profile: Power Saver")


def get_hat(event):
    global TARGET_TDP
    hats = gamepad.get_numhats()

    for i in range(hats):
        hat = gamepad.get_hat(i)

    if gamepad.get_hat(i) == (1, 0):
        TARGET_TDP = str(int(TARGET_TDP) + 1000)
        GUI.currentTDP = str(int(TARGET_TDP) // 1000)
    if gamepad.get_hat(i) == (-1, 0):
        TARGET_TDP = str(int(TARGET_TDP) - 1000)
        GUI.currentTDP = str(int(TARGET_TDP) // 1000)


def keyboard_mouse_events(event):

    if event.ui_element == GUI.SMT_BUTTON:
        if subprocess.getoutput('cat /sys/devices/system/cpu/smt/control') == 'on':
            GUI.SMT = 'off'
        else:
            GUI.SMT = 'on'
        subprocess.run('/usr/bin/echo ' + GUI.SMT +
                       ' | sudo tee /sys/devices/system/cpu/smt/control', shell=True)
        print("Toggled SMT")

    if event.ui_element == GUI.MIN_BUTTON:
        button_number = 0
        set_tdp_values(button_number)

    if event.ui_element == GUI.TIER1_BUTTON:
        button_number = 1
        set_tdp_values(button_number)

    if event.ui_element == GUI.TIER2_BUTTON:
        button_number = 2
        set_tdp_values(button_number)

    if event.ui_element == GUI.MAX_BUTTON:
        button_number = 3
        set_tdp_values(button_number)

    if event.ui_element == GUI.BOOST_BUTTON:
        if subprocess.getoutput('cat /sys/devices/system/cpu/cpufreq/boost') == '1':
            GUI.BOOST = '0'
        else:
            GUI.BOOST = '1'
        subprocess.run('/usr/bin/echo ' + GUI.BOOST +
                       ' | sudo tee /sys/devices/system/cpu/cpufreq/boost', shell=True)
        print("Toggled Boost")
    if event.ui_element == GUI.DEFAULT_BUTTON:
        subprocess.run('/usr/bin/echo ' + DEFAULT_BOOST +
                       ' | sudo tee /sys/devices/system/cpu/cpufreq/boost', shell=True)
        subprocess.run('/usr/bin/echo ' + DEFAULT_SMT +
                       ' | sudo tee /sys/devices/system/cpu/smt/control', shell=True)

    if event.ui_element == GUI.PERFORMANCE_BUTTON:
        PARAMS = MAX_PERFORMANCE
        subprocess.run(RYZENADJ + ' ' + PARAMS, shell=True)
        GUI.POWER_PROFILE_LABEL.set_text("Power Profile: Performance")

    if event.ui_element == GUI.POWERSAVER_BUTTON:
        PARAMS = POWER_SAVER
        subprocess.run(RYZENADJ + ' ' + PARAMS, shell=True)
        GUI.POWER_PROFILE_LABEL.set_text("Power Profile: Power Saver")

    if event.ui_element == GUI.QUIET_FAN:
        GUI.FAN_CURVE_LABEL.set_text("Fan Curve: Quiet")
        subprocess.run(HHFC + ' ' + QUIET_FAN_CONFIG, shell=True)

    if event.ui_element == GUI.BALANCED_FAN:
        subprocess.run(HHFC + ' ' + BALANCED_FAN_CONFIG, shell=True)
        GUI.FAN_CURVE_LABEL.set_text("Fan Curve: Balanced")

    if event.ui_element == GUI.PERFORMANCE_FAN:
        subprocess.run(HHFC + ' ' + PERF_FAN_CONFIG, shell=True)
        GUI.FAN_CURVE_LABEL.set_text("Fan Curve: Performance")

    if event.ui_element == GUI.CLOSE_BUTTON:
        sys.exit(0)

    if event.ui_element == GUI.POSITIVE_INCREMENT_BUTTON and GUI.currentTDP != int(MAX_TDP) // 1000:
        GUI.currentTDP = GUI.currentTDP + 1
        button_number = 4
        set_tdp_values(button_number)

    if event.ui_element == GUI.NEGATIVE_INCREMENT_BUTTON and GUI.currentTDP != int(MIN_TDP) // 1000:
        GUI.currentTDP = GUI.currentTDP - 1
        button_number = 5
        set_tdp_values(button_number)

    if event.ui_element == GUI.APPLY_CHANGES:
        print("Writing" + " " + TARGET_TDP + " " + "with Ryzenadj")
        print(RYZENADJ + ' ' + STAPM_LIMIT + "=" + TARGET_TDP + " " + FAST_LIMIT + "=" +
              TARGET_TDP + " " + SLOW_LIMIT + "=" + TARGET_TDP + " " + TCTL_TEMP + "=" + TEMP_LIMIT)
        subprocess.run(RYZENADJ + ' ' + STAPM_LIMIT + "=" + TARGET_TDP + " " + FAST_LIMIT + "=" +
                       TARGET_TDP + " " + SLOW_LIMIT + "=" + TARGET_TDP + " " + TCTL_TEMP + "=" + TEMP_LIMIT, shell=True)


def __main__():

    global gamepad
    global controller_list

    joysticks = {}
    controller_list = {}
    pygame.init()
    isRunning = True
    button_on = False

    while isRunning:

        time_delta = clock.tick(60)/1000.0
        GUI.window_surface.blit(GUI.background, (0, 0))
        GUI.window_surface.fill((0, 10, 25))
        check_depends()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False

            if event.type == pygame.USEREVENT:

                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    keyboard_mouse_events(event)

            if event.type == pygame.JOYBUTTONDOWN:
                set_gamepad_button(event)
                gamepad_button_events(event)

              # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                gamepad = pygame.joystick.Joystick(event.device_index)
                joysticks[gamepad.get_instance_id()] = gamepad
                controller_list[gamepad.get_instance_id()] = gamepad
                print(f"{gamepad.get_name()} {gamepad.get_instance_id()} connected")

            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")

            # if event.type == pygame.JOYBUTTONUP:
            #   gamepad_button_events(event)

            if event.type == pygame.JOYAXISMOTION and event.axis == 5 and event.value == 1 or event.type == pygame.JOYAXISMOTION and event.axis == 2 and event.value == 1:
                set_gamepad_button(event)
            if event.type == pygame.JOYHATMOTION:
                # get_axis(event)
                set_gamepad_button(event)

            GUI.manager.process_events(event)

        update_hud()
        GUI.manager.update(time_delta)
        GUI.manager.draw_ui(GUI.window_surface)
        pygame.display.update()


def __init__():
    global isRunning
    global clock
    clock = pygame.time.Clock()
    GUI.draw_ui()


if __name__ == "__main__":
    __init__()
    __main__()
