import schedule
import time
import sensors #sensors.py


def job_heartbeat():
    print("I'm working...")

def job_sensors():
    print("Getting Sensors..")
    temperature = sensors.getTemp()
    sysTemp = sensors.getSysTemp()
    print "temp: %d, sysTemp: %d" %(temperature, sysTemp)


schedule.every(20).seconds.do(job_heartbeat)
#schedule.every(10).seconds.do(job2,"hello")
schedule.every(5).seconds.do(job_sensors)

while True:
    schedule.run_pending()
    time.sleep(1)
