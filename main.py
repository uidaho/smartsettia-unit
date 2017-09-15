#!/usr/bin/python
import time
import schedule    # scheduler library
import sensors     #sensors.py
import webcam      # webcam module
import my_globals  # global variables

def job_heartbeat():
    print("I'm working...")

def job_sensors():
    print("Getting Sensors..")
    sensors.update()
    print "\ttemp: %d, sysTemp: %d" %(my_globals.sensor_dat["Temp"], my_globals.sensor_dat["SysTemp"])

def job_webcam():
    webcam.get_Picture()


schedule.every(20).seconds.do(job_heartbeat)
schedule.every(2).seconds.do(job_sensors)
#schedule.every(1).seconds.do(job_webcam)
#communicate with webserver - receive
#communicate with webserver - send
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
    SN = getserial()


#Program start
print "Welcome to Smartsettia!"
initialize()
print "SN=" + SN
while True:
    schedule.run_pending()
    time.sleep(0.1)
