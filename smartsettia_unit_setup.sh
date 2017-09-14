#!/bin/bash

# get root permission
if [ $EUID != 0 ]; then
    sudo "$0" "$@"
    exit $?
fi

echo "Setting up smartsettia"

apt update
#https://www.saltycrane.com/blog/2010/02/how-install-pip-ubuntu/
apt install  python-pip -y
apt install --upgrade pip
apt install --upgrade vertualenv


echo -e "\nInstalling dependencies"
pip install schedule

echo -e "\nSetting up ramdisk for pictures (disabled atm)"
apt install tmpfs -y    #install the ramdisk software
mkdir -p /mnt/ramdisk   #make the mount directory
MOUNTCODE="tmpfs       /mnt/ramdisk tmpfs   nodev,nosuid,noexec,nodiratime,size=11M   0 0"
#check if fstab already has this line. if not add it.
grep -q -F "$MOUNTCODE" /etc/fstab || echo "$MOUNTCODE" >> /etc/fstab
mount -a               # mount the ramdisk

echo -e "\nDone"
