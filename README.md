# smartsettia-unit
Unit software for University of Idaho CS480 Capstone Project

## Instructions

### Raspberri Pi Setup
Download Raspbian 
[https://www.raspberrypi.org/downloads/raspbian/](https://www.raspberrypi.org/downloads/raspbian/)
unzip the file.

Follow these instructions
https://www.raspberrypi.org/documentation/installation/installing-images/README.md
or [download Rufus](https://rufus.akeo.ie/) and flash the image

Run `sudo raspi-config`



1. Change User Password – This step is recommended! Follow the on-screen directions to set a new password for you Pi. By default the password is set to raspberry, and the user is set to pi.

1. Change Hostname to `Smartsettia-Unit`

1. Enable Boot to Desktop/Scratch – Select whether to boot into desktop or simply the text console. The console mode will obviously boot faster, and you can type Startx to open the GUI. Booting to desktop may be easier for those more comfortable with Windows or Mac, though.
Internationalisation Options – Here you can adjust the timezone, keyboard layout, and language of your Pi. These changes take a while to be made, so be patient.

1. Localization - By default raspberian is in britain.
   * Change Locale - By default raspberian is in britain. Use `en_US.UTF-8`
   * Change Timezonee - US is labled as `Pacific-New` for some reason

1. Advanced Options
   * Expand Filesystem
  
1. Interfacing Options
   * SSH - Enable if you need it
   * I2C - Enable
  
1. Finish
1. Reboot `sudo reboot`


### Smartsettia Setup
Run the following commands
```bash
sudo apt update
sudo apt install git
git clone https://github.com/uidaho/smartsettia-unit.git
```
Change directory into the cloned folder.
`cd smartsettia-unit`

Run the setup script.
`sudo ./smartsettia_unit_setup.sh`

## Running Smartsettia
`./main.py`



References
https://learn.sparkfun.com/tutorials/setting-up-raspbian-and-doom#setup-raspbian
