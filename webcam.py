# cv compare: https://stackoverflow.com/questions/11094481/capturing-a-single-image-from-my-webcam-in-java-or-python
# cv settings: https://stackoverflow.com/questions/32943227/python-opencv-capture-images-from-webcam
# another compareg: https://softwarerecs.stackexchange.com/questions/18134/python-library-for-taking-camera-images
# Timestamp: http://startgrid.blogspot.com/2012/08/tutorial-creating-timestamp-on.html
import time
import wget
import os
from subprocess import call
from my_globals import settings  #import settings from my_globals

filename = settings["img_dir"] + settings["img_name"]      # full path to image

def remove_image():
    # remove current picture
    try:
        os.remove(filename)
    except OSError:
        pass

def get_cat_picture():
    url = "http://lorempixel.com/1024/768/cats/"
    remove_image()
    cat_pic = wget.download(url, out=filename)
    print ("filename: ", cat_pic)



def get_Picture(FAKEWEBCAM):
    print ("\n--- Getting picture ----------")
    if FAKEWEBCAM == 1:     # get fake picture
        get_cat_picture()
        return
    else:                   # get picture from webcam
        global filename
        call(["fswebcam", "-d","/dev/video0", "-r", "1280x720", filename])
