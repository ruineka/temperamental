#!/bin/bash

# Run as Steam Deck
echo "Use DISPLAY=:1 if running from desktop, use DISPLAY=:0 if running from a session"
./gamescope-xprops-swap $PWD/temperamental.py "DEFAULT"
