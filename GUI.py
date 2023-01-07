#!/bin/python3
import pygame
import pygame_gui
import os
import subprocess
import os.path
import sys

from profile import MIN_TDP,STEP_ONE,STEP_TWO,MAX_TDP

SMT = ''
BOOST = ''

# Gui Elements
pygame.init()

pygame.display.set_caption('Temperamental TDP Control')
window_surface = pygame.display.set_mode((800,600))
background = pygame.Surface((800,600))

manager = pygame_gui.UIManager((800,600))

# Buttons
button1 = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(0,200,100,100),
                            text=str(int(MIN_TDP) // 1000) + "W TDP",
                            manager=manager
                        )
button2 = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(0,300,100,100),
                            text=str(int(STEP_ONE) // 1000) + "W TDP",
                            manager=manager
                        )
button3 = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(0,400,100,100),
                            text=str(int(STEP_TWO) // 1000) + "W TDP",
                            manager=manager
                        )
button4 = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(0,500,100,100),
                            text=str(int(MAX_TDP) // 1000) + "W TDP",
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
button10 = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(700,5,70,30),
                            text='Close',
                            manager=manager
                        )
# HUD information
label1 = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(100,350,225,100),
                            text="Current Power Draw:" + " " + subprocess.getoutput("awk '{print $1*10^-5 " "}' /sys/class/power_supply/BATT/current_now") + "W",
                            manager=manager
)
label2 = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(100,375,225,100),
                            text="Current TDP Value:" + " " + "Not Set",
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
                            relative_rect=pygame.Rect(14,0,500,100),
                            text="CPU Name: " + subprocess.check_output("lscpu | grep \"Model name\" | cut -d : -f 2 | xargs", shell=True, universal_newlines=True).strip(),
                            manager=manager
)
label11 = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(550,0,225,100),
                            text="Power Profile: Not Enabled",
                            manager=manager
)
label12 = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(514,25,225,100),
                            text="Fan Curve: Not Implemented",
                            manager=manager
)
label13 = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(527,50,225,100),
                            text="",
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
                            relative_rect=pygame.Rect(350,400,425,200),
                            html_text="Use this tool at your own risk, I don't take responsiblity for any issues caused by this tool",
                            manager=manager
)

        # Update Hud Values       
label1.set_text("Current Power Draw" + " " + subprocess.getoutput("awk '{print $1*10^-5 " "}' /sys/class/power_supply/BATT/current_now") + "W")
        
if subprocess.getoutput('cat /sys/devices/system/cpu/smt/control') == 'on':
   label4.set_text("SMT Enabled")
else:
   label4.set_text("SMT Disabled")
if subprocess.getoutput('cat /sys/devices/system/cpu/cpufreq/boost') == '1':
   label3.set_text("Boost Enabled")
else:
   label3.set_text("Boost Disabled")
