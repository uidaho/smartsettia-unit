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



1. Change User Password – This step is **absolutly required!** Follow the on-screen directions to set a new password for you Pi. By default the password is set to `raspberry`, and the user is set to `pi`.

1. Under Networking
   * N1 Change Hostname to `Smartsettia-Unit` or another descriptive name
   * N2 Setup wifi. Enter 'AirVandalGuest' & `GoVandals!` to connect to guest network
      * Note: This will only work for the guest network. AirVandalGold requires additional setup
      * Wifi Settings can be configured with  `sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`


1. (optional) Enable Boot to Desktop(default) or command line – Select whether to boot into desktop or simply the text console. The console mode will obviously boot faster, and you can type Startx to open the GUI. Booting to desktop may be easier for those more comfortable with Windows or Mac, though.
Internationalisation Options – Here you can adjust the timezone, keyboard layout, and language of your Pi. These changes take a while to be made, so be patient.

1. Localization - By default raspberian is in britain.
   * T1 Change Locale - By default raspberian is in britain.
      * Use the space key to enable `en_US.UTF-8`
      * Next menu choose `en_US.UTF-8` for the default language
   * T2 Change Timezonee - `US` > `Pacific-New` or your prefered timezone
      * Note: the smartsettia-unit script uses UTC time so the device timezone does not affect the opperation of this project

1. Interfacing Options
   * SSH - (optional) Enable if you need it. More secure if left disabled
   * I2C - Enable

1. Advanced Options
   * Expand Filesystem - This will ensure that the entire sd card is available to the system
  
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
`sudo ./setup.sh -y`

## Running Smartsettia
For most situations and production the script is run and managed by the system. <br>
To check the status: `sudo systemctl status smartsettia.service` <br>
\* `status` can be replaced with the following commands: `stop`, `start`, `restart`

## Viewing Output
To view output
Follow current program output: `journalctl -u smartsettia.service -f` <br>
To see output since a date: <br>
\*  `journalctl -u smartsettia.service --since yesterday` <br>
\*  `journalctl -u smartsettia.service --since '1 hour ago'` <br>
To exit, press: `ctl + c`

For more options and controls for viewing logs: https://www.loggly.com/ultimate-guide/using-journalctl/

## Updating Smartsettia
When new code is pushed to github, you can update the device through this command <br>
``` bash
cd smartsettia-unit
./update.sh
```
Note you can add `-d` to pull and update on the development branch. `./update.sh -d`


## other program options
These commands are primarly focused for development purposes.
```
usage: main.py [-h] [-s] [-fw] [-d D] [-cd CD] [-npi] [-u UUID]

optional arguments:
  -h, --help            show this help message and exit
  -s, --single          Runs the program loop only once
  -fw, --fakewebcam     Use Fake webcam
  -d D                  Specify Domain. 0 prod, 1 brandon c9, 2 nick c9.
                        Default 0
  -cd CD                Specify custom Domain. This overrides all other domain
                        settings
  -npi, --notpi         Run as if this was not a raspberry pi. Disables GPIO
                        reading
  -u UUID, --uuid UUID  Use supplied UUID5 instead of generated uuid
```

`-s` or `--single` Runs all the internal tasks only once then exits

`fw` or `--fakewebcam` This pulls an image from a fast updating trafic camera when testing on a system without a physical camera

`-d D`  Used like `-d 2` This selects from a list of predefined urls for tesing on other development servers.

`-cd CD` Overrides server address to given address. `-cd https://httpbin.org` for example

`npi` or `notpi` Used when running on a system that does not have GPIO ports, aka hardware pins. This is used to disable GPIO outputs and simulates inputs for testing.

`-u UUID` or `-uuid UUID`  This is used to override the generated UUID number to what is provided. This can be used to replace a device and give it an existing identity. `-u "fdf9626a-65da-52ef-b43b-aed368471aa1"`

### References
https://learn.sparkfun.com/tutorials/setting-up-raspbian-and-doom#setup-raspbian
