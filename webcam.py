# cv compare: https://stackoverflow.com/questions/11094481/capturing-a-single-image-from-my-webcam-in-java-or-python
# cv settings: https://stackoverflow.com/questions/32943227/python-opencv-capture-images-from-webcam
# another compareg: https://softwarerecs.stackexchange.com/questions/18134/python-library-for-taking-camera-images
# Timestamp: http://startgrid.blogspot.com/2012/08/tutorial-creating-timestamp-on.html
import time
#from SimpleCV import *
import cv2


def get_Picture():
    print "Picture",
    cam = cv2.VideoCapture(0)
    time.sleep(0.1) #wait for camera initialization
    return_value, image = cam.read()

    print "-saving",
    filename = "Webcam_picture.png"
    cv2.imwrite(filename, image)
    del(cam)
    print "-done"
