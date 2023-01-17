#!/bin/python3
import pygame
import pygame_gui
import subprocess
import sys

from devices import MIN_TDP, STEP_ONE, STEP_TWO, MAX_TDP, SYSTEM_NAME

SMT = subprocess.getoutput('cat /sys/devices/system/cpu/smt/control')
BOOST = subprocess.getoutput('cat /sys/devices/system/cpu/cpufreq/boost')

currentTDP = 0
targetTDP = 0
defaultTDP = 0

currentFanCurve = ""

# Gui Elements
pygame.init()

pygame.display.set_caption('Temperamental TDP Control')
window_surface = pygame.display.set_mode((1280, 800))
background = pygame.Surface((1280, 800))
img = pygame.image.load('usr/lib/temperamental/assets/images/icon.png')
pygame.display.set_icon(img)

manager = pygame_gui.UIManager((1280, 800))

try:
    system_name = sys.argv[1]
except:
    if SYSTEM_NAME != "":
        system_name = SYSTEM_NAME
    else:
        system_name = "DEFAULT"


def draw_ui():
    # Define UI Variables
    global MIN_BUTTON
    global TIER1_BUTTON
    global TIER2_BUTTON
    global MAX_BUTTON
    global DEFAULT_BUTTON
    global SMT_BUTTON
    global BOOST_BUTTON
    global PERFORMANCE_BUTTON
    global POWERSAVER_BUTTON
    global CLOSE_BUTTON
    global SAVE_BUTTON
    global LOAD_BUTTON
    global POSITIVE_INCREMENT_BUTTON
    global NEGATIVE_INCREMENT_BUTTON
    global APPLY_CHANGES
    global QUIET_FAN
    global BALANCED_FAN
    global PERFORMANCE_FAN
    global CURRENT_TDP_VALUE
    global BOOST_LABEL
    global SMT_LABEL
    global POWER_PROFILE_LABEL
    global FAN_CURVE_LABEL
    global HHFC_LABEL
    global RYZENADJ_STATUS_LABEL
    global TEXT_FIELD_SUMMARY
    global IMAGE_1

    match system_name:
        case "ONE XPLAYER":
            MIN_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 382, 100, 25),
                text=str(int(MIN_TDP) // 1000) + "W TDP",
                manager=manager
            )
            TIER1_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 355, 100, 25),
                text=str(int(STEP_ONE) // 1000) + "W TDP",
                manager=manager
            )
            TIER2_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 328, 100, 25),
                text=str(int(STEP_TWO) // 1000) + "W TDP",
                manager=manager
            )
            MAX_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 410, 100, 25),
                text=str(int(MAX_TDP) // 1000) + "W TDP",
                manager=manager
            )
            DEFAULT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(460, 508, 350, 50),
                text='Restore Defaults',
                manager=manager
            )
            SMT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(820, 250, 175, 30),
                text='Toggle SMT',
                manager=manager
            )
            BOOST_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(275, 250, 175, 30),
                text='Toggle CPU Boost',
                manager=manager
            )
            PERFORMANCE_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(455, 242, 175, 30),
                text='Toggle Performance Mode',
                manager=manager
            )
            POWERSAVER_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(640, 242, 175, 30),
                text='Toggle Power Saver Mode',
                manager=manager
            )
            CLOSE_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(308, 312, 75, 40),
                text='Close',
                manager=manager
            )
            SAVE_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 440, 150, 40),
                text='Save',
                manager=manager
            )
            LOAD_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(308, 352, 75, 40),
                text='Load',
                manager=manager
            )
            POSITIVE_INCREMENT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(308, 435, 75, 25),
                text='+',
                manager=manager
            )
            NEGATIVE_INCREMENT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(308, 408, 75, 25),
                text='-',
                manager=manager
            )
            APPLY_CHANGES = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 290, 150, 30),
                text='Apply Changes',
                manager=manager
            )
            QUIET_FAN = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(1100, 260, 175, 40),
                text='Quiet Fan',
                manager=manager
            )
            BALANCED_FAN = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(1100, 300, 175, 40),
                text='Balanced Fan',
                manager=manager
            )
            PERFORMANCE_FAN = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(1100, 340, 175, 40),
                text='Performance Fan',
                manager=manager
            )
            # HUD information
            CURRENT_TDP_VALUE = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect(525, 185, 225, 50),
                html_text="Current TDP Target: ",
                manager=manager
            )
            BOOST_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(850, 100, 150, 50),
                text=BOOST,
                manager=manager
            )
            SMT_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(1050, 100, 150, 50),
                text=SMT,
                manager=manager
            )
            POWER_PROFILE_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(0, 75, 225, 100),
                text="Power Profile: Not Enabled",
                manager=manager
            )
            FAN_CURVE_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(250, 75, 225, 100),
                text="Fan Curve: Not Set",
                manager=manager
            )
            HHFC_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(600, 75, 225, 100),
                text="",
                manager=manager
            )
            RYZENADJ_STATUS_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(450, 75, 225, 100),
                text="",
                manager=manager
            )
            TEXT_FIELD_SUMMARY = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect(0, 0, 1280, 100),
                html_text="System Name: " + system_name + "\n" + "CPU Name: " + subprocess.check_output(
                    "lscpu | grep \"Model name\" | cut -d : -f 2 | xargs", shell=True, universal_newlines=True).strip(),
                manager=manager
            )
            IMAGE_1 = pygame_gui.elements.UIImage(
                relative_rect=pygame.Rect(375, 250, 525, 325),
                image_surface=pygame.image.load(
                    'usr/lib/temperamental/assets/images/oxp-ctr.png').convert_alpha(),
                manager=manager
            )

        case "AYA NEO":
            MIN_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(400, 250, 100, 25),
                text=str(int(MIN_TDP) // 1000) + "W TDP",
                manager=manager
            )
            TIER1_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(300, 270, 100, 25),
                text=str(int(STEP_ONE) // 1000) + "W TDP",
                manager=manager
            )
            TIER2_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(770, 250, 100, 25),
                text=str(int(STEP_TWO) // 1000) + "W TDP",
                manager=manager
            )
            MAX_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(900, 275, 100, 25),
                text=str(int(MAX_TDP) // 1000) + "W TDP",
                manager=manager
            )
            DEFAULT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(475, 760, 175, 40),
                text='Restore Defaults',
                manager=manager
            )
            SMT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(0, 770, 175, 30),
                text='Toggle SMT',
                manager=manager
            )
            BOOST_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(0, 740, 175, 30),
                text='Toggle CPU Boost',
                manager=manager
            )
            PERFORMANCE_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(0, 710, 175, 30),
                text='Toggle Performance Mode',
                manager=manager
            )
            POWERSAVER_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(0, 680, 175, 30),
                text='Toggle Power Saver Mode',
                manager=manager
            )
            CLOSE_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(900, 360, 70, 25),
                text='Close',
                manager=manager
            )
            SAVE_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(335, 760, 70, 40),
                text='Save',
                manager=manager
            )
            LOAD_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(250, 760, 70, 40),
                text='Load',
                manager=manager
            )
            POSITIVE_INCREMENT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(325, 495, 75, 25),
                text='+',
                manager=manager
            )
            NEGATIVE_INCREMENT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(300, 420, 75, 25),
                text='-',
                manager=manager
            )
            APPLY_CHANGES = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(900, 390, 150, 25),
                text='Apply Changes',
                manager=manager
            )
            QUIET_FAN = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(1100, 260, 175, 40),
                text='Quiet Fan',
                manager=manager
            )
            BALANCED_FAN = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(1100, 300, 175, 40),
                text='Balanced Fan',
                manager=manager
            )
            PERFORMANCE_FAN = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(1100, 340, 175, 40),
                text='Performance Fan',
                manager=manager
            )
            # HUD information
            CURRENT_TDP_VALUE = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect(525, 200, 225, 50),
                html_text="Current TDP Target: ",
                manager=manager
            )
            BOOST_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(1100, 150, 150, 50),
                text=BOOST,
                manager=manager
            )
            SMT_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(1100, 200, 150, 50),
                text=SMT,
                manager=manager
            )
            POWER_PROFILE_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(0, 75, 225, 100),
                text="Power Profile: Not Enabled",
                manager=manager
            )
            FAN_CURVE_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(250, 75, 225, 100),
                text="Fan Curve: Not Set",
                manager=manager
            )
            HHFC_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(600, 75, 225, 100),
                text="",
                manager=manager
            )
            RYZENADJ_STATUS_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(450, 75, 225, 100),
                text="",
                manager=manager
            )
            TEXT_FIELD_SUMMARY = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect(0, 0, 1280, 100),
                html_text="System Name: " + system_name + "\n" + "CPU Name: " + subprocess.check_output(
                    "lscpu | grep \"Model name\" | cut -d : -f 2 | xargs", shell=True, universal_newlines=True).strip(),
                manager=manager
            )
            IMAGE_1 = pygame_gui.elements.UIImage(
                relative_rect=pygame.Rect(375, 250, 525, 325),
                image_surface=pygame.image.load(
                    'usr/lib/temperamental/assets/images/aya-neo-ctr.png').convert_alpha(),
                manager=manager
            )
            
        case "AYA NEO AIR":
            MIN_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 382, 100, 25),
                text=str(int(MIN_TDP) // 1000) + "W TDP",
                manager=manager
            )
            TIER1_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 355, 100, 25),
                text=str(int(STEP_ONE) // 1000) + "W TDP",
                manager=manager
            )
            TIER2_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 328, 100, 25),
                text=str(int(STEP_TWO) // 1000) + "W TDP",
                manager=manager
            )
            MAX_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 410, 100, 25),
                text=str(int(MAX_TDP) // 1000) + "W TDP",
                manager=manager
            )
            DEFAULT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(460, 508, 350, 50),
                text='Restore Defaults',
                manager=manager
            )
            SMT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(820, 250, 175, 30),
                text='Toggle SMT',
                manager=manager
            )
            BOOST_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(275, 250, 175, 30),
                text='Toggle CPU Boost',
                manager=manager
            )
            PERFORMANCE_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(455, 242, 175, 30),
                text='Toggle Performance Mode',
                manager=manager
            )
            POWERSAVER_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(640, 242, 175, 30),
                text='Toggle Power Saver Mode',
                manager=manager
            )
            CLOSE_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(308, 312, 75, 40),
                text='Close',
                manager=manager
            )
            SAVE_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 440, 150, 40),
                text='Save',
                manager=manager
            )
            LOAD_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(308, 352, 75, 40),
                text='Load',
                manager=manager
            )
            POSITIVE_INCREMENT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(308, 435, 75, 25),
                text='+',
                manager=manager
            )
            NEGATIVE_INCREMENT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(308, 408, 75, 25),
                text='-',
                manager=manager
            )
            APPLY_CHANGES = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 290, 150, 30),
                text='Apply Changes',
                manager=manager
            )
            QUIET_FAN = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(1100, 260, 175, 40),
                text='Quiet Fan',
                manager=manager
            )
            BALANCED_FAN = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(1100, 300, 175, 40),
                text='Balanced Fan',
                manager=manager
            )
            PERFORMANCE_FAN = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(1100, 340, 175, 40),
                text='Performance Fan',
                manager=manager
            )
            # HUD information
            CURRENT_TDP_VALUE = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect(525, 185, 225, 50),
                html_text="Current TDP Target: ",
                manager=manager
            )
            BOOST_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(850, 100, 150, 50),
                text=BOOST,
                manager=manager
            )
            SMT_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(1050, 100, 150, 50),
                text=SMT,
                manager=manager
            )
            POWER_PROFILE_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(0, 75, 225, 100),
                text="Power Profile: Not Enabled",
                manager=manager
            )
            FAN_CURVE_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(250, 75, 225, 100),
                text="Fan Curve: Not Set",
                manager=manager
            )
            HHFC_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(600, 75, 225, 100),
                text="",
                manager=manager
            )
            RYZENADJ_STATUS_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(450, 75, 225, 100),
                text="",
                manager=manager
            )
            TEXT_FIELD_SUMMARY = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect(0, 0, 1280, 100),
                html_text="System Name: " + system_name + "\n" + "CPU Name: " + subprocess.check_output(
                    "lscpu | grep \"Model name\" | cut -d : -f 2 | xargs", shell=True, universal_newlines=True).strip(),
                manager=manager
            )
            IMAGE_1 = pygame_gui.elements.UIImage(
                relative_rect=pygame.Rect(375, 250, 525, 325),
                image_surface=pygame.image.load(
                    'usr/lib/temperamental/assets/images/aya-neo-air-ctr.png').convert_alpha(),
                manager=manager
            )
            
        case "AYA NEO NEXT":
            MIN_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 382, 100, 25),
                text=str(int(MIN_TDP) // 1000) + "W TDP",
                manager=manager
            )
            TIER1_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 355, 100, 25),
                text=str(int(STEP_ONE) // 1000) + "W TDP",
                manager=manager
            )
            TIER2_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 328, 100, 25),
                text=str(int(STEP_TWO) // 1000) + "W TDP",
                manager=manager
            )
            MAX_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 410, 100, 25),
                text=str(int(MAX_TDP) // 1000) + "W TDP",
                manager=manager
            )
            DEFAULT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(460, 508, 350, 50),
                text='Restore Defaults',
                manager=manager
            )
            SMT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(820, 250, 175, 30),
                text='Toggle SMT',
                manager=manager
            )
            BOOST_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(275, 250, 175, 30),
                text='Toggle CPU Boost',
                manager=manager
            )
            PERFORMANCE_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(455, 242, 175, 30),
                text='Toggle Performance Mode',
                manager=manager
            )
            POWERSAVER_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(640, 242, 175, 30),
                text='Toggle Power Saver Mode',
                manager=manager
            )
            CLOSE_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(308, 312, 75, 40),
                text='Close',
                manager=manager
            )
            SAVE_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 440, 150, 40),
                text='Save',
                manager=manager
            )
            LOAD_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(308, 352, 75, 40),
                text='Load',
                manager=manager
            )
            POSITIVE_INCREMENT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(308, 435, 75, 25),
                text='+',
                manager=manager
            )
            NEGATIVE_INCREMENT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(308, 408, 75, 25),
                text='-',
                manager=manager
            )
            APPLY_CHANGES = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 290, 150, 30),
                text='Apply Changes',
                manager=manager
            )
            QUIET_FAN = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(1100, 260, 175, 40),
                text='Quiet Fan',
                manager=manager
            )
            BALANCED_FAN = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(1100, 300, 175, 40),
                text='Balanced Fan',
                manager=manager
            )
            PERFORMANCE_FAN = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(1100, 340, 175, 40),
                text='Performance Fan',
                manager=manager
            )
            # HUD information
            CURRENT_TDP_VALUE = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect(525, 185, 225, 50),
                html_text="Current TDP Target: ",
                manager=manager
            )
            BOOST_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(850, 100, 150, 50),
                text=BOOST,
                manager=manager
            )
            SMT_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(1050, 100, 150, 50),
                text=SMT,
                manager=manager
            )
            POWER_PROFILE_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(0, 75, 225, 100),
                text="Power Profile: Not Enabled",
                manager=manager
            )
            FAN_CURVE_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(250, 75, 225, 100),
                text="Fan Curve: Not Set",
                manager=manager
            )
            HHFC_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(600, 75, 225, 100),
                text="",
                manager=manager
            )
            RYZENADJ_STATUS_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(450, 75, 225, 100),
                text="",
                manager=manager
            )
            TEXT_FIELD_SUMMARY = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect(0, 0, 1280, 100),
                html_text="System Name: " + system_name + "\n" + "CPU Name: " + subprocess.check_output(
                    "lscpu | grep \"Model name\" | cut -d : -f 2 | xargs", shell=True, universal_newlines=True).strip(),
                manager=manager
            )
            IMAGE_1 = pygame_gui.elements.UIImage(
                relative_rect=pygame.Rect(375, 250, 525, 325),
                image_surface=pygame.image.load(
                    'usr/lib/temperamental/assets/images/aya-neo-next-ctr.png').convert_alpha(),
                manager=manager
            )
            
        case "AYA NEO 2":
            MIN_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 382, 100, 25),
                text=str(int(MIN_TDP) // 1000) + "W TDP",
                manager=manager
            )
            TIER1_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 355, 100, 25),
                text=str(int(STEP_ONE) // 1000) + "W TDP",
                manager=manager
            )
            TIER2_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 328, 100, 25),
                text=str(int(STEP_TWO) // 1000) + "W TDP",
                manager=manager
            )
            MAX_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 410, 100, 25),
                text=str(int(MAX_TDP) // 1000) + "W TDP",
                manager=manager
            )
            DEFAULT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(460, 508, 350, 50),
                text='Restore Defaults',
                manager=manager
            )
            SMT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(820, 250, 175, 30),
                text='Toggle SMT',
                manager=manager
            )
            BOOST_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(275, 250, 175, 30),
                text='Toggle CPU Boost',
                manager=manager
            )
            PERFORMANCE_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(455, 242, 175, 30),
                text='Toggle Performance Mode',
                manager=manager
            )
            POWERSAVER_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(640, 242, 175, 30),
                text='Toggle Power Saver Mode',
                manager=manager
            )
            CLOSE_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(308, 312, 75, 40),
                text='Close',
                manager=manager
            )
            SAVE_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 440, 150, 40),
                text='Save',
                manager=manager
            )
            LOAD_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(308, 352, 75, 40),
                text='Load',
                manager=manager
            )
            POSITIVE_INCREMENT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(308, 435, 75, 25),
                text='+',
                manager=manager
            )
            NEGATIVE_INCREMENT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(308, 408, 75, 25),
                text='-',
                manager=manager
            )
            APPLY_CHANGES = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 290, 150, 30),
                text='Apply Changes',
                manager=manager
            )
            QUIET_FAN = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(1100, 260, 175, 40),
                text='Quiet Fan',
                manager=manager
            )
            BALANCED_FAN = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(1100, 300, 175, 40),
                text='Balanced Fan',
                manager=manager
            )
            PERFORMANCE_FAN = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(1100, 340, 175, 40),
                text='Performance Fan',
                manager=manager
            )
            # HUD information
            CURRENT_TDP_VALUE = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect(525, 185, 225, 50),
                html_text="Current TDP Target: ",
                manager=manager
            )
            BOOST_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(850, 100, 150, 50),
                text=BOOST,
                manager=manager
            )
            SMT_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(1050, 100, 150, 50),
                text=SMT,
                manager=manager
            )
            POWER_PROFILE_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(0, 75, 225, 100),
                text="Power Profile: Not Enabled",
                manager=manager
            )
            FAN_CURVE_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(250, 75, 225, 100),
                text="Fan Curve: Not Set",
                manager=manager
            )
            HHFC_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(600, 75, 225, 100),
                text="",
                manager=manager
            )
            RYZENADJ_STATUS_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(450, 75, 225, 100),
                text="",
                manager=manager
            )
            TEXT_FIELD_SUMMARY = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect(0, 0, 1280, 100),
                html_text="System Name: " + system_name + "\n" + "CPU Name: " + subprocess.check_output(
                    "lscpu | grep \"Model name\" | cut -d : -f 2 | xargs", shell=True, universal_newlines=True).strip(),
                manager=manager
            )
            IMAGE_1 = pygame_gui.elements.UIImage(
                relative_rect=pygame.Rect(375, 250, 525, 325),
                image_surface=pygame.image.load(
                    'usr/lib/temperamental/assets/images/aya-neo-2-ctr.png').convert_alpha(),
                manager=manager
            )
                                    
        case "Steam Deck":
          MIN_BUTTON = pygame_gui.elements.UIButton(
                                       relative_rect=pygame.Rect(420,280,100,25),
                                       text=str(int(MIN_TDP) // 1000) + "W TDP",
                                       manager=manager
                                   )
          TIER1_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(320,260,100,25),
                                      text=str(int(STEP_ONE) // 1000) + "W TDP",
                                      manager=manager
                                  )
          TIER2_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(855,260,100,25),
                                      text=str(int(STEP_TWO) // 1000) + "W TDP",
                                      manager=manager
                                  )
          MAX_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(755,280,100,25),
                                      text=str(int(MAX_TDP) // 1000) + "W TDP",
                                      manager=manager
                                  )
          DEFAULT_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(475,760,175,40),
                                      text='Restore Defaults',
                                      manager=manager
                                  )
          SMT_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(0,770,175,30),
                                      text='Toggle SMT',
                                      manager=manager
                                  )
          BOOST_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(0,740,175,30),
                                      text='Toggle CPU Boost',
                                      manager=manager
                                  )
          PERFORMANCE_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(0,710,175,30),
                                      text='Toggle Performance Mode',
                                      manager=manager
                                  )
          POWERSAVER_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(0,680,175,30),
                                      text='Toggle Power Saver Mode',
                                      manager=manager
                                  )
          CLOSE_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(894,340,140,25),
                                      text='Close',
                                      manager=manager
                                  )
          SAVE_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(335,760,70,40),
                                      text='Save',
                                      manager=manager
                                  )
          LOAD_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(250,760,70,40),
                                      text='Load',
                                      manager=manager
                                  )
          POSITIVE_INCREMENT_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(300,417,75,25),
                                      text='+',
                                      manager=manager
                                  )
          NEGATIVE_INCREMENT_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(300,382,75,25),
                                      text='-',
                                      manager=manager
                                  )
          APPLY_CHANGES = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(900,417,140,25),
                                      text='Apply Changes',
                                      manager=manager
                                  )
          QUIET_FAN = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(1100,260,175,40),
                                      text='Quiet Fan',
                                      manager=manager
                                  )
          BALANCED_FAN = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(1100,300,175,40),
                                      text='Balanced Fan',
                                      manager=manager
                                  )
          PERFORMANCE_FAN = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(1100,340,175,40),
                                      text='Performance Fan',
                                      manager=manager
                                  )
          # HUD information
          CURRENT_TDP_VALUE = pygame_gui.elements.UITextBox(
                                      relative_rect=pygame.Rect(525,200,225,50),
                                      html_text="Current TDP Target: ",
                                      manager=manager
          )
          BOOST_LABEL = pygame_gui.elements.UILabel(
                                      relative_rect=pygame.Rect(1100,150,150,50),
                                      text=BOOST,
                                      manager=manager
          )
          SMT_LABEL = pygame_gui.elements.UILabel(
                                      relative_rect=pygame.Rect(1100,200,150,50),
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
                                      text="Fan Curve: Not Set",
                                      manager=manager
          )
          HHFC_LABEL = pygame_gui.elements.UILabel(
                                      relative_rect=pygame.Rect(600,75,225,100),
                                      text="",
                                      manager=manager
          )
          RYZENADJ_STATUS_LABEL = pygame_gui.elements.UILabel(
                                      relative_rect=pygame.Rect(450,75,225,100),
                                      text="",
                                      manager=manager
          )
          TEXT_FIELD_SUMMARY = pygame_gui.elements.UITextBox(
                                      relative_rect=pygame.Rect(0,0,1280,100),
                                      html_text="System Name: " + system_name + "\n" +"CPU Name: " + subprocess.check_output("lscpu | grep \"Model name\" | cut -d : -f 2 | xargs", shell=True, universal_newlines=True).strip(),
                                      manager=manager
          )
          IMAGE_1 = pygame_gui.elements.UIImage(
                                      relative_rect=pygame.Rect(375,250,525,325),
                                      image_surface= pygame.image.load('usr/lib/temperamental/assets/images/sd-ctr.png').convert_alpha(),
                                      manager=manager
          )

        case "DEFAULT":
            MIN_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 415, 150, 35),
                text=str(int(MIN_TDP) // 1000) + "W TDP",
                manager=manager
            )
            TIER1_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 370, 135, 35),
                text=str(int(STEP_ONE) // 1000) + "W TDP",
                manager=manager
            )
            TIER2_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 328, 115, 35),
                text=str(int(STEP_TWO) // 1000) + "W TDP",
                manager=manager
            )
            MAX_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 460, 115, 35),
                text=str(int(MAX_TDP) // 1000) + "W TDP",
                manager=manager
            )
            DEFAULT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(550, 508, 175, 50),
                text='Restore Defaults',
                manager=manager
            )
            SMT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(850, 290, 175, 30),
                text='Toggle SMT',
                manager=manager
            )
            BOOST_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(247, 275, 180, 30),
                text='Toggle CPU Boost',
                manager=manager
            )
            PERFORMANCE_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(247, 241, 225, 30),
                text='Toggle Performance Mode',
                manager=manager
            )
            POWERSAVER_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(800, 241, 225, 30),
                text='Toggle Power Saver Mode',
                manager=manager
            )
            CLOSE_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(308, 335, 90, 40),
                text='Close',
                manager=manager
            )
            SAVE_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 500, 150, 40),
                text='Save',
                manager=manager
            )
            LOAD_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(308, 375, 90, 40),
                text='Load',
                manager=manager
            )
            POSITIVE_INCREMENT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(325, 462, 75, 25),
                text='+',
                manager=manager
            )
            NEGATIVE_INCREMENT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(325, 434, 75, 25),
                text='-',
                manager=manager
            )
            APPLY_CHANGES = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(247, 305, 150, 25),
                text='Apply Changes',
                manager=manager
            )
            QUIET_FAN = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(1100, 260, 175, 40),
                text='Quiet Fan',
                manager=manager
            )
            BALANCED_FAN = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(1100, 300, 175, 40),
                text='Balanced Fan',
                manager=manager
            )
            PERFORMANCE_FAN = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(1100, 340, 175, 40),
                text='Performance Fan',
                manager=manager
            )
            # HUD information
            CURRENT_TDP_VALUE = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect(525, 200, 225, 50),
                html_text="Current TDP Target: ",
                manager=manager
            )
            BOOST_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(850, 100, 150, 50),
                text=BOOST,
                manager=manager
            )
            SMT_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(1050, 100, 150, 50),
                text=SMT,
                manager=manager
            )
            POWER_PROFILE_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(0, 75, 225, 100),
                text="Power Profile: Not Enabled",
                manager=manager
            )
            FAN_CURVE_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(250, 75, 225, 100),
                text="Fan Curve: Not Set",
                manager=manager
            )
            HHFC_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(600, 75, 225, 100),
                text="",
                manager=manager
            )
            RYZENADJ_STATUS_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(450, 75, 225, 100),
                text="",
                manager=manager
            )
            TEXT_FIELD_SUMMARY = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect(0, 0, 1280, 100),
                html_text="System Name: " + system_name + "\n" + "CPU Name: " + subprocess.check_output(
                    "lscpu | grep \"Model name\" | cut -d : -f 2 | xargs", shell=True, universal_newlines=True).strip(),
                manager=manager
            )
            IMAGE_1 = pygame_gui.elements.UIImage(
                relative_rect=pygame.Rect(375, 250, 525, 325),
                image_surface=pygame.image.load(
                    'usr/lib/temperamental/assets/images/xbox-ctr.png').convert_alpha(),
                manager=manager
            )

        case "Desktop":

            MIN_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(340, 250, 100, 25),
                text=str(int(MIN_TDP) // 1000) + "W TDP",
                manager=manager
            )
            TIER1_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(320, 280, 100, 25),
                text=str(int(STEP_ONE) // 1000) + "W TDP",
                manager=manager
            )
            TIER2_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(835, 250, 100, 25),
                text=str(int(STEP_TWO) // 1000) + "W TDP",
                manager=manager
            )
            MAX_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(855, 280, 100, 25),
                text=str(int(MAX_TDP) // 1000) + "W TDP",
                manager=manager
            )
            DEFAULT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(475, 760, 175, 40),
                text='Restore Defaults',
                manager=manager
            )
            SMT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(0, 770, 175, 30),
                text='Toggle SMT',
                manager=manager
            )
            BOOST_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(0, 740, 175, 30),
                text='Toggle CPU Boost',
                manager=manager
            )
            PERFORMANCE_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(0, 710, 175, 30),
                text='Toggle Performance Mode',
                manager=manager
            )
            POWERSAVER_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(0, 680, 175, 30),
                text='Toggle Power Saver Mode',
                manager=manager
            )
            CLOSE_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(860, 355, 70, 25),
                text='Close',
                manager=manager
            )
            SAVE_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(335, 760, 70, 40),
                text='Save',
                manager=manager
            )
            LOAD_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(250, 760, 70, 40),
                text='Load',
                manager=manager
            )
            POSITIVE_INCREMENT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(325, 495, 75, 25),
                text='+',
                manager=manager
            )
            NEGATIVE_INCREMENT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(335, 390, 75, 25),
                text='-',
                manager=manager
            )
            APPLY_CHANGES = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(865, 420, 150, 25),
                text='Apply Changes',
                manager=manager
            )
            QUIET_FAN = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(1100, 260, 175, 40),
                text='Quiet Fan',
                manager=manager
            )
            BALANCED_FAN = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(1100, 300, 175, 40),
                text='Balanced Fan',
                manager=manager
            )
            PERFORMANCE_FAN = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(1100, 340, 175, 40),
                text='Performance Fan',
                manager=manager
            )
            # HUD information
            CURRENT_TDP_VALUE = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect(525, 200, 225, 50),
                html_text="Current TDP Target: ",
                manager=manager
            )
            BOOST_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(1100, 150, 150, 50),
                text=BOOST,
                manager=manager
            )
            SMT_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(1100, 200, 150, 50),
                text=SMT,
                manager=manager
            )
            POWER_PROFILE_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(0, 75, 225, 100),
                text="Power Profile: Not Enabled",
                manager=manager
            )
            FAN_CURVE_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(250, 75, 225, 100),
                text="Fan Curve: Not Set",
                manager=manager
            )
            HHFC_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(600, 75, 225, 100),
                text="",
                manager=manager
            )
            RYZENADJ_STATUS_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(450, 75, 225, 100),
                text="",
                manager=manager
            )
            TEXT_FIELD_SUMMARY = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect(0, 0, 1280, 100),
                html_text="System Name: " + system_name + "\n" + "CPU Name: " + subprocess.check_output(
                    "lscpu | grep \"Model name\" | cut -d : -f 2 | xargs", shell=True, universal_newlines=True).strip(),
                manager=manager
            )
            IMAGE_1 = pygame_gui.elements.UIImage(
                relative_rect=pygame.Rect(375, 250, 525, 325),
                image_surface=pygame.image.load(
                    'usr/lib/temperamental/assets/images/xbox-ctr.png').convert_alpha(),
                manager=manager
            )
            
        case "AOKZOE A1 AR07":
            MIN_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 382, 100, 25),
                text=str(int(MIN_TDP) // 1000) + "W TDP",
                manager=manager
            )
            TIER1_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 355, 100, 25),
                text=str(int(STEP_ONE) // 1000) + "W TDP",
                manager=manager
            )
            TIER2_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 328, 100, 25),
                text=str(int(STEP_TWO) // 1000) + "W TDP",
                manager=manager
            )
            MAX_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 410, 100, 25),
                text=str(int(MAX_TDP) // 1000) + "W TDP",
                manager=manager
            )
            DEFAULT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(460, 508, 350, 50),
                text='Restore Defaults',
                manager=manager
            )
            SMT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(820, 250, 175, 30),
                text='Toggle SMT',
                manager=manager
            )
            BOOST_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(275, 250, 175, 30),
                text='Toggle CPU Boost',
                manager=manager
            )
            PERFORMANCE_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(455, 242, 175, 30),
                text='Toggle Performance Mode',
                manager=manager
            )
            POWERSAVER_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(640, 242, 175, 30),
                text='Toggle Power Saver Mode',
                manager=manager
            )
            CLOSE_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(308, 312, 75, 40),
                text='Close',
                manager=manager
            )
            SAVE_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 440, 150, 40),
                text='Save',
                manager=manager
            )
            LOAD_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(308, 352, 75, 40),
                text='Load',
                manager=manager
            )
            POSITIVE_INCREMENT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(308, 435, 75, 25),
                text='+',
                manager=manager
            )
            NEGATIVE_INCREMENT_BUTTON = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(308, 408, 75, 25),
                text='-',
                manager=manager
            )
            APPLY_CHANGES = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(878, 290, 150, 30),
                text='Apply Changes',
                manager=manager
            )
            QUIET_FAN = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(1100, 260, 175, 40),
                text='Quiet Fan',
                manager=manager
            )
            BALANCED_FAN = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(1100, 300, 175, 40),
                text='Balanced Fan',
                manager=manager
            )
            PERFORMANCE_FAN = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(1100, 340, 175, 40),
                text='Performance Fan',
                manager=manager
            )
            # HUD information
            CURRENT_TDP_VALUE = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect(525, 185, 225, 50),
                html_text="Current TDP Target: ",
                manager=manager
            )
            BOOST_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(850, 100, 150, 50),
                text=BOOST,
                manager=manager
            )
            SMT_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(1050, 100, 150, 50),
                text=SMT,
                manager=manager
            )
            POWER_PROFILE_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(0, 75, 225, 100),
                text="Power Profile: Not Enabled",
                manager=manager
            )
            FAN_CURVE_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(250, 75, 225, 100),
                text="Fan Curve: Not Set",
                manager=manager
            )
            HHFC_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(600, 75, 225, 100),
                text="",
                manager=manager
            )
            RYZENADJ_STATUS_LABEL = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect(450, 75, 225, 100),
                text="",
                manager=manager
            )
            TEXT_FIELD_SUMMARY = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect(0, 0, 1280, 100),
                html_text="System Name: " + system_name + "\n" + "CPU Name: " + subprocess.check_output(
                    "lscpu | grep \"Model name\" | cut -d : -f 2 | xargs", shell=True, universal_newlines=True).strip(),
                manager=manager
            )
            IMAGE_1 = pygame_gui.elements.UIImage(
                relative_rect=pygame.Rect(375, 250, 525, 325),
                image_surface=pygame.image.load(
                    'usr/lib/temperamental/assets/images/aokzoe-ctr.png').convert_alpha(),
                manager=manager
            )

                      
        case other:
          MIN_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(340,250,100,25),
                                      text=str(int(MIN_TDP) // 1000) + "W TDP",
                                      manager=manager
                                  )
          TIER1_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(320,280,100,25),
                                      text=str(int(STEP_ONE) // 1000) + "W TDP",
                                      manager=manager
                                  )
          TIER2_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(835,250,100,25),
                                      text=str(int(STEP_TWO) // 1000) + "W TDP",
                                      manager=manager
                                  )
          MAX_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(855,280,100,25),
                                      text=str(int(MAX_TDP) // 1000) + "W TDP",
                                      manager=manager
                                  )
          DEFAULT_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(475,760,175,40),
                                      text='Restore Defaults',
                                      manager=manager
                                  )
          SMT_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(0,770,175,30),
                                      text='Toggle SMT',
                                      manager=manager
                                  )
          BOOST_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(0,740,175,30),
                                      text='Toggle CPU Boost',
                                      manager=manager
                                  )
          PERFORMANCE_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(0,710,175,30),
                                      text='Toggle Performance Mode',
                                      manager=manager
                                  )
          POWERSAVER_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(0,680,175,30),
                                      text='Toggle Power Saver Mode',
                                      manager=manager
                                  )
          CLOSE_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(860,355,70,25),
                                      text='Close',
                                      manager=manager
                                  )
          SAVE_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(335,760,70,40),
                                      text='Save',
                                      manager=manager
                                  )
          LOAD_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(250,760,70,40),
                                      text='Load',
                                      manager=manager
                                  )
          POSITIVE_INCREMENT_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(325,495,75,25),
                                      text='+',
                                      manager=manager
                                  )
          NEGATIVE_INCREMENT_BUTTON = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(335,390,75,25),
                                      text='-',
                                      manager=manager
                                  )
          APPLY_CHANGES = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(865,420,150,25),
                                      text='Apply Changes',
                                      manager=manager
                                  )
          QUIET_FAN = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(1100,260,175,40),
                                      text='Quiet Fan',
                                      manager=manager
                                  )
          BALANCED_FAN = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(1100,300,175,40),
                                      text='Balanced Fan',
                                      manager=manager
                                  )
          PERFORMANCE_FAN = pygame_gui.elements.UIButton(
                                      relative_rect=pygame.Rect(1100,340,175,40),
                                      text='Performance Fan',
                                      manager=manager
                                  )
          # HUD information
          CURRENT_TDP_VALUE = pygame_gui.elements.UITextBox(
                                      relative_rect=pygame.Rect(525,200,225,50),
                                      html_text="Current TDP Target: ",
                                      manager=manager
          )
          BOOST_LABEL = pygame_gui.elements.UILabel(
                                      relative_rect=pygame.Rect(1100,150,150,50),
                                      text=BOOST,
                                      manager=manager
          )
          SMT_LABEL = pygame_gui.elements.UILabel(
                                      relative_rect=pygame.Rect(1100,200,150,50),
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
                                      text="Fan Curve: Not Set",
                                      manager=manager
          )
          HHFC_LABEL = pygame_gui.elements.UILabel(
                                      relative_rect=pygame.Rect(600,75,225,100),
                                      text="",
                                      manager=manager
          )
          RYZENADJ_STATUS_LABEL = pygame_gui.elements.UILabel(
                                      relative_rect=pygame.Rect(450,75,225,100),
                                      text="",
                                      manager=manager
          )
          TEXT_FIELD_SUMMARY = pygame_gui.elements.UITextBox(
                                      relative_rect=pygame.Rect(0,0,1280,100),
                                      html_text="System Name: " + system_name + "\n" +"CPU Name: " + subprocess.check_output("lscpu | grep \"Model name\" | cut -d : -f 2 | xargs", shell=True, universal_newlines=True).strip(),
                                      manager=manager
          )
          IMAGE_1 = pygame_gui.elements.UIImage(
                                      relative_rect=pygame.Rect(375,250,525,325),
                                      image_surface= pygame.image.load('usr/lib/temperamental/assets/images/xbox-ctr.png').convert_alpha(),
                                      manager=manager
          )
