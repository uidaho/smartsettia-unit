#!/usr/bin/python
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
args = parser.parse_args() # parse args
single_run = args.s

def job_heartbeat():
    print("I'm working...")

def job_sensors():
    print("Getting Sensors..")
    sensors.update()
    print "\ttemp: %d, cpu_temp: %d" %(my_globals.sensor_dat["Temperature"], my_globals.sensor_dat["cpu_temp"])

def job_webcam():
    t0 = int(round(time.time() * 1000)) # debugger
    webcam.get_Picture()
    t1 = int(round(time.time() * 1000)) # debugger
    #print "timepic: %d" % (t1-t0)      # debugger
    remote_comm.pic_upload()

def job_remote_comm():
    print "remote communication"
    remote_comm.remote_send()


schedule.every(20).seconds.do(job_heartbeat)
schedule.every(10).seconds.do(job_sensors)
schedule.every(3).seconds.do(job_webcam)
#communicate with webserver - receive
#communicate with webserver - send
#schedule.every(5).seconds.do(job_remote_comm)
#garage door monitor
#webserver


#function Deff

def initialize():
    generate_uuid()
    remote_comm.register()
    #remote_comm.pic_upload()


#Program start
print "Welcome to Smartsettia!"
initialize()
while True and not single_run:
    schedule.run_pending()
    time.sleep(0.1)
