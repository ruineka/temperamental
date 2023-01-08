#!/bin/python3

import pygame
import pygame_gui
import os
import os.path
import subprocess
import sys
import GUI
import profile
import vlc
import time
from os import path
from profile import MIN_TDP,STEP_ONE,STEP_TWO,MAX_TDP

# Define variables

RYZENADJ='/usr/bin/ryzenadj'
PARAMS=''
GUI.currentTDP = int(MIN_TDP) // 1000

# Grab current values before changes
DEFAULT_SMT = subprocess.getoutput('cat /sys/devices/system/cpu/smt/control')
DEFAULT_BOOST = subprocess.getoutput('cat /sys/devices/system/cpu/cpufreq/boost')
subprocess.run(RYZENADJ + ' ' + '-i', shell=True)

# gamepad init

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
    print(joystick.get_name() + " connected!")

# Check for dependencies
if path.exists("/usr/bin/ryzenadj"):
   print("Ryzenadj Found")
   GUI.RYZENADJ_STATUS_LABEL.set_text("Ryzenadj: Found")
else:
   GUI.RYZENADJ_STATUS_LABEL.set_text("Ryzenadj: Not Found")
   
if path.exists("/usr/share/handycon.py"):
   print("HandyGCCS Found")
else:
   print("HandyGCCS Not Found")
   
if path.exists("/usr/share/hhfc/"):
   print("HHFC Found")
   GUI.HHFC_LABEL.set_text("HHFC: Found")
else:
   print("HHFC Not Found")
   GUI.HHFC_LABEL.set_text("HHFC: Not Found")
   
isRunning = True
clock = pygame.time.Clock()
   
