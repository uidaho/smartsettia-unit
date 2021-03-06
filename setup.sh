#!/bin/bash

# get root permission
if [ $EUID != 0 ]; then
    sudo -H "$0" "$@"
    exit $?
fi

FLAG_RAMDISK=0;
CLEAN_BLOAT=0;

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
  # ramdisk
  while true; do
      read -p "Do you wish to setup the ramdisk? " yn
      case $yn in
          [Yy]* ) FLAG_RAMDISK=1; break;;
          [Nn]* ) break;;
          * ) echo "Please answer yes or no.";;
      esac
  done
  
  # clean bloat
  while true; do
    read -p "Do you wish to remove unneeded programs such as libreoffice, wolfram, scratch and some games? " yn
    case $yn in
        [Yy]* ) CLEAN_BLOAT=1; break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
  done
fi


# remove unneeded programs if enabled
if [ $CLEAN_BLOAT -eq "1" ]; then
  echo -e "\nRemoving unneeded programs"
  echo      "-------------------------------"
  sudo apt -y purge libreoffice* wolfram-engine sonic-pi scratch scratch2 minecraft-pi sense-hat
  sudo apt -y autoremove
fi


echo -e "\nSetting up smartsettia user and group"
echo -e   "----------------------"
SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# test if user exits already, if not create user
id -u smartsettia &>/dev/null || sudo useradd -M -r -U smartsettia
sudo usermod -aG pi,adm,dialout,cdrom,audio,video,plugdev,input,netdev,gpio,i2c,spi smartsettia    # pi group reverence: https://raspberrypi.stackexchange.com/a/75681
sudo chgrp -R smartsettia $SCRIPTDIR/*
#sudo usermod -aG smartsettia <user>


echo -e "\nSetting up smartsettia"
echo -e   "----------------------"
apt -qq update

# skip upgrades if -f flag is given
if [[ $* != *--f* ]]; then
  apt -q -y upgrade
fi
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
pip3 install --upgrade sdnotify # systemd watchdog support


echo -e "\nSetting up Environment"
echo      "-----------------------"
sudo timedatectl set-timezone Etc/UTC  # may not work on other platforms


echo -e "\nSetting up system service"
sudo mkdir -p /var/log/smartsettia
sudo chown -R smartsettia:smartsettia /var/log/smartsettia
SERVICE_NAME=smartsettia.service
SERVICE_PATH="/lib/systemd/system/$SERVICE_NAME"
# check if a service file already exists and delete if so.
if [ -f $SERVICE_PATH ]; then
  echo -e "\n Removing $SERVICE_NAME and replacing with new service"
  sudo rm -v $SERVICE_PATH
fi
sudo cp -v $SERVICE_NAME $SERVICE_PATH       # copy service to systemd directory
sudo chmod 644 $SERVICE_PATH
chmod +x $SERVICE_PATH


# Setup Ramdisk if enabled
if [ $FLAG_RAMDISK -eq "1" ]; then
  echo -e "\nSetting up ramdisk for pictures & logs"
  echo      "-------------------------------"
  mkdir -p /mnt/ramdisk   #make the mount directory
  sudo chown smartsettia:smartsettia /mnt/ramdisk
  MOUNTCODE="tmpfs       /mnt/ramdisk tmpfs   nodev,nosuid,noexec,nodiratime,size=100M   0 0"
  #check if fstab already has this line. if not add it.
  grep -q -F "$MOUNTCODE" /etc/fstab || echo "$MOUNTCODE" >> /etc/fstab
  mount -a               # mount the ramdisk
fi


sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME


echo -e "\nSmartsettia setup done"
echo      "----------------------"
