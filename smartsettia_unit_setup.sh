#!/bin/bash

echo "Setting up smartsettia"

sudo apt update
#https://www.saltycrane.com/blog/2010/02/how-install-pip-ubuntu/
sudo apt install  python-pip
sudo apt install --upgrade pip
sudo apt install --upgrade vertualenv


echo "Installing dependencies"
sudo pip install schedule

echo "Done"
