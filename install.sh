#!/bin/bash

if [ $EUID -ne 0 ]; then
	echo "You need sudo permissions to run this"
	exit 1
fi

mkdir -p /usr/share/temperamental/profiles
cp -r profiles /usr/share/temperamental/

echo "Installed Successfully"

