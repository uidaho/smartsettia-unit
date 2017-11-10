# https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=4&cad=rja&uact=8&ved=0ahUKEwi38Ljt_6rWAhUJ1mMKHeeuC4kQFghAMAM&url=http%3A%2F%2Fwww.pythonforbeginners.com%2Fpython-on-the-web%2Fhow-to-use-urllib2-in-python
import time
from datetime import datetime
import os.path
import json
import requests
import my_globals   # smartsettia globals
from my_globals import settings
from helper_lib import print_error, print_log

headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

show_logging = 0        # flag if logs are shown in terminal


def status_update():
    print ("\n--- Uploading Status -----------------")
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
        print ("Overriding server command to %s" % payload["server_command"])
        payload["cover_command"] = payload["server_command"]
        my_globals.status["server_override"] = False   # reset back to false
    else:
        del payload["server_command"]       # only deleting this entry from payload. my_globals will still exist
    
    print ("\tjson dmp: ", json.dumps(payload)) # debugger

    # Debugging Code
    print ("Device ID: %d" % my_globals.settings["id"])    # because I'm tired of scrolling up to registration output for id
    print ("\tCover status:  %s" % payload["cover_status"])
    print ("\tError message: %r" % payload["error_msg"])
    
    #print_log("remote:status_update", url, show_logging)

    try:
        try:  # Send the request
            req = requests.post(url,headers=headers, json=payload, timeout=(3.05, 27))
        except Exception as e:
            print ("remote_comm:status_update:Error sending request")
            print ("\t", e)
        try:  # log raw response to rile
            file=open(my_globals.settings["storage_dir"] +"request_status_update.log","a")
            # The [:-3] truncates the last 3 characters of the string which is used cut out some microsecond digits
            file.write("\n\n" + str(datetime.now())[:-3] + "\n")
            file.write(str(req.status_code) + "\n")
            if req.status_code == 503:
                file.write("Server unavailable")
            else:
                file.write(req.text)
            file.close()
        except Exception as e:
            #raise
            print ("remote_comm:status_update:Error writing to log")
            print (e)

        print ("Response code: ", req.status_code)

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
                #print "rtndata: ", rtndata     # debugger
                my_globals.status['server_command'] = rtndata["data"]["cover_command"]
                print ("server command: ", my_globals.status['server_command'])

                # Convert the time string from server into a time object for HH:MM
                #new_cover_time_open  = datetime.strptime(rtndata["data"]["open_time"],  '%H:%M').time()
                #new_cover_time_close = datetime.strptime(rtndata["data"]["close_time"], '%H:%M').time()
                new_cover_time_open  = rtndata["data"]["open_time"]
                new_cover_time_close = rtndata["data"]["close_time"]
                # test if values changed
                if (new_cover_time_open != settings['cover_time_open']):
                    my_globals.settings['cover_time_open']  = new_cover_time_open
                    print ("\tCover time open changed to %s." % my_globals.settings["cover_time_open"])
                    
                if (new_cover_time_close != settings['cover_time_close']):
                    my_globals.settings['cover_time_close'] = new_cover_time_close
                    print ("\tCover time close changed to %s." % my_globals.settings["cover_time_close"])
                    
                print ("open %s\tclose %s" % (my_globals.settings['cover_time_open'], my_globals.settings['cover_time_close']))

                # update job rates
                # do in main?

            except Exception as e:
                print ("remote_comm:status_update:Error converting json")
                print (e)
        # test status code to determin if we were Successful
        if req.status_code == 201:
            print ("Status Update Successful")
        else:
            print ("\tstatus_update failed: Responce code: ", req.status_code)
            print ("\tURL: ", url)                      # debugger
            print ("\tHeaders: ", headers)              # debugger
            print ("\tjson dmp: ", json.dumps(payload)) # debugger
    except:
        print ("remote_comm:status_update:General Error")
    print ("--------------------------------------")
    # END of status_update


def sensor_upload():
    print ("\n--- Uploading Sensor Data-------------")
    global headers
    # setup the data
    url = my_globals.settings["server_sensor_addr"]
    payload = {}                             # initialize variable
    payload["uuid"]  = my_globals.settings["uuid"]      # add uuid
    payload["token"] = my_globals.settings["token"]     # add token
    payload.update(my_globals.sensor_data)      # add in sensor_dat dictionary

    #print_log("remote:sensor_upload", url, show_logging)

    try:
        try:  # Send the request
            req = requests.post(url,headers=headers, json=payload, timeout=(3.05, 27))
        except Exception as e:
            print ("remote_comm:sensor_upload:Error sending request")
            print ("\t", e)
        try:  # log raw response to rile
            file=open(my_globals.settings["storage_dir"] +"request_sensor_upload.log","a")
            file.write("\n\n" + str(datetime.now())[:-3] + "\n")
            file.write(str(req.status_code) + "\n")
            if req.status_code == 503:
                file.write("Server unavailable")
            else:
                file.write(req.text)
            file.close()
        except Exception as e:
            #raise
            print ("remote_comm:sensor_upload:Error writing to log")
            print (e)

        print ("Response code: ", req.status_code)
        try:  # parse returned datea
            rtndata = req.json()
            rtndata2= rtndata["data"]
            #print "rtndata: ", rtndata     # debugger
            #print "rtndata2: ", rtndata2   # debugger

        except Exception as e:
            print ("remote_comm:sensor_upload:Error converting json")
            print (e)
        # test status code to determin if we were Successful
        if req.status_code == 200 or req.status_code == 201:
            print ("Sensor Upload Successful")
        elif req.status_code == 422:
            print ("Unprocessable Entity. Re-registering")
            register()
        else:
            print ("sensor_upload failed: Responce code: ", req.status_code)
            # Debugging Code
            print ("\tURL: ", url)                      # debugger
            print ("\tHeaders: ", headers)              # debugger
            print ("\tjson dmp: ", json.dumps(payload)) # debugger
    except:
        print ("remote_comm:sensor_upload:General Error")
    print ("--------------------------------------")
    #END of sensor_upload


