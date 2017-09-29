#!/usr/bin/python3
import time
import schedule    # scheduler library
import sensors     #sensors.py
import webcam      # webcam module
import my_globals  # global variables
import remote_comm # server communication module
import argparse    # argument parsing
from helper_lib import print_error, print_log, generate_uuid


# Global Vars
single_run = 0

# https://stackoverflow.com/a/30493366
parser = argparse.ArgumentParser()
parser.add_argument('-s', action='store_true', help='Runs the program loop only once')
parser.add_argument('-fw',action='store_true', help='Use Fake webcam')
args = parser.parse_args() # parse args
SINGLE_RUN = args.s
FAKEWEBCAM = args.fw     # enable or disable fake webcam

print ("Using fake webcam: ", args.fw)

# If I'm running you should see this periodically
def job_heartbeat():
    print("I'm working...")

# Save setting to file
def job_save_settings():
    my_globals.save_settings()

# Read enviroment sensors
def job_sensors():
    print("Getting Sensors..")
    sensors.update()
    print ("\ttemp: %d, cpu_temp: %d" %(my_globals.sensor_dat["Temperature"], my_globals.sensor_dat["cpu_temp"]))

# send status to server
def job_upload_status():
    print ("Uploading status")
    remote_comm.status_update()

# take a picture
def job_webcam():
    t0 = int(round(time.time() * 1000)) # debugger
    webcam.get_Picture(FAKEWEBCAM)      # get picture function with option fake bool
    t1 = int(round(time.time() * 1000)) # debugger
    #print "timepic: %d" % (t1-t0)      # debugger
    remote_comm.pic_upload()

schedule.every(20).seconds.do(job_heartbeat)
schedule.every(60).seconds.do(job_save_settings)
schedule.every(10).seconds.do(job_sensors)
schedule.every(3).seconds.do(job_webcam)
#schedule.every(5).seconds.do(job_upload_status)
#schedule.every(5).seconds.do(job_upload_sensors)
#schedule.every(5).seconds.do(job_upload_webcam)   # TODO to separate webcam upload, or not
#garage door monitor
#webserver


#function Deff

def initialize():
    generate_uuid()                 # generate uuid from hardware
    my_globals.load_settings()      # load settings from file
    remote_comm.register()          # register device with webserver


#Program start
print ("Welcome to Smartsettia!")
initialize()
while True and not SINGLE_RUN:
    schedule.run_pending()
    time.sleep(0.1)
