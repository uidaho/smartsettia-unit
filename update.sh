#!/bin/bash

BRANCH="master"

# if -d flag given then switch and pull development branch
if [[ $* == *-d* ]]; then
    echo "Using development branch"
    BRANCH="development"
fi

echo "Updating smartsettia - $BRANCH"

echo -e "\n--- Stopping smartsettia service ---"
sudo -H systemctl stop smartsettia.service
#sudo -H systemctl status smartsettia.service
sleep 1
echo -e "\n--- Pulling changes ---"


# check to stay on current branch
if [[ $* != *-c* ]]; then
    git checkout $BRANCH
else
    echo "--- Staying on current branch ---"
fi
git pull
echo -e "\n--- Starting smartsettia service ---"
sudo -H systemctl start smartsettia.service
sleep 1
sudo -H systemctl status smartsettia.service

echo "--- Done ---"
