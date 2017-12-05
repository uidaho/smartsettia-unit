# https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=4&cad=rja&uact=8&ved=0ahUKEwi38Ljt_6rWAhUJ1mMKHeeuC4kQFghAMAM&url=http%3A%2F%2Fwww.pythonforbeginners.com%2Fpython-on-the-web%2Fhow-to-use-urllib2-in-python
import time
from datetime import datetime
import os.path
import json
import requests
import my_globals   # smartsettia globals
from my_globals import settings
import logging

headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

# switch to enable/disable file logging of post requests
# logs are stored to global storage location which is located on the ramdisk
enable_file_logging = False


def status_update():
    logging.info("--- Uploading Status -----------------")
    global headers
    # setup the data
    url = my_globals.settings["server_status_addr"]
    payload = {}                             # initialize variable
    payload["uuid"]  = my_globals.settings["uuid"]      # add uuid
    payload["token"] = my_globals.settings["token"]     # add token
    payload.update(my_globals.status)        # add in status dictionary
    
    # server command, if sent, will override that variable server side
    # server_override if true will not delete 
    # server_command is the local variable, cover_command is the server variable
    if (my_globals.status["server_override"] == True):
        logging.debug ("Overriding server command to %s" % payload["server_command"])
        payload["cover_command"] = payload["server_command"]
        my_globals.status["server_override"] = False   # reset back to false
    else:
        del payload["server_command"]       # only deleting this entry from payload. my_globals will still exist
    
    logging.debug ("json dmp: %r" % json.dumps(payload)) # debugger

    # Debugging Code
    logging.debug ("Device ID: %d" % my_globals.settings["id"])    # because I'm tired of scrolling up to registration output for id
    logging.debug ("Cover status:  %s" % payload["cover_status"])
    logging.debug ("Error message: %r" % payload["error_msg"])
    
    try:
        try:  # Send the request
            req = requests.post(url,headers=headers, json=payload, timeout=(3.05, 27))
        except Exception as e:
            logging.error ("status_update:Error sending request")
            logging.debug (e)
        if enable_file_logging:
            try:  # log raw response to rile
                file=open(my_globals.settings["storage_dir"] +"request_status_update.log","a")
                # The [:-3] truncates the last 3 characters of the string which is used cut out some microsecond digits
                file.write("\n\n" + str(datetime.now())[:-3] + "\n")
                file.write(str(req.status_code) + "\n")
                if req.status_code == 503:
                    file.write("Server unavailable")
                #else:
                #    file.write(req.text[:2000])
                file.close()
            except Exception as e:
                #raise
                logging.error ("status_update:Error writing to log")
                logging.debug (e)

        logging.debug ("Response code: %s" % req.status_code)

        # parse returned data if successful post
        if req.status_code == 201:
            # clear error_msg
            my_globals.status["error_msg"] = None
            
            # remove server_command from status if exists
            if ("server_command" in my_globals.status):
                #print ("server_command exists and was sent. removing")
                del my_globals.status["server_command"]
                
            try:  # parse returned data
                rtndata = req.json()
                #logging.debug ("rtndata: %r" % rtndata)     # debugger can produce lots of logs
                my_globals.status['server_command'] = rtndata["data"]["cover_command"]
                logging.debug ("server command: %s" % my_globals.status['server_command'])

                new_cover_time_open  = rtndata["data"]["open_time"]
                new_cover_time_close = rtndata["data"]["close_time"]
                # test if values changed
                if (new_cover_time_open != settings['cover_time_open']):
                    my_globals.settings['cover_time_open']  = new_cover_time_open
                    logging.info ("Cover time open changed to %s." % my_globals.settings["cover_time_open"])
                    
                if (new_cover_time_close != settings['cover_time_close']):
                    my_globals.settings['cover_time_close'] = new_cover_time_close
                    logging.info ("Cover time close changed to %s." % my_globals.settings["cover_time_close"])
                    
                logging.info ("open %s\tclose %s" % (my_globals.settings['cover_time_open'], my_globals.settings['cover_time_close']))

                # job rates
                logging.debug("old update rate %d, type: %s" % (settings['job_server_status_sec'], type(settings['job_server_status_sec'])))
                new_job_status_rate  = rtndata['data']['update_rate']
                new_job_image_rate   = rtndata['data']['image_rate']
                new_job_sensor_rate  = rtndata['data']['sensor_rate']
                logging.debug("status: %r, image: %r, sensor: %r" % (new_job_status_rate, new_job_image_rate, new_job_sensor_rate))
                logging.debug("new update rate %d, type: %s" % (new_job_status_rate, type(new_job_status_rate)))
                
                # test if job rates are different from stored value. Reschedule if different
                import job_scheduling           # must be imported in this scope to avoid circular imports
                if (new_job_status_rate != my_globals.settings['job_server_status_sec']):
                    my_globals.settings['job_server_status_sec'] = new_job_status_rate
                    job_scheduling.schedule_job_status()
                    logging.debug("## post settings for status %d, type %s" % (my_globals.settings['job_server_status_sec'], type(my_globals.settings['job_server_status_sec'])))
                if (new_job_image_rate != my_globals.settings['job_webcam_sec']):
                    my_globals.settings['job_webcam_sec'] = new_job_image_rate
                    job_scheduling.schedule_job_webcam()
                if (new_job_sensor_rate != my_globals.settings['job_server_sensors_sec']):
                    my_globals.settings['job_server_sensors_sec'] = new_job_sensor_rate
                    job_scheduling.schedule_job_sensors()

            except Exception as e:
                logging.error ("status_update:Error converting json")
                logging.debug (e)

        # test status code to determin if we were Successful
        if req.status_code == 201:
            logging.info ("Status Update Successful")
        else:
            logging.debug ("status_update failed: Responce code: %s" % req.status_code)
            logging.debug ("URL: %s" % url)                      # debugger
            logging.debug ("Headers: %s" % headers)              # debugger
            logging.debug ("json dmp: %s" % json.dumps(payload)) # debugger
    except Exception as e:
        logging.error ("status_update:General Error")
        logging.debug(e)
    # END of status_update


