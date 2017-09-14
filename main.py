#!/usr/bin/python
import schedule
import time
import sensors #sensors.py
import webcam



def job_heartbeat():
    print("I'm working...")

def job_sensors():
    print("Getting Sensors..")
    temperature = sensors.getTemp()
    sysTemp = sensors.getSysTemp()
    print "temp: %d, sysTemp: %d" %(temperature, sysTemp)

def job_webcam():
    webcam.getPicture()


schedule.every(20).seconds.do(job_heartbeat)
schedule.every(5).seconds.do(job_sensors)
#schedule.every(1).seconds.do(job_webcam)

while True:
    schedule.run_pending()
    time.sleep(0.1)
