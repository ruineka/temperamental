#!/bin/python3
import pygame
import pygame_gui
import os
import subprocess
import os.path
import sys

from profile import MIN_TDP,STEP_ONE,STEP_TWO,MAX_TDP

SMT = subprocess.getoutput('cat /sys/devices/system/cpu/smt/control')
BOOST = subprocess.getoutput('cat /sys/devices/system/cpu/cpufreq/boost')

currentTDP = 0
targetTDP = 0
defaultTDP = 0

# Gui Elements
pygame.init()

pygame.display.set_caption('Temperamental TDP Control')
window_surface = pygame.display.set_mode((800,600))
background = pygame.Surface((800,600))

manager = pygame_gui.UIManager((800,600))

# Buttons
MIN_BUTTON = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(0,150,100,50),
                            text=str(int(MIN_TDP) // 1000) + "W TDP",
                            manager=manager
                        )
TIER1_BUTTON = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(100,150,100,50),
                            text=str(int(STEP_ONE) // 1000) + "W TDP",
                            manager=manager
                        )
TIER2_BUTTON = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(200,150,100,50),
                            text=str(int(STEP_TWO) // 1000) + "W TDP",
                            manager=manager
                        )
MAX_BUTTON = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(300,150,100,50),
                            text=str(int(MAX_TDP) // 1000) + "W TDP",
                            manager=manager
                        )
DEFAULT_BUTTON = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(475,560,175,40),
                            text='Restore Defaults',
                            manager=manager
                        )
SMT_BUTTON = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(0,570,175,30),
                            text='Toggle SMT',
                            manager=manager
                        )
BOOST_BUTTON = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(0,540,175,30),
                            text='Toggle CPU Boost',
                            manager=manager
                        )
PERFORMANCE_BUTTON = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(0,510,175,30),
                            text='Toggle Performance Mode',
                            manager=manager
                        )
POWERSAVER_BUTTON = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(0,480,175,30),
                            text='Toggle Power Saver Mode',
                            manager=manager
                        )
CLOSE_BUTTON = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(405,560,70,40),
                            text='Close',
                            manager=manager
                        )
SAVE_BUTTON = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(335,560,70,40),
                            text='Save',
                            manager=manager
                        )
LOAD_BUTTON = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(250,560,70,40),
                            text='Load',
                            manager=manager
                        )
POSITIVE_INCREMENT_BUTTON = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(0,200,75,40),
                            text='+',
                            manager=manager
                        )
NEGATIVE_INCREMENT_BUTTON = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(75,200,75,40),
                            text='-',
                            manager=manager
                        )
APPLY_CHANGES = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(650,560,150,40),
                            text='Apply Changes',
                            manager=manager
                        )
QUIET_FAN= pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(600,260,175,40),
                            text='Quiet Fan',
                            manager=manager
                        )
BALANCED_FAN = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(600,300,175,40),
                            text='Balanced Fan',
                            manager=manager
                        )
PERFORMANCE_FAN = pygame_gui.elements.UIButton(
                            relative_rect=pygame.Rect(600,340,175,40),
                            text='Performance Fan',
                            manager=manager
                        )
# HUD information
CURRENT_TDP_VALUE = pygame_gui.elements.UITextBox(
                            relative_rect=pygame.Rect(550,500,225,50),
                            html_text="Current TDP Target: ",
                            manager=manager
)
BOOST_LABEL = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(600,150,150,50),
                            text=BOOST,
                            manager=manager
)
SMT_LABEL = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(600,200,150,50),
                            text=SMT,
                            manager=manager
)
POWER_PROFILE_LABEL = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(0,75,225,100),
                            text="Power Profile: Not Enabled",
                            manager=manager
)
FAN_CURVE_LABEL = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(250,75,225,100),
                            text="Fan Curve: Not Implemented",
                            manager=manager
)
HHFC_LABEL = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(600,75,225,100),
                            text="",
                            manager=manager
)
RYZENADJ_STATUS_LABEL = pygame_gui.elements.UILabel(
                            relative_rect=pygame.Rect(450,75,225,100),
                            text="Ryzenadj: Not Found",
                            manager=manager
)
TEXT_FIELD_SUMMARY = pygame_gui.elements.UITextBox(
                            relative_rect=pygame.Rect(0,0,800,100),
                            html_text="System Name: " + subprocess.getoutput('cat /sys/devices/virtual/dmi/id/product_name') + "\n" +"CPU Name: " + subprocess.check_output("lscpu | grep \"Model name\" | cut -d : -f 2 | xargs", shell=True, universal_newlines=True).strip(),
                            manager=manager
)

