# cv compare: https://stackoverflow.com/questions/11094481/capturing-a-single-image-from-my-webcam-in-java-or-python
# cv settings: https://stackoverflow.com/questions/32943227/python-opencv-capture-images-from-webcam
# another compareg: https://softwarerecs.stackexchange.com/questions/18134/python-library-for-taking-camera-images
# Timestamp: http://startgrid.blogspot.com/2012/08/tutorial-creating-timestamp-on.html
import time
import wget
import os
import cv2
#import settings f my_globals
from my_globals import settings


image = settings["img_dir"] + settings["img_name"]      # full path to image

cam = cv2.VideoCapture()
print "camera: ", cam



def remove_image():
    # remove current picture
    try:
        os.remove(image)
    except OSError:
        pass

def get_cat_picture():
    url = "http://lorempixel.com/1024/768/cats/"
    #remove_image()
    cat_pic = wget.download(url, out=image)
    print "filename: ", cat_pic



def get_Picture():
    #get_cat_picture()
    #return

    global count
    print "Picture",
    global cam
    time.sleep(0.1) #wait for camera initialization
    return_value, image = cam.read()

    print "-saving",
    filename = settings["img_dir"] + settings["img_name"]      # full path to image
    # print filename                # debugger
    cv2.imwrite(filename, image)
    print "-done"
