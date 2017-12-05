# another compareg: https://softwarerecs.stackexchange.com/questions/18134/python-library-for-taking-camera-images
# Timestamp: http://startgrid.blogspot.com/2012/08/tutorial-creating-timestamp-on.html

# short note on camera software
# started with opencv but it is such a large library
# used fswebcam for a while but it produced intermitant black frames. However it had build in boarders
# now using v4lctl for taking pictures and imagemagick for banners

import time
import datetime
import wget
import os
from subprocess import call
#from my_globals import settings  #import settings from my_globals
import my_globals
import logging


def remove_image(filename):
    # remove current picture
    try:
        os.remove(filename)
    except OSError:
        pass

def get_cat_picture(filename):
    #url = "http://lorempixel.com/1024/768/cats/"   # cats
    url = "http://207.251.86.238/cctv448.jpg"       # NY trafic cam
    remove_image(filename)
    cat_pic = wget.download(url, out=filename, bar=None)


def get_Picture():
    logging.info (" --- Getting picture ------------------")
    filename = my_globals.settings["storage_dir"] + my_globals.settings["img_name"]      # full path to image
    logging.debug("Img Filename: "+ filename)
    remove_image(filename)
    if my_globals.FAKEWEBCAM == 1:     # get fake picture
        get_cat_picture(filename)
    else:                   # get picture from webcam
        # setup some metadata for fswebcam
        compression = "45"
        device      = "/dev/video0"
        resolution  = "1280x720"
        #resolution  = "1024x600
        #resolution = "640x480"
        textcolor   = "#0000cc00"
        font        = "luxisr:14"
        title       = str(my_globals.settings["name"])
        subtitle    = "cpu null"  #"cpu: {} C".format(cpu_temp())
        info        =  str(my_globals.settings["uuid"])

        # call fswebcam to take the picture
        #call(["fswebcam", "-S 3", "--jpeg", compression, "-d", device, "-r", resolution, "--scale", "960x540",
         #"--top-banner", "--text-colour", textcolor, "--font", font,
         # "--title", title, "--subtitle", subtitle, "--info", info, filename])
          
        # call v4lctl to take the picture
        call(["v4lctl", "-c", device, "snap", "jpeg", resolution, filename])
        #logging.debug ("Img size: " + str(call(["du", "-h", filename])))    # prints size of picture.
    
    # overlay reference
    # overlay_text = "/usr/bin/convert "+ filename + "  -pointsize 36 -fill white -annotate +40+728 '" + "hello" + "' "  
    # overlay_text += " -pointsize 36 -fill white -annotate +40+630 'Your Text annotation here ' " + filename
    
    # The [:-4] truncates the last 4 characters of the string which is used cut out some microsecond digits
    text = '"Smartsettia - %s UTC"' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    overlay_text = "convert " + filename + " -gravity North   -background YellowGreen  -splice 0x18 \
          -annotate +0+2 " + text + " " + filename
    #logging.debug ("Webcam: convert command: %s" % overlay_text)      # debugger to see command executed
    call ([overlay_text], shell=True)