#!/usr/bin/python3
import time
from os import path   # Used in checking webcam storage path
import threading
import schedule    # scheduler library
import webcam      # webcam module
import my_globals  # global variables
import remote_comm # server communication module
import argparse    # argument parsing
from helper_lib import print_error, print_log, generate_uuid


# https://stackoverflow.com/a/30493366
parser = argparse.ArgumentParser()
parser.add_argument('-s',  '--single',     action='store_true', help='Runs the program loop only once')
parser.add_argument('-fw', '--fakewebcam', action='store_true', help='Use Fake webcam')
parser.add_argument('-d',   type=int,      action='store',      help='Specify Domain. 0 prod, 1 brandon c9, 2 nick c9. Default 0', default="0")
parser.add_argument('-cd',  type=str,      action='store',      help='Specify custom Domain. This overrides all other domain settings', default=None)
parser.add_argument('-npi', '--notpi',     action='store_true', help='Run as if this was not a raspberry pi. Disables GPIO reading', default="False")
args = parser.parse_args() # parse args
my_globals.NOT_PI = args.notpi
DOMAIN_INDEX = args.d
DOMAIN_CUSTOM = args.cd
SINGLE_RUN = args.single
FAKEWEBCAM = args.fakewebcam     # enable or disable fake webcam
print ("cust domain: ", args.cd)

from cover import fsm, gpio_cleanup   # cover monitor module. Must be imported after NOT_PI has been set
import sensors     #sensors.py

# multi thread support
def run_threaded(job_func):
	job_thread = threading.Thread(target=job_func)
	job_thread.start()

# If I'm running you should see this periodically
def job_heartbeat():
    print("I'm working...")

# Save setting to file
def job_save_settings():
    my_globals.save_settings()
    
def job_cover_monitor():
    fsm()

# Read enviroment sensors
def job_sensors():
    print("Getting Sensors..")
    sensors.update()
    print ("\ttemp: %d, cpu_temp: %d" %(my_globals.sensor_dat["temperature"], my_globals.sensor_dat["cpu_temp"]))
    remote_comm.sensor_upload()

# send status to server
def job_upload_status():
    #print ("Uploading status")
    remote_comm.status_update()

# take a picture
def job_webcam():
    t0 = int(round(time.time() * 1000)) # debugger
    webcam.get_Picture(FAKEWEBCAM)      # get picture function with option fake bool
    t1 = int(round(time.time() * 1000)) # debugger
    print ("timepic: %d" % (t1-t0))      # debugger
    remote_comm.pic_upload()

schedule.every(20).seconds.do(job_heartbeat)
schedule.every(60).seconds.do(job_save_settings)
schedule.every(5).seconds.do(job_sensors)
schedule.every(3).seconds.do(job_webcam)
schedule.every(2).seconds.do(job_upload_status)
schedule.every(1).seconds.do(job_cover_monitor)
#webserver


#function Deff

def initialize():
    generate_uuid()                 # generate uuid from hardware
    my_globals.load_settings()      # load settings from file
    
    print ("Using fake webcam: ", FAKEWEBCAM)
    if (my_globals.NOT_PI == True):
        print("Not Pi flag set. GPIO is disabled.")
    
    # Validate args.d (domain index) with possible domain indexes
    if (DOMAIN_INDEX >= 0 and DOMAIN_INDEX < len(my_globals.DOMAIN) and DOMAIN_CUSTOM == None):
        my_globals.update_url(my_globals.DOMAIN[DOMAIN_INDEX])
    elif (DOMAIN_CUSTOM != None):
        print("Using custom domain. Overriding url settings.")
        my_globals.update_url(DOMAIN_CUSTOM)
    else:
        print ("Error invalid domain index. Exiting")
        print ("To specify domain use '-d' <index>. from 0 to %d. For more info use '--help'" % (len(my_globals.DOMAIN)-1))
        exit()
    
    # check if /mnt/ramdisk exists else fallback to tmp directory
    if path.isdir(my_globals.settings["img_dir"]) == 0:   # if path to directory exists
        print ("Ramdisk does not exist. Using /tmp/")
        # This is undesirable for sdcard wear and writing speed compared to a ramdisk
        my_globals.settings["img_dir"] = "/tmp/"
    
    remote_comm.register()          # register device with webserver
    
    # run the cover montitor a few times to let it syncronize
    job_cover_monitor()
    job_cover_monitor()


#Program start
print ("\nWelcome to Smartsettia!")
initialize()

# if single run run everything once
if SINGLE_RUN:
    print("Running single mode")
    schedule.run_all()      # run all jobs
    gpio_cleanup()
    exit()              # exit program

while True and not SINGLE_RUN:
    schedule.run_pending()
    time.sleep(0.1)
