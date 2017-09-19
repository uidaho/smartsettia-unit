# cv compare: https://stackoverflow.com/questions/11094481/capturing-a-single-image-from-my-webcam-in-java-or-python
# cv settings: https://stackoverflow.com/questions/32943227/python-opencv-capture-images-from-webcam
# another compareg: https://softwarerecs.stackexchange.com/questions/18134/python-library-for-taking-camera-images
# Timestamp: http://startgrid.blogspot.com/2012/08/tutorial-creating-timestamp-on.html
import time
from SimpleCV import *
import cv2

count = 1

def get_Picture():
    global count
    print "Picture"
    cam = cv2.VideoCapture(0)
    time.sleep(1.0) #wait for camera initialization
    return_value, image = cam.read()

    print "saving pic"
    filename = "Webcam_picture_%d.png" % count
    print "Filename: ", filename
    #img.save(filename)
    cv2.imwrite(filename, image)
    del(cam)
    #count = count + 1
