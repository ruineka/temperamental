#!/bin/python3

import pygame
import pygame_gui
import os
import subprocess
import time

# Define variables

currentTDP = 0
targetTDP = 0
defaultTDP = 0

SMT = ''
BOOST = ''

RYZENADJ='/usr/bin/ryzenadj'
PARAMS=''

# Grab current values before changes
DEFAULT_SMT = subprocess.getoutput('cat /sys/devices/system/cpu/smt/control')
DEFAULT_BOOST = subprocess.getoutput('cat /sys/devices/system/cpu/cpufreq/boost')
subprocess.run(RYZENADJ + ' ' + '-i', shell=True)
   
pygame.init()

pygame.display.set_caption('Temperamental TDP Control')
window_surface = pygame.display.set_mode((800,600))
background = pygame.Surface((800,600))

# gamepad init

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
    print(joystick.get_name() + " connected!")


# Gui Elements

manager = pygame_gui.UIManager((800,600))

# Buttons
button1 = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(0,200,100,100),
                            text='5W TDP',
                            manager=manager
                        )
button2 = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(0,300,100,100),
                            text='10W TDP',
                            manager=manager
                        )
button3 = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(0,400,100,100),
                            text='15W TDP',
                            manager=manager
                        )
button4 = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(0,500,100,100),
                            text='25W TDP',
                            manager=manager
                        )
button5 = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(100,510,175,30),
                            text='Restore Defaults',
                            manager=manager
                        )
button6 = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(100,570,175,30),
                            text='Toggle SMT',
                            manager=manager
                        )
button7 = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(100,540,175,30),
                            text='Toggle CPU Boost',
                            manager=manager
                        )
button8 = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(550,250,175,30),
                            text='Toggle Performance Mode',
                            manager=manager
                        )
button9 = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(550,200,175,30),
                            text='Toggle Power Saver Mode',
                            manager=manager
                        )
# HUD information
label1 = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(100,350,200,100),
                            text="Current Power Draw",
                            manager=manager
)
label2 = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(100,375,200,100),
                            text="Current TDP Value",
                            manager=manager
)
label3 = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(100,400,200,100),
                            text=BOOST,
                            manager=manager
)
label4 = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(100,425,200,100),
                            text=SMT,
                            manager=manager
)
label5 = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(-50,0,200,100),
                            text="CPU Name",
                            manager=manager
)
label6 = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(-50,25,200,100),
                            text="GPU Name",
                            manager=manager
)
label7 = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(-47,50,200,100),
                            text="CPU Cores",
                            manager=manager
)
label8 = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(-30,75,200,100),
                            text="CPU Frequency",
                            manager=manager
)
label9 = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(-30,100,200,100),
                            text="GPU Frequency",
                            manager=manager
)
label10 = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(-46,125,200,100),
                            text="Fan Speed",
                            manager=manager
)
label11 = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(550,0,225,100),
                            text="Power Profile: Performance",
                            manager=manager
)
label12 = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(514,25,225,100),
                            text="Fan Curve: Custom",
                            manager=manager
)
label13 = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(527,50,225,100),
                            text="HHFC Status: Enabled",
                            manager=manager
)
label14 = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(523,75,225,100),
                            text="Ryzenadj: Not Found",
                            manager=manager
)
label15 = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(225,-25,350,100),
                            text="System Name: " + subprocess.getoutput('cat /sys/devices/virtual/dmi/id/product_name'),
                            manager=manager
)
textbox1 = pygame_gui.elements.UITextBox(
                            relative_rect=pygame.Rect(350,400,350,200),
                            html_text=subprocess.getoutput(RYZENADJ + ' ' + '-i'),
                            manager=manager
)


isRunning = True
clock = pygame.time.Clock()

while isRunning:

    time_delta = clock.tick(60)/1000.0
    window_surface.blit(background,(0,0))
    window_surface.fill((64,64,64))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
            
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            
                if event.ui_element == button6:

                    if subprocess.getoutput('cat /sys/devices/system/cpu/smt/control') == 'on':
                       SMT = 'off'
                    else:
                       SMT = 'on'
                    subprocess.run('/usr/bin/echo ' + SMT + ' > /sys/devices/system/cpu/smt/control', shell=True)
            
                if event.ui_element == button1:
                    PARAMS='--stapm-limit=5000 --fast-limit=5000 --slow-limit=5000 --tctl-temp=90'
                    subprocess.run(RYZENADJ + ' ' + PARAMS, shell=True)
                    
                if event.ui_element == button2:
                    PARAMS='--stapm-limit=10000 --fast-limit=10000 --slow-limit=10000 --tctl-temp=90'
                    subprocess.run(RYZENADJ + ' ' + PARAMS, shell=True)
                    
                if event.ui_element == button3:
                    PARAMS='--stapm-limit=15000 --fast-limit=15000 --slow-limit=15000 --tctl-temp=90'
                    subprocess.run(RYZENADJ + ' ' + PARAMS, shell=True)     
                         
                if event.ui_element == button4:
                   print("For safety reasons 25W target is disabled in code for now")
                    #PARAMS='--stapm-limit=25000 --fast-limit=25000 --slow-limit=25000 --tctl-temp=90'
                    #subprocess.run(RYZENADJ + ' ' + PARAMS, shell=True)
                    
                if event.ui_element == button7:
                    if subprocess.getoutput('cat /sys/devices/system/cpu/cpufreq/boost') == '1':
                       BOOST = '0'
                    else:
                       BOOST = '1'
                    subprocess.run('/usr/bin/echo ' +  BOOST + ' > /sys/devices/system/cpu/cpufreq/boost', shell=True)
                    
                if event.ui_element == button5:
                   subprocess.run('/usr/bin/echo ' +  DEFAULT_BOOST + ' > /sys/devices/system/cpu/cpufreq/boost', shell=True)
                   subprocess.run('/usr/bin/echo ' +  DEFAULT_SMT + ' > /sys/devices/system/cpu/smt/control', shell=True)
                   
                if event.ui_element == button8:
                    PARAMS='--max-performance'
                    subprocess.run(RYZENADJ + ' ' + PARAMS, shell=True)
                    
                if event.ui_element == button9:
                    PARAMS='--power-saving'
                    subprocess.run(RYZENADJ + ' ' + PARAMS, shell=True)
                   
        # Update Hud Values       
        if subprocess.getoutput('cat /sys/devices/system/cpu/smt/control') == 'on':
           label4.set_text("SMT Enabled")
        else:
           label4.set_text("SMT Disabled")
        if subprocess.getoutput('cat /sys/devices/system/cpu/cpufreq/boost') == '1':
           label3.set_text("Boost Enabled")
        else:
           label3.set_text("Boost Disabled")
                   
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
    
        manager.process_events(event)
    
    manager.update(time_delta)
    manager.draw_ui(window_surface)
    pygame.display.update()     

