#!/usr/bin/python
import time
import schedule    # scheduler library
import sensors     #sensors.py
import webcam      # webcam module
import my_globals  # global variables
import remote_comm # server communication module
import uuid

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

# Global Vars

#function Deff

def generate_uuid():
    # https://stackoverflow.com/questions/159137/getting-mac-address
    seed = uuid.getnode()       # returns 48bit value from MAC or rand number if not found
    uu = str(uuid.uuid5(uuid.NAMESPACE_URL, str(seed)))
    print "uuid: ", uu
    my_globals.settings["uuid"] = uu

def initialize():
    generate_uuid()
    remote_comm.register()


#Program start
print "Welcome to Smartsettia!"
initialize()
while True:
    schedule.run_pending()
    time.sleep(0.1)