while isRunning:

    time_delta = clock.tick(60)/1000.0
    GUI.window_surface.blit(GUI.background,(0,0))
    GUI.window_surface.fill((0,10,25))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
            
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            
                if event.ui_element == GUI.SMT_BUTTON:

                    if subprocess.getoutput('cat /sys/devices/system/cpu/smt/control') == 'on':
                       SMT = 'off'
                    else:
                       SMT = 'on'
                    subprocess.run('/usr/bin/echo ' + SMT + ' > /sys/devices/system/cpu/smt/control', shell=True)
            
                if event.ui_element == GUI.MIN_BUTTON:
                    PARAMS="--stapm-limit=" + MIN_TDP + " " + "--fast-limit=" + MIN_TDP + " " + "--slow-limit=" + MIN_TDP + " " + "--tctl-temp=90"
                    GUI.currentTDP = int(MIN_TDP) // 1000
                    GUI.CURRENT_TDP_VALUE.set_text("Current TDP Value:" + " " + str(int(MIN_TDP) // 1000) +"W TDP")
                    
                if event.ui_element == GUI.TIER1_BUTTON:
                    PARAMS="--stapm-limit=" + STEP_ONE + " " + "--fast-limit=" + STEP_ONE + " " + "--slow-limit=" + STEP_ONE + " " + "--tctl-temp=90"
                    GUI.currentTDP = int(STEP_ONE) // 1000
                    GUI.CURRENT_TDP_VALUE.set_text("Current TDP Value:" + " " + str(int(STEP_ONE) // 1000) +"W TDP")
                    
                if event.ui_element == GUI.TIER2_BUTTON:
                    PARAMS="--stapm-limit=" + STEP_TWO + " " + "--fast-limit=" + STEP_TWO + " " + "--slow-limit=" + STEP_TWO + " " + "--tctl-temp=90"
                    GUI.currentTDP = int(STEP_TWO) // 1000
                    GUI.CURRENT_TDP_VALUE.set_text("Current TDP Value:" + " " + str(int(STEP_TWO) // 1000) +"W TDP")  
                         
                if event.ui_element == GUI.MAX_BUTTON:
                    PARAMS="--stapm-limit=" + MAX_TDP + " " + "--fast-limit=" + MAX_TDP + " " + "--slow-limit=" + MAX_TDP + " " + "--tctl-temp=90"
                    GUI.currentTDP = int(MAX_TDP) // 1000
                    GUI.CURRENT_TDP_VALUE.set_text("Current TDP Value:" + " " + str(int(MAX_TDP) // 1000) +"W TDP")
                if event.ui_element == GUI.BOOST_BUTTON:
                    if subprocess.getoutput('cat /sys/devices/system/cpu/cpufreq/boost') == '1':
                       BOOST = '0'
                    else:
                       BOOST = '1'
                    subprocess.run('/usr/bin/echo ' +  BOOST + ' > /sys/devices/system/cpu/cpufreq/boost', shell=True)
                    
                if event.ui_element == GUI.DEFAULT_BUTTON:
                   subprocess.run('/usr/bin/echo ' +  DEFAULT_BOOST + ' > /sys/devices/system/cpu/cpufreq/boost', shell=True)
                   subprocess.run('/usr/bin/echo ' +  DEFAULT_SMT + ' > /sys/devices/system/cpu/smt/control', shell=True)
                   
                if event.ui_element == GUI.PERFORMANCE_BUTTON:
                    PARAMS='--max-performance'
                    subprocess.run(RYZENADJ + ' ' + PARAMS, shell=True)
                    GUI.POWER_PROFILE_LABEL.set_text("Power Profile: Performance")
                    
                if event.ui_element == GUI.POWERSAVER_BUTTON:
                    PARAMS='--power-saving'
                    subprocess.run(RYZENADJ + ' ' + PARAMS, shell=True)
                    GUI.POWER_PROFILE_LABEL.set_text("Power Profile: Power Saver")
                    
                if event.ui_element == GUI.CLOSE_BUTTON:
                    sys.exit(0)
                if event.ui_element == GUI.POSITIVE_INCREMENT_BUTTON and GUI.currentTDP != int(MAX_TDP) // 1000:
                    GUI.currentTDP = GUI.currentTDP + 1
                    PARAMS="--stapm-limit=" + str(GUI.currentTDP * 1000) + " " + "--fast-limit=" + str(GUI.currentTDP * 1000) + " " + " --slow-limit=" + str(GUI.currentTDP * 1000) + " " + " --tctl-temp=90"
                if event.ui_element == GUI.NEGATIVE_INCREMENT_BUTTON and GUI.currentTDP != int(MIN_TDP) // 1000:
                    GUI.currentTDP = GUI.currentTDP - 1
                    PARAMS="--stapm-limit=" + str(GUI.currentTDP * 1000) + " " + "--fast-limit=" + str(GUI.currentTDP * 1000) + " " + " --slow-limit=" + str(GUI.currentTDP * 1000) + " " + " --tctl-temp=90"
                if event.ui_element == GUI.APPLY_CHANGES:
                   print(RYZENADJ + " " + PARAMS)
                   subprocess.run(RYZENADJ + ' ' + PARAMS, shell=True)
                    
# Update Hud Values   
        if GUI.currentTDP != 0:
           GUI.CURRENT_TDP_VALUE.set_text("Current TDP Target:" + " " + str(GUI.currentTDP) + "W")
        
        if GUI.SMT == "on":
           GUI.SMT_LABEL.set_text("SMT Enabled")
        else:
           GUI.SMT_LABEL.set_text("SMT Disabled")
        if GUI.BOOST == '1':
           GUI.BOOST_LABEL.set_text("Boost Enabled")
        else:
           GUI.BOOST_LABEL.set_text("Boost Disabled")
                   
    # Gamepad inputs are yet to be implemented
        if event.type == pygame.JOYBUTTONDOWN:
           if event.button == 0:
              print("Set TDP to 5W")
           if event.button == 1:
              print("Set TDP to 10W")
           if event.button == 2:
              print("Set TDP to 15W")
           if event.button == 3:
              print("Set TDP to MAX")
           if event.button == 4:
              print("Toggle Boost")
           if event.button == 5:
              print("Toggle SMT")
           print(event)
        if event.type == pygame.JOYBUTTONUP:
            print(event)
    
        GUI.manager.process_events(event)
    
    GUI.manager.update(time_delta)
    GUI.manager.draw_ui(GUI.window_surface)
    pygame.display.update()
