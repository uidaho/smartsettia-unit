#!/bin/bash

# get root permission
if [ $EUID != 0 ]; then
    sudo "$0" "$@"
    exit $?
fi

FLAG_GPIO=0;
FLAG_RAMDISK=0;

# yes for questions
# for travis builds
if [[ $* == *--y* ]]; then
  FLAG_GPIO=1;
  FLAG_RAMDISK=1;
else
  while true; do
      read -p "Is this Device a Raspberri Pi? " yn
      case $yn in
          [Yy]* ) FLAG_GPIO=1; break;;
          [Nn]* ) break;;
          * ) echo "Please answer yes or no.";;
      esac
  done

  while true; do
      read -p "Do you wish to setup the ramdisk? " yn
      case $yn in
          [Yy]* ) FLAG_RAMDISK=1; break;;
          [Nn]* ) break;;
          * ) echo "Please answer yes or no.";;
      esac
  done
fi

echo -e "\nSetting up smartsettia"
echo -e   "----------------------"

apt -qq update
#https://www.saltycrane.com/blog/2010/02/how-install-pip-ubuntu/
apt install -y python-pip
pip install --upgrade pip
pip install --upgrade virtualenv
apt install -y fswebcam

#https://learn.adafruit.com/playing-sounds-and-using-buttons-with-raspberry-pi/install-python-module-rpi-dot-gpio
if [ $FLAG_GPIO -eq "1" ]; then
  apt install python-rip.gpio
fi


echo -e "\nInstalling python dependencies"
echo      "-----------------------"
pip install schedule
pip install requests
pip install wget    # webcam replacement if no webcam
pip install call



if [ $FLAG_RAMDISK -eq "1" ]; then
  echo -e "\nSetting up ramdisk for pictures"
  echo      "-------------------------------"
  mkdir -p /mnt/ramdisk   #make the mount directory
  MOUNTCODE="tmpfs       /mnt/ramdisk tmpfs   nodev,nosuid,noexec,nodiratime,size=11M   0 0"
  #check if fstab already has this line. if not add it.
  grep -q -F "$MOUNTCODE" /etc/fstab || echo "$MOUNTCODE" >> /etc/fstab
  mount -a               # mount the ramdisk
fi


echo -e "\nSmartsettia setup done"
echo      "----------------------"
