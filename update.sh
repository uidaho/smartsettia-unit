#!/bin/bash

# get root permission
if [ $EUID != 0 ]; then
    sudo "$0" "$@"
    exit $?
fi

BRANCH="master"

# if -d flag given then switch and pull development branch
if [[ $* == *-d* ]]; then
    echo "Using development branch"
    BRANCH="development"
fi

echo "Updating smartsettia - $BRANCH"

git status
sudo systemctl stop smartsettia.service || exit
sleep 1
git checkout $BRANCH || exit
git pull
sudo systemctl start smartsettia.service

echo "Done"
