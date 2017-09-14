#!/usr/bin/python
import schedule
import time
import sensors #sensors.py
import webcam


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


def job_heartbeat():
    print("I'm working...")

def job_sensors():
    print("Getting Sensors..")
    sensor_dat = sensors.update()
    #print "temp: %d, sysTemp: %d" %(temperature, sysTemp)

def job_webcam():
    webcam.get_Picture()


schedule.every(20).seconds.do(job_heartbeat)
schedule.every(5).seconds.do(job_sensors)
#schedule.every(1).seconds.do(job_webcam)

# Global Vars
SN = "NOTSET_000000000"

#function Deff

def initialize():
    SN = getserial()


#Program start
print "Welcome to Smartsettia!"
initialize()
print SN
while True:
    schedule.run_pending()
    time.sleep(0.1)
