# Temperamental
A gamepad focused TDP management tool designed with TDP control from the desktop and Steam's GamepadUI in mind.

# Dependencies
--pygame\
--pygame_gui\
--python3\
--ryzenadj\
--playsound

# Supported devices (feature incomplete at this time)
AMD ONEXPLAYER\
HP Dev One\
AOKZOE\
AYA NEO

# Planned devices to support
INTEL ONEXPLAYER

# Usage
ChimeraOS install and testing

# Switch to TTY 3 CTRL+ALT+F3
```shell
sudo frzr-unlock
sudo pacman -Sy python-pip git
pip install pygame pygame_gui
git clone https://github.com/ruineka/temperamental
cd temperamental
sudo ./install.sh
./gamepad-listener.py
```

#Switch to TTY 7 CTRL+ALT+F7

Press L3 and R3 to start temperamental in gamemode

![Screenshot from 2023-01-15 10-54-53](https://user-images.githubusercontent.com/16360335/212610590-fed6b9f7-dcab-4e30-92bd-7507cdebe758.png)

