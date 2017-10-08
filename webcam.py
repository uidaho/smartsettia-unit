# cv compare: https://stackoverflow.com/questions/11094481/capturing-a-single-image-from-my-webcam-in-java-or-python
# cv settings: https://stackoverflow.com/questions/32943227/python-opencv-capture-images-from-webcam
# another compareg: https://softwarerecs.stackexchange.com/questions/18134/python-library-for-taking-camera-images
# Timestamp: http://startgrid.blogspot.com/2012/08/tutorial-creating-timestamp-on.html
# fswebcam: https://www.raspberrypi.org/documentation/usage/webcams/
# fswebcam doc: https://www.systutorials.com/docs/linux/man/1-fswebcam/
import time
import wget
import os
from subprocess import call
#from my_globals import settings  #import settings from my_globals
import my_globals


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
    cat_pic = wget.download(url, out=filename)
    print ("filename: ", cat_pic)


def get_Picture(FAKEWEBCAM):
    print ("\n--- Getting picture ------------------")
    filename = my_globals.settings["img_dir"] + my_globals.settings["img_name"]      # full path to image
    print ("Img Filename: ", filename)
    if FAKEWEBCAM == 1:     # get fake picture
        get_cat_picture(filename)
        return
    else:                   # get picture from webcam
        global filename
        # setup some metadata for fswebcam
        compression = "95"
        device      = "/dev/video0"
        resolution  = "1280x720"
        textcolor   = "#0000cc00"
        font        = "luxisr:14"
        title       = str(my_globals.settings["name"])
        subtitle    = "cpu null"  #"cpu: {} C".format(cpu_temp())
        info        =  str(my_globals.settings["uuid"])

        # call fswebcam to take the picture
        call(["fswebcam", "-S 3", "--jpeg", compression, "-d", device, "-r", resolution,
         "--top-banner", "--text-colour", textcolor, "--font", font,
          "--title", title, "--subtitle", subtitle, "--info", info, filename])
