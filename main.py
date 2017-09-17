#!/usr/bin/python
import time
import schedule    # scheduler library
import sensors     #sensors.py
import webcam      # webcam module
import my_globals  # global variables
import remote_comm # server communication module

def job_heartbeat():
    print("I'm working...")

def job_sensors():
    print("Getting Sensors..")
    sensors.update()
    print "\ttemp: %d, cpu_temp: %d" %(my_globals.sensor_dat["Temperature"], my_globals.sensor_dat["cpu_temp"])

def job_webcam():
    webcam.get_Picture()

def job_remote_comm():
    print "remote communication"
    remote_comm.remote_send()


schedule.every(20).seconds.do(job_heartbeat)
schedule.every(5).seconds.do(job_sensors)
#(disabled) schedule.every(2).seconds.do(job_webcam)
#communicate with webserver - receive
#communicate with webserver - send
schedule.every(5).seconds.do(job_remote_comm)
#garage door monitor
#webserver

# Global Vars
SN = "NOTSET_000000000"


#function Deff

def getserial():
  # Extract serial from cpuinfo file
  #Example: 000000000000000d
  cpuserial = "NOTFOUND_0000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR_0000000000"
  return cpuserial


def initialize():
    global SN
    SN = getserial()


#Program start
print "Welcome to Smartsettia!"
initialize()
print "SN=" + SN
while True:
    schedule.run_pending()
    time.sleep(0.1)
