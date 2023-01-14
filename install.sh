#!/bin/bash

if [ $EUID -ne 0 ]; then
	echo "You need sudo permissions to run this"
	exit 1
fi

mkdir -p /usr/share/temperamental/profiles
mkdir -p /usr/bin/temperamental-polkit-helpers/
cp -r profiles /usr/share/temperamental/
cp -r temperamental-polkit-helpers/ /usr/bin/

echo "Installed Successfully"

