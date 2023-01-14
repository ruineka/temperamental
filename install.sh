#!/bin/bash

if [ $EUID -ne 0 ]; then
	echo "You need sudo permissions to run this"
	exit 1
fi

mkdir -p /usr/share/temperamental/profiles
mkdir -p /usr/bin/temperamental-polkit-helpers/
cp -r profiles /usr/share/temperamental/
cp -r temperamental-polkit-helpers/ /usr/bin/
cp org.ruineka.temperamental.policy /usr/share/polkit-1/actions/


# Set up the sudo permissions
echo "***POSSIBLE SECURITY RISK. UNDERSTAND THE FOLLOWING***"
echo "Adding password free sudo access to the following files for user ${SUDO_USER}:"
echo "/sys/devices/system/cpu/cpufreq/boost"
echo "/sys/devices/system/cpu/smt/control"
cat <<-EOF > "/etc/sudoers.d/temperamental_sudo"
${SUDO_USER} ALL=(ALL) NOPASSWD: /usr/bin/tee /sys/devices/system/cpu/cpufreq/boost*
${SUDO_USER} ALL=(ALL) NOPASSWD: /usr/bin/tee /sys/devices/system/cpu/smt/control*
EOF

echo "Installed Successfully"

