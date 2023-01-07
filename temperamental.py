#!/bin/python3

import pygame
import pygame_gui
import os
import os.path
import subprocess
import sys
import GUI
import profile
from os import path
from profile import MIN_TDP,STEP_ONE,STEP_TWO,MAX_TDP

# Define variables

currentTDP = 0
targetTDP = 0
defaultTDP = 0

RYZENADJ='/usr/bin/ryzenadj'
PARAMS=''

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
   GUI.label14.set_text("Ryzenadj: Found")
else:
   GUI.label14.set_text("Ryzenadj: Not Found")
   
if path.exists("/usr/share/handycon.py"):
   print("HandyGCCS Found")
else:
   print("HandyGCCS Not Found")
   
if path.exists("/usr/share/hhfc/"):
   print("HHFC Found")
   GUI.label13.set_text("HHFC: Found")
else:
   print("HHFC Not Found")
   GUI.label13.set_text("HHFC: Not Found")
   
isRunning = True
clock = pygame.time.Clock()
   
while isRunning:

    time_delta = clock.tick(60)/1000.0
    GUI.window_surface.blit(GUI.background,(0,0))
    GUI.window_surface.fill((64,64,64))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
            
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            
                if event.ui_element == GUI.button6:

                    if subprocess.getoutput('cat /sys/devices/system/cpu/smt/control') == 'on':
                       SMT = 'off'
                    else:
                       SMT = 'on'
                    subprocess.run('/usr/bin/echo ' + SMT + ' > /sys/devices/system/cpu/smt/control', shell=True)
            
                if event.ui_element == GUI.button1:
                    PARAMS="--stapm-limit=" + MIN_TDP + " " + "--fast-limit=" + MIN_TDP + " " + " --slow-limit=" + MIN_TDP + " " + " --tctl-temp=90"
                    subprocess.run(RYZENADJ + ' ' + PARAMS, shell=True)
                    GUI.label2.set_text("Current TDP Value:" + " " + str(int(MIN_TDP) // 1000) +"W TDP")
                    
                if event.ui_element == GUI.button2:
                    PARAMS="--stapm-limit=" + STEP_ONE + " " + "--fast-limit=" + STEP_ONE + " " + " --slow-limit=" + STEP_ONE + " " + " --tctl-temp=90"
                    subprocess.run(RYZENADJ + ' ' + PARAMS, shell=True)
                    GUI.label2.set_text("Current TDP Value:" + " " + str(int(STEP_ONE) // 1000) +"W TDP")
                    
                if event.ui_element == GUI.button3:
                    PARAMS="--stapm-limit=" + STEP_TWO + " " + "--fast-limit=" + STEP_TWO + " " + " --slow-limit=" + STEP_TWO + " " + " --tctl-temp=90"
                    subprocess.run(RYZENADJ + ' ' + PARAMS, shell=True)   
                    GUI.label2.set_text("Current TDP Value:" + " " + str(int(STEP_TWO) // 1000) +"W TDP")  
                         
                if event.ui_element == GUI.button4:
                    PARAMS="--stapm-limit=" + MAX_TDP + " " + "--fast-limit=" + MAX_TDP + " " + " --slow-limit=" + MAX_TDP + " " + " --tctl-temp=90"
                    subprocess.run(RYZENADJ + ' ' + PARAMS, shell=True)
                    GUI.label2.set_text("Current TDP Value:" + " " + str(int(MAX_TDP) // 1000) +"W TDP")
                if event.ui_element == GUI.button7:
                    if subprocess.getoutput('cat /sys/devices/system/cpu/cpufreq/boost') == '1':
                       BOOST = '0'
                    else:
                       BOOST = '1'
                    subprocess.run('/usr/bin/echo ' +  BOOST + ' > /sys/devices/system/cpu/cpufreq/boost', shell=True)
                    
                if event.ui_element == GUI.button5:
                   subprocess.run('/usr/bin/echo ' +  DEFAULT_BOOST + ' > /sys/devices/system/cpu/cpufreq/boost', shell=True)
                   subprocess.run('/usr/bin/echo ' +  DEFAULT_SMT + ' > /sys/devices/system/cpu/smt/control', shell=True)
                   
                if event.ui_element == GUI.button8:
                    PARAMS='--max-performance'
                    subprocess.run(RYZENADJ + ' ' + PARAMS, shell=True)
                    GUI.label11.set_text("Power Profile: Performance")
                    
                if event.ui_element == GUI.button9:
                    PARAMS='--power-saving'
                    subprocess.run(RYZENADJ + ' ' + PARAMS, shell=True)
                    GUI.label11.set_text("Power Profile: Power Saver")
                    
                if event.ui_element == GUI.button10:
                    sys.exit(0)
                   
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
