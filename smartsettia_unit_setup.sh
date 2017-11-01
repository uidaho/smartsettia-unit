#!/bin/bash

# only clean and exit
if [[ $* == *-C* ]]; then
  echo "Removing .logs & .pyc files then exiting"
  rm -f *.log *.pyc
  exit
fi

# get root permission
if [ $EUID != 0 ]; then
    sudo "$0" "$@"
    exit $?
fi

FLAG_RAMDISK=0;

# cleaning
if [[ $* == *-c* ]]; then
  echo "Removing .logs & .pyc files"
  rm -f *.log *.pyc
fi



# yes for questions
# for travis builds
if [[ $* == *--y* ]]; then
  FLAG_RAMDISK=1;
else
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
apt install -y python3 python3-pip
#pip install --upgrade pip
#pip install --upgrade virtualenv
# apt install -y fswebcam   # old webcam implementation
apt install -y xawtv        # webcam
apt install -y imagemagick  # Adds overlay to photos


echo -e "\nInstalling python dependencies"
echo      "-----------------------"
pip3 install --upgrade schedule
pip3 install --upgrade requests
pip3 install --upgrade wget     # webcam replacement if no webcam
pip3 install --upgrade call
pip3 install --upgrade uuid     # is this really needed?
pip3 install --upgrade RPI.GPIO # gpio


echo -e "\nSetting up Environment"
echo      "-----------------------"
sudo timedatectl set-timezone Etc/UTC  # may not work on other platforms


if [ $FLAG_RAMDISK -eq "1" ]; then
  echo -e "\nSetting up ramdisk for pictures & logs"
  echo      "-------------------------------"
  mkdir -p /mnt/ramdisk   #make the mount directory
  MOUNTCODE="tmpfs       /mnt/ramdisk tmpfs   nodev,nosuid,noexec,nodiratime,size=100M   0 0"
  #check if fstab already has this line. if not add it.
  grep -q -F "$MOUNTCODE" /etc/fstab || echo "$MOUNTCODE" >> /etc/fstab
  mount -a               # mount the ramdisk
fi


echo -e "\nSmartsettia setup done"
echo      "----------------------"
