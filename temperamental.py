#!/bin/python3

import pygame
import pygame_gui
import os
import subprocess

# Define variables

currentTDP = 0
targetTDP = 0
defaultTDP = 0
SMT = ''
DEFAULT_SMT = subprocess.getoutput('cat /sys/devices/system/cpu/smt/control')
SMT_TOGGLE = False
BOOST = ''
DEFAULT_BOOST = subprocess.getoutput('cat /sys/devices/system/cpu/cpufreq/boost')
BOOST_TOGGLE = False

# Grab current stats

if subprocess.getoutput('cat /sys/devices/system/cpu/smt/control') == 'on':
   SMT = "SMT Enabled"
else:
   SMT = "SMT Disabled"
if subprocess.getoutput('cat /sys/devices/system/cpu/cpufreq/boost') == '1':
   BOOST = "Boost Enabled"
else:
   BOOST = "Boost Disabled"
   
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
                            relative_rect=pygame.Rect(50,50,100,100),
                            text='5w TDP',
                            manager=manager
                        )
button2 = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(50,150,100,100),
                            text='10w TDP',
                            manager=manager
                        )
button3 = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(50,250,100,100),
                            text='15w TDP',
                            manager=manager
                        )
button4 = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(50,350,100,100),
                            text='25w TDP',
                            manager=manager
                        )
button5 = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(300,250,175,30),
                            text='Restore Defaults',
                            manager=manager
                        )
button6 = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(300,450,175,30),
                            text='Toggle SMT',
                            manager=manager
                        )
button7 = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(300,350,175,30),
                            text='Toggle CPU Boost',
                            manager=manager
                        )
# HUD information
label1 = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(0,-25,200,100),
                            text="Set TDP Value",
                            manager=manager
)
label2 = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(475,-25,200,100),
                            text="Current TDP Value",
                            manager=manager
)
label3 = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(150,-25,200,100),
                            text=BOOST,
                            manager=manager
)
label4 = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(325,-25,200,100),
                            text=SMT,
                            manager=manager
)


isRunning = True
clock = pygame.time.Clock()

while isRunning:

    time_delta = clock.tick(60)/1000.0
    window_surface.blit(background,(0,0))
    window_surface.fill((25,20,100))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
            
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            
                if event.ui_element == button6:
                    SMT_TOGGLE = not SMT_TOGGLE
                    if SMT_TOGGLE == True:
                       SMT = 'on'
                    else:
                       SMT = 'off'
                    subprocess.run('/usr/bin/echo ' + SMT + ' > /sys/devices/system/cpu/smt/control', shell=True)
                    
                if event.ui_element == button7:
                    BOOST_TOGGLE = not BOOST_TOGGLE
                    if BOOST_TOGGLE == True:
                       BOOST = '1'
                    else:
                       BOOST = '0'
                    subprocess.run('/usr/bin/echo ' +  BOOST + ' > /sys/devices/system/cpu/cpufreq/boost', shell=True)
                    
                if event.ui_element == button5:
                   subprocess.run('/usr/bin/echo ' +  DEFAULT_BOOST + ' > /sys/devices/system/cpu/cpufreq/boost', shell=True)
                   subprocess.run('/usr/bin/echo ' +  DEFAULT_SMT + ' > /sys/devices/system/cpu/smt/control', shell=True)
                   
        if SMT == 'on':
           label4.set_text("SMT Enabled")
        else:
           label4.set_text("SMT Disabled")
        if BOOST == '1':
           label3.set_text("Boost Enabled")
        else:
           label3.set_text("Boost Disabled")
                   
    # Gamepad inputs are yet to be implemented

        if event.type == pygame.JOYBUTTONDOWN:
            print(event)
        if event.type == pygame.JOYBUTTONUP:
            print(event)
    
        manager.process_events(event)
    
    manager.update(time_delta)
    manager.draw_ui(window_surface)
    pygame.display.update()     

