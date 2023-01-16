#!/bin/bash

# Run as Steam Deck
echo "Use DISPLAY=:1 if running from desktop, use DISPLAY=:0 if running from a session"
DISPLAY=:0 /usr/lib/temperamental/./gamescope-xprops-swap /usr/lib/temperamental/temperamental.py