def register():
    print ("\n--- Registering Device ---------------")
    global headers
    url = my_globals.settings["server_reg_addr"]
    payload = {}
    payload["uuid"] = my_globals.settings["uuid"]
    payload["challenge"] = my_globals.settings["challenge"]

    #print_log("remote:register", url, show_logging)

    try:
        try:
            req = requests.post(url, headers=headers, data=json.dumps(payload), timeout=(3.05, 27))
        except:
            print ("remote_comm:register:Error sending request")
        try:
            file=open(my_globals.settings["storage_dir"] +"request_register.log","a")
            file.write("\n\n" + str(datetime.now())[:-3] + "\n")
            file.write(str(req.status_code) + "\n")
            if req.status_code == 503:
                file.write("Server unavailable")
            else:
                file.write(req.text)
            file.close()
        except Exception as e:
            #raise
            print ("remote_comm:register:Error writing to log")
            print (e)

        print ("Response code: ", req.status_code)
        #print req.text
        try:
            rtndata = req.json()
            rtndata2= rtndata["data"]
            #print "rtndata: ", rtndata     # debugger
            #print ("rtndata2: ", rtndata2)   # debugger
            print ("Token: ", rtndata2["token"])
            my_globals.settings["token"] = rtndata2["token"]  # set token to response token
            print ("Name:  ", rtndata2["name"])
            my_globals.settings["name"] = rtndata2["name"]  # set token to response token
            print ("ID:    ", rtndata2["id"])
            my_globals.settings["id"] = rtndata2["id"]

        except Exception as e:
            print ("remote_comm:register:Error converting json")
            print (e)

        if req.status_code == 200 or req.status_code == 201:
            print ("Registration Successful")
        else:
            print ("Registration failed: Responce code: ", req.status_code)
            print ("\tURL:  ", url)                     # debugger
            print ("\tUUID: ", payload["uuid"])         # debugger
            print ("\tHeaders: ", headers)              # debugger
            print ("\tjson dmp: ", json.dumps(payload)) # debugger
    except:
        print ("remote_comm:register:General Error")
    print ("--------------------------------------")
    # END of register


def pic_upload():
    print ("--- Uploading Picture ----------------")
    # first check if file exists
    image = my_globals.settings["storage_dir"] + my_globals.settings["img_name"]
    if os.path.isfile(image) == 0:           # if path to file exists
        print ("Image does not exist. Skipping upload")
        print ("--------------------------------------")
        return

    ## upload picture
    # setup the data
    headers = {'Accept': 'application/json'}
    url = my_globals.settings["server_img_addr"]
    payload = {}
    payload["uuid"] = ('', str(my_globals.settings["uuid"]))
    payload["token"] = ('', str(my_globals.settings["token"]))
    files= {"image": open(my_globals.settings["storage_dir"] + my_globals.settings["img_name"],'rb')}


    #print_log("remote:webcam", url, show_logging)
    #print ("-------------")

    try:
        try:  # Send the request
            req = requests.post(url,headers=headers, files=files, data=payload, timeout=(3.05, 27))
        except Exception as e:
            print ("remote_comm:webcam:Error sending request")
            print ("\t", e)
        try:  # log raw response to rile
            file=open(my_globals.settings["storage_dir"] +"request_webcam.log","a")
            file.write("\n\n" + str(datetime.now())[:-3] + "\n")
            file.write(str(req.status_code) + "\n")
            if req.status_code == 503:
                file.write("Server unavailable")
            else:
                file.write(req.text)
            file.close()
        except Exception as e:
            #raise
            print ("remote_comm:webcam:Error writing to log")
            print (e)

        print ("Response code: ", req.status_code)
        try:  # parse returned datea
            rtndata = req.json()
            rtndata2= rtndata["data"]
            #print "rtndata: ", rtndata     # debugger
            #print "rtndata2: ", rtndata2   # debugger

        except Exception as e:
            print ("remote_comm:webcam:Error converting json")
            print (e)
        # test status code to determin if we were Successful
        if req.status_code == 200 or req.status_code == 201:
            print ("Webcam upload Successful")
        else:
            print ("Webcam upload failed: Responce code: ", req.status_code)
            # Debugging Code
            print ("\tImage name: ", image)             # debugger
            print ("\tURL: ", url)                      # debugger
            print ("\tHeaders: ", headers)              # debugger
            print ("\tjson dmp: ", json.dumps(payload)) # debugger
    except:
        print ("remote_comm:webcam:General Error")
    print ("--------------------------------------")
    #END of pic_upload