def sensor_upload():
    logging.info ("--- Uploading Sensor Data-------------")
    global headers
    # setup the data
    url = my_globals.settings["server_sensor_addr"]
    payload = {}                             # initialize variable
    payload["uuid"]  = my_globals.settings["uuid"]      # add uuid
    payload["token"] = my_globals.settings["token"]     # add token
    payload.update(my_globals.sensor_data)      # add in sensor_dat dictionary


    try:
        try:  # Send the request
            req = requests.post(url,headers=headers, json=payload, timeout=(3.05, 27))
        except Exception as e:
            logging.error ("sensor_upload:Error sending request")
            logging.debug (e)
        if enable_file_logging:
            try:  # log raw response to rile
                file=open(my_globals.settings["storage_dir"] +"request_sensor_upload.log","a")
                file.write("\n\n" + str(datetime.now())[:-3] + "\n")
                file.write(str(req.status_code) + "\n")
                if req.status_code == 503:
                    file.write("Server unavailable")
                else:
                    file.write(req.text[:2000])
                file.close()
            except Exception as e:
                #raise
                logging.error ("sensor_upload:Error writing to log")
                logging.debug (e)

        logging.debug ("Response code: %s" % req.status_code)
        try:  # parse returned datea
            rtndata = req.json()
            rtndata2= rtndata["data"]
            #print "rtndata: ", rtndata     # debugger
            #print "rtndata2: ", rtndata2   # debugger

        except Exception as e:
            logging.error ("sensor_upload:Error converting json")
            logging.debug (e)
        # test status code to determin if we were Successful
        if req.status_code == 200 or req.status_code == 201:
            logging.info ("Sensor Upload Successful")
        elif req.status_code == 422:
            logging.warning ("Unprocessable Entity. Re-registering")
            register()
        elif req.status_code == 500:
            logging.warning ("Server error. Sleeping for 10 seconds")
            time.sleep(10)  # to slow the program to prevent several error posts in a short time
        else:
            logging.error ("sensor_upload failed: Responce code: %s" % req.status_code)
            # Debugging Code
            logging.debug ("\tURL: %s" % url)                      # debugger
            logging.debug ("\tHeaders: %s" % headers)              # debugger
            logging.debug ("\tjson dmp: $s" % json.dumps(payload)) # debugger
    except:
        logging.error ("sensor_upload:General Error")
    #END of sensor_upload


