#!/bin/python3

import pygame
import pygame_gui
import os
import os.path
import subprocess
import sys
import GUI
from playsound import playsound
from os import path
from devices import MIN_TDP,STEP_ONE,STEP_TWO,MAX_TDP,QUIET_FAN_CONFIG,BALANCED_FAN_CONFIG,PERF_FAN_CONFIG

# Define variables

RYZENADJ='/usr/bin/ryzenadj'
HHFC='hhfc -c'
FAN_PROFILE_DIR="/usr/share/temperamental/profiles/"
PARAMS=''
GUI.currentTDP = int(MIN_TDP) // 1000

# Grab current values before changes
DEFAULT_SMT = subprocess.getoutput('cat /sys/devices/system/cpu/smt/control')
DEFAULT_BOOST = subprocess.getoutput('cat /sys/devices/system/cpu/cpufreq/boost')
subprocess.run(RYZENADJ + ' ' + '-i', shell=True)
   
def get_profile():
   print("Grab profiles")
   
def set_tdp_values(button_number):
    global TARGET_TDP
    
    match button_number:
    
       case 0:
          TARGET_TDP = MIN_TDP
          GUI.currentTDP = int(MIN_TDP) // 1000
          GUI.CURRENT_TDP_VALUE.set_text("Current TDP Value:" + " " + str(int(MIN_TDP) // 1000) +"W TDP")
          
       case 1:
          TARGET_TDP = STEP_ONE
          GUI.currentTDP = int(STEP_ONE) // 1000
          GUI.CURRENT_TDP_VALUE.set_text("Current TDP Value:" + " " + str(int(STEP_ONE) // 1000) +"W TDP")
        
       case 2:
          TARGET_TDP = STEP_TWO
          GUI.currentTDP = int(STEP_ONE) // 1000
          GUI.CURRENT_TDP_VALUE.set_text("Current TDP Value:" + " " + str(int(STEP_ONE) // 1000) +"W TDP")
       case 3:
          TARGET_TDP = MAX_TDP
          GUI.currentTDP = int(MAX_TDP) // 1000
          GUI.CURRENT_TDP_VALUE.set_text("Current TDP Value:" + " " + str(int(MAX_TDP) // 1000) +"W TDP")

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
       GUI.CURRENT_TDP_VALUE.set_text("Current TDP Target:" + " " + str(GUI.currentTDP) + "W")
       if GUI.SMT == "on":
          GUI.SMT_LABEL.set_text("SMT Enabled")
       else:
          GUI.SMT_LABEL.set_text("SMT Disabled")
       if GUI.BOOST == '1':
          GUI.BOOST_LABEL.set_text("Boost Enabled")
       else:
          GUI.BOOST_LABEL.set_text("Boost Disabled")
          
def gamepad_button_events(event):

   print("running gamepad events")
   print(event)
   if event.button == 0:
      GUI.currentTDP = int(MIN_TDP) // 1000
   if event.button == 1:
      sys.exit(0)
   if event.button == 2:
      GUI.currentTDP = int(STEP_ONE) // 1000
   if event.button == 3:
      GUI.currentTDP = int(MAX_TDP) // 1000
   if event.button == 4:
      print("Toggle Boost")
   if event.button == 5:
      print("Toggle SMT")
   if event.button == 13:
      GUI.currentTDP = GUI.currentTDP + 1
   if event.button == 14:
      GUI.currentTDP = GUI.currentTDP - 1
      print(event)
      
def get_axis(event):
    hats = gamepad.get_numhats()

    for i in range(hats):
     hat = gamepad.get_hat(i)

    if gamepad.get_hat(i) == (1,0):
       GUI.currentTDP = GUI.currentTDP + 1
       print("right d pad")
    if gamepad.get_hat(i) == (-1,0):
       GUI.currentTDP = GUI.currentTDP - 1
       print("left d pad") 

def keyboard_mouse_events(event):

    if event.ui_element == GUI.SMT_BUTTON:
       if subprocess.getoutput('cat /sys/devices/system/cpu/smt/control') == 'on':
          SMT = 'off'
       else:
          SMT = 'on'
       subprocess.run('/usr/bin/echo ' + SMT + ' > /sys/devices/system/cpu/smt/control', shell=True)
            
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
       PARAMS="--stapm-limit=" + str(GUI.currentTDP * 1000) + " " + "--fast-limit=" + str(GUI.currentTDP * 1000) + " " + " --slow-limit=" + str(GUI.currentTDP * 1000) + " " + " --tctl-temp=90"
       
    if event.ui_element == GUI.NEGATIVE_INCREMENT_BUTTON and GUI.currentTDP != int(MIN_TDP) // 1000:
       GUI.currentTDP = GUI.currentTDP - 1
       PARAMS="--stapm-limit=" + str(GUI.currentTDP * 1000) + " " + "--fast-limit=" + str(GUI.currentTDP * 1000) + " " + " --slow-limit=" + str(GUI.currentTDP * 1000) + " " + " --tctl-temp=90"
       
    if event.ui_element == GUI.APPLY_CHANGES:
       print("Writing" + " " + TARGET_TDP + " " + "with Ryzenadj")
       subprocess.run(RYZENADJ + ' ' + "--stapm-limit=" + TARGET_TDP + " " + "--fast-limit=" + TARGET_TDP + " " + "--slow-limit=" + TARGET_TDP + " " + "--tctl-temp=90", shell=True)  

def __main__():

   global gamepad

   joysticks = {}
   pygame.init()
   isRunning = True

   while isRunning:
   
       time_delta = clock.tick(60)/1000.0
       GUI.window_surface.blit(GUI.background,(0,0))
       GUI.window_surface.fill((0,10,25))
       check_depends()
       
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               isRunning = False
    
           if event.type == pygame.USEREVENT:
           
               if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                   playsound("assets/sfx/click.mp3")
                   keyboard_mouse_events(event)

           if event.type == pygame.JOYBUTTONDOWN:
              print(event)
              gamepad_button_events(event)

            # Handle hotplugging
           if event.type == pygame.JOYDEVICEADDED:

               gamepad = pygame.joystick.Joystick(event.device_index)
               joysticks[gamepad.get_instance_id()] = gamepad
               print(f"Joystick {gamepad.get_instance_id()} connencted")

           if event.type == pygame.JOYDEVICEREMOVED:
               del joysticks[event.instance_id]
               print(f"Joystick {event.instance_id} disconnected")
               
          # if event.type == pygame.JOYBUTTONUP:
           #   gamepad_button_events(event)
           
           if event.type == pygame.JOYAXISMOTION:
              get_axis(event)
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
