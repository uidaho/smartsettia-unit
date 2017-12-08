#!/bin/bash

BRANCH="master"

# if -d flag given then switch and pull development branch
if [[ $* == *-d* ]]; then
    echo "Using development branch"
    BRANCH="development"
fi

echo "Updating smartsettia"

git status
sudo systemctl stop smartsettia.service \
&& sleep 1  \
&& git checkout $BRANCH \
&& git pull \
sudo systemctl start smartsettia.service

echo "Done"