def register():
    logging.info ("--- Registering Device ---------------")
    global headers
    url = my_globals.settings["server_reg_addr"]
    payload = {}
    payload["uuid"] = my_globals.settings["uuid"]
    payload["challenge"] = my_globals.settings["challenge"]

    try:
        try:
            req = requests.post(url, headers=headers, data=json.dumps(payload), timeout=(3.05, 27))
        except:
            logging.error ("register:Error sending request")
        if enable_file_logging:
            try:
                file=open(my_globals.settings["storage_dir"] +"request_register.log","a")
                file.write("\n\n" + str(datetime.now())[:-3] + "\n")
                file.write(str(req.status_code) + "\n")
                if req.status_code == 503:
                    file.write("Server unavailable")
                else:
                    file.write(req.text[:2000]) # truncate the supper long error trace report
                file.close()
            except Exception as e:
                #raise
                logging.error ("register:Error writing to log")
                logging.debug (e)

        logging.debug ("Response code: %s" % req.status_code)
        #print req.text[:2000]
        try:
            rtndata = req.json()
            rtndata2= rtndata["data"]
            #print "rtndata: ", rtndata     # debugger
            #print ("rtndata2: ", rtndata2)   # debugger
            logging.info ("Token: %s" % rtndata2["token"])
            my_globals.settings["token"] = rtndata2["token"]  # set token to response token
            logging.info ("Name:  %s" % rtndata2["name"])
            my_globals.settings["name"] = rtndata2["name"]  # set token to response token
            logging.info ("ID:    %s" % rtndata2["id"])
            my_globals.settings["id"] = rtndata2["id"]

        except Exception as e:
            logging.error ("register:Error converting json")
            logging.debug (e)

        if req.status_code == 200 or req.status_code == 201:
            logging.info ("Registration Successful")
        else:
            logging.error ("Registration failed: Responce code: %r" % req.status_code)
            logging.debug ("URL:  %r" % url)                     # debugger
            logging.debug ("UUID: %r" % payload["uuid"])         # debugger
            logging.debug ("tHeaders: %r" % headers)              # debugger
            logging.debug ("json dmp: %r" % json.dumps(payload)) # debugger
    except:
        logging.error ("register:General Error")
    print ("--------------------------------------")
    # END of register


def pic_upload():
    logging.info ("--- Uploading Picture ----------------")
    # first check if file exists
    image = my_globals.settings["storage_dir"] + my_globals.settings["img_name"]
    if os.path.isfile(image) == 0:           # if path to file exists
        logging.warning ("Image does not exist. Skipping upload")
        return

    ## upload picture
    # setup the data
    headers = {'Accept': 'application/json'}
    url = my_globals.settings["server_img_addr"]
    payload = {}
    payload["uuid"] = ('', str(my_globals.settings["uuid"]))
    payload["token"] = ('', str(my_globals.settings["token"]))
    files= {"image": open(my_globals.settings["storage_dir"] + my_globals.settings["img_name"],'rb')}

    try:
        try:  # Send the request
            req = requests.post(url,headers=headers, files=files, data=payload, timeout=(3.05, 27))
        except Exception as e:
            logging.error ("webcam:Error sending request")
            logging.debug (e)
        try:  # log raw response to rile
            file=open(my_globals.settings["storage_dir"] +"request_webcam.log","a")
            file.write("\n\n" + str(datetime.now())[:-3] + "\n")
            file.write(str(req.status_code) + "\n")
            if req.status_code == 503:
                file.write("Server unavailable")
            else:
                file.write(req.text[:2000])
            file.close()
        except Exception as e:
            #raise
            logging.error ("webcam:Error writing to log")
            logging.debug (e)

        logging.debug ("Response code: %s" % req.status_code)
        try:  # parse returned datea
            rtndata = req.json()
            rtndata2= rtndata["data"]
            #print "rtndata: ", rtndata     # debugger
            #print "rtndata2: ", rtndata2   # debugger

        except Exception as e:
            logging.error ("webcam:Error converting json")
            logging.debug (e)
        # test status code to determin if we were Successful
        if req.status_code == 200 or req.status_code == 201:
            logging.info ("Webcam upload Successful")
        else:
            logging.error ("Webcam upload failed: Responce code: %r" % req.status_code)
            # Debugging Code
            logging.debug ("Image name: %r" % image)             # debugger
            logging.debug ("URL: %r" % url)                      # debugger
            logging.debug ("Headers: %r" % headers)              # debugger
            logging.debug ("json dmp: %r" % json.dumps(payload)) # debugger
    except:
        logging.error ("webcam:General Error")
    #END of pic_upload
