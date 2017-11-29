# This file handles all jobs and job scheduling
# Each job has:
#   * scheduler to set its rate
#   * the job function itself

import logging
import time
import datetime
import threading
import schedule
import my_globals
import webcam
import remote_comm
#from remote_comm import register   # importing this way to avoid circular includes
import sensors          # TODO this may cause more timming issues
from cover import fsm, cover_schedule


# multi thread support
def run_threaded(job_func):
	job_thread = threading.Thread(target=job_func)
	job_thread.start()



# status
def schedule_job_status():
    rate = my_globals.settings["job_server_status_sec"]
    logging.info("Schedualing status job for every %d seconds" % rate)
    schedule.clear("status")
    schedule.every(rate).seconds.do(job_upload_status).tag("status")
    #time.sleep(3)

# send status to server
def job_upload_status():
    remote_comm.status_update()



# sensors
def schedule_job_sensors():
    rate = my_globals.settings["job_server_sensors_sec"]
    logging.info("Schedualing sensors job for every %d seconds" % rate)
    schedule.clear("sensors")
    schedule.every(rate).seconds.do(job_sensors).tag("sensors")
    #time.sleep(3)

# Read enviroment sensors
def job_sensors():
    logging.info("Getting Sensors")
    sensors.update()
    remote_comm.sensor_upload()



FAKEWEBCAM = 1
# webcam
def schedule_job_webcam():
    rate = my_globals.settings["job_webcam_sec"]
    logging.info("Schedualing webcam job for every %d seconds" % rate)
    schedule.clear("webcam")
    schedule.every(rate).seconds.do(job_webcam).tag("webcam")              # non-threaded
    #schedule.every(rate).seconds.do(run_threaded, job_webcam).tag("webcam") # threaded
    #time.sleep(3)
    
# take a picture
def job_webcam():
    t0 = int(round(time.time() * 1000)) # debugger
    webcam.get_Picture(FAKEWEBCAM)      # get picture function with option fake bool
    t1 = int(round(time.time() * 1000)) # debugger
    logging.debug ("timepic: %d" % (t1-t0))      # debugger
    remote_comm.pic_upload()




# cover monitor
def job_cover_monitor():
    fsm()

def job_cover_schedule():
    cover_schedule()

# Save setting to file
def job_save_settings():
    my_globals.save_settings()
    
# If I'm running you should see this periodically
def job_heartbeat():
    logging.info("I'm working. %s" % datetime.datetime.now())


# Schedule jobs that are hard coded times
schedule.every(30).seconds.do(job_heartbeat)
schedule.every(15).minutes.do(remote_comm.register)   # periodic re-register device with webserver
schedule.every(2).seconds.do(job_cover_monitor)
schedule.every(2).minutes.do(job_save_settings)
schedule.every(10).seconds.do(job_cover_schedule)

# Reference: Jobs that are dynamically schedualed
# * job_status
# * job sensors
# * job webcam