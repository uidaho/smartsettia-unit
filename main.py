#!/usr/bin/python3
import time
import datetime
from os import path   # Used in checking webcam storage path
import os
import threading
import schedule    # scheduler library
import webcam      # webcam module
import my_globals  # global variables
import remote_comm # server communication module
import argparse    # argument parsing
from helper_lib import generate_uuid, is_valid_uuid
import helper_lib
import logging

# Logger: logging config   https://docs.python.org/3/howto/logging-cookbook.html
logger = logging.getLogger()
formatter = helper_lib.MyFormatter()           # sets format of the logs. Uses cusom class
logger.setLevel(logging.DEBUG)              # This essentially sets the highest logging level

# Logger: create file handler which logs even debug messages
fh = logging.FileHandler('smartsettia.log')
fh.setFormatter(formatter)      # set format
fh.setLevel(logging.INFO)    # set level for file logging
logger.addHandler(fh)           # add filehandle to logger

# Logger: create console handle
ch = logging.StreamHandler()
ch.setFormatter(formatter)
ch.setLevel(logging.WARNING)    # set logging level for consol
logger.addHandler(ch)


# https://stackoverflow.com/a/30493366
parser = argparse.ArgumentParser()
parser.add_argument('-s',  '--single',     action='store_true', help='Runs the program loop only once')
parser.add_argument('-fw', '--fakewebcam', action='store_true', help='Use Fake webcam')
parser.add_argument('-d',   type=int,      action='store',      help='Specify Domain. 0 prod, 1 brandon c9, 2 nick c9. Default 0', default="0")
parser.add_argument('-cd',  type=str,      action='store',      help='Specify custom Domain. This overrides all other domain settings', default=None)
parser.add_argument('-npi', '--notpi',     action='store_true', help='Run as if this was not a raspberry pi. Disables GPIO reading', default="False")
parser.add_argument('-u', '--uuid',     action='store', help='Use supplied UUID5 instead of generated uuid', default=None)
args = parser.parse_args() # parse args
my_globals.NOT_PI = args.notpi
DOMAIN_INDEX = args.d
DOMAIN_CUSTOM = args.cd
SINGLE_RUN = args.single
FAKEWEBCAM = args.fakewebcam     # enable or disable fake webcam
UUID_CUSTOM = args.uuid          # custome uuid

from cover import fsm, gpio_cleanup, cover_schedule   # cover monitor module. Must be imported after NOT_PI has been set
import sensors     #sensors.py

# multi thread support
def run_threaded(job_func):
	job_thread = threading.Thread(target=job_func)
	job_thread.start()

# If I'm running you should see this periodically
def job_heartbeat():
    logging.info("I'm working. %s" % datetime.datetime.now())

# Save setting to file
def job_save_settings():
    my_globals.save_settings()
    
def job_cover_monitor():
    fsm()
    
def job_cover_schedule():
    cover_schedule()

# Read enviroment sensors
def job_sensors():
    logging.info("Getting Sensors")
    sensors.update()
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
    logging.debug ("timepic: %d" % (t1-t0))      # debugger
    remote_comm.pic_upload()

schedule.every(30).seconds.do(job_heartbeat)
schedule.every(15).minutes.do(remote_comm.register)   # periodic re-register device with webserver
schedule.every(2).seconds.do(job_upload_status)
schedule.every(30).seconds.do(job_sensors)
schedule.every(7).seconds.do(job_webcam)
schedule.every(2).seconds.do(job_cover_monitor)
schedule.every(10).seconds.do(job_cover_schedule)
schedule.every(2).minutes.do(job_save_settings)


#function Deff

def initialize():
    # Test if using a custom uuid and validate it. else use hardware uuid
    if (UUID_CUSTOM == None):
        generate_uuid()                 # generate uuid from hardware
    else:
        if is_valid_uuid(UUID_CUSTOM):
            print ("Custom UUID is: %s" % UUID_CUSTOM)
            my_globals.settings["uuid"] = UUID_CUSTOM
        else:
            print ("Invalid Custom UUID: %r" % str(UUID_CUSTOM))
            print ("          Format is: 'xxxxxxxx-xxxx-4xxx-xxxx-xxxxxxxxxxxx'")
            print ("Exiting")
            exit()
    
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
    if path.isdir(my_globals.settings["storage_dir"]) == 0:   # if path to directory exists
        logging.warning ("Ramdisk does not exist. Using /tmp/smartsettia")
        # This is undesirable for sdcard wear and writing speed compared to a ramdisk
        if not os.path.exists("/tmp/smartsettia/"):     # test if tmp directory exists
            os.makedirs("/tmp/smartsettia/")            # create directory
        my_globals.settings["storage_dir"] = "/tmp/smartsettia/"

    # log file setup for program start
    file=open(my_globals.settings["storage_dir"] + "error.log","a")
    file.write(str(datetime.datetime.now()))
    file.write("\tProgram start\n-------------\n")
    file.close()    

    remote_comm.register()
    
    # run the cover montitor a few times to let it syncronize
    job_cover_monitor()
    job_cover_monitor()
    print ("--------------------------------------")


#Program start
print ("\nWelcome to Smartsettia!")
print ("Version: %s" % my_globals.version)
initialize()

# if single run run everything once
if SINGLE_RUN:
    print("Running single mode")
    schedule.run_all()      # run all jobs
    gpio_cleanup()
    exit()              # exit program

# watch dog setup.
# move to better spot later
# https://www.freedesktop.org/software/systemd/man/sd_notify.html#
# sdnotify: https://github.com/bb4242/sdnotify
import sdnotify
n = sdnotify.SystemdNotifier()
n.notify("READY=1")

# https://docs.python.org/2/library/signal.html
import signal

def signal_term_handler(signal, frame):
    print ('Recived signal: ', str(signal))
    #print ('got SIGTERM')
    n.notify("STOPPING=1")
    gpio_cleanup()
    exit(0)
    
while True and not SINGLE_RUN:
    schedule.run_pending()
    try:
        time.sleep(0.1)
    except KeyboardInterrupt as e:
        print("\nProgram exited by keyboard interrupt")
        n.notify("STOPPING=1")
        gpio_cleanup()
        exit()
    
    # watchdog
    try:
        n.notify("WATCHDOG=1")
    except Exception as e:
        print ("Error with watchdog: ", e)
        exit()  # debugging
    
    # test if program recieved a terminate command
    signal.signal(signal.SIGHUP , signal_term_handler) # 1
    signal.signal(signal.SIGINT , signal_term_handler) # 2
    signal.signal(signal.SIGQUIT, signal_term_handler) # 3
    signal.signal(signal.SIGABRT, signal_term_handler) # 6
    signal.signal(signal.SIGTERM, signal_term_handler) # 15