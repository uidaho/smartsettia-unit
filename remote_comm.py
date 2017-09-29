# https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=4&cad=rja&uact=8&ved=0ahUKEwi38Ljt_6rWAhUJ1mMKHeeuC4kQFghAMAM&url=http%3A%2F%2Fwww.pythonforbeginners.com%2Fpython-on-the-web%2Fhow-to-use-urllib2-in-python
import time
import os.path
import json
import requests
import my_globals   # smartsettia globals
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

    # Debugging Code
    #print ("Data is: ", payload)              # debugger
    #print (payload.items())                   # debugger
    #print (url)                               # debugger
    #print ("json dmp: ", json.dumps(payload)) # debugger
    #print ("headers: ", headers)              # debugger
    print_log("remote:status_update", url, show_logging)
    #print ("-------------")

    try:
        try:  # Send the request
            req = requests.post(url,headers=headers, json=payload)
        except Exception as e:
            print ("remote_comm:status_update:Error sending request")
            print ("\t", e)
        try:  # log raw response to rile
            file=open("request_status_update.log","a")
            file.write("\n\n" + str(time.time()) + "\n")
            file.write(str(req.status_code) + "\n")
            file.write(req.text)
            file.close()
        except Exception as e:
            #raise
            print ("remote_comm:status_update:Error writing to log")
            print (e)

        print ("Response code: ", req.status_code)
        try:  # parse returned datea
            rtndata = req.json()
            rtndata2= rtndata["data"]
            #print "rtndata: ", rtndata     # debugger
            #print "rtndata2: ", rtndata2   # debugger

        except Exception as e:
            print ("remote_comm:status_update:Error converting json")
            print (e)
        # test status code to determin if we were Successful
        if req.status_code == 200 or req.status_code == 201:
            print ("Status Update Successful")
        else:
            print ("status_update failed: Responce code: ", req.status_code)
    except:
        print ("remote_comm:status_update:General Error")
    print ("--------------------------------------")
    # END of status_update


def sensor_upload():
    print ("\n--- Uploading Sensor Data-------------")
    global headers
    # setup the data
    url = my_globals.settings["server_update_addr"]
    payload = {}                             # initialize variable
    payload["uuid"]  = my_globals.settings["uuid"]      # add uuid
    payload["token"] = my_globals.settings["token"]     # add token
    payload.update(my_globals.sensor_dat)      # add in sensor_dat dictionary
    
    # this should be removed when status is separated server side
    # or.. it could stay. TODO needs discusion
    payload.update(my_globals.status)          # add in status dictionary 

    # Debugging Code
    #print ("Data is: ", payload)              # debugger
    #print (payload.items())                   # debugger
    #print (url)                               # debugger
    #print ("json dmp: ", json.dumps(payload)) # debugger
    #print ("headers: ", headers)              # debugger
    print_log("remote:sensor_upload", url, show_logging)
    #print ("-------------")

    try:
        try:  # Send the request
            req = requests.post(url,headers=headers, json=payload)
        except Exception as e:
            print ("remote_comm:sensor_upload:Error sending request")
            print ("\t", e)
        try:  # log raw response to rile
            file=open("request_sensor_upload.log","a")
            file.write("\n\n" + str(time.time()) + "\n")
            file.write(str(req.status_code) + "\n")
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
        else:
            print ("sensor_upload failed: Responce code: ", req.status_code)
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
    #print ("Data is: ", payload)              # debugger

    print ("URL:  ", url)                      # debugger
    #print ("json dmp: ", json.dumps(payload)) # debugger
    #print ("headers: ", headers)
    print_log("remote:register", url, show_logging)
    #print "-------------"

    try:
        try:
            req = requests.post(url, headers=headers, data=json.dumps(payload))
        except:
            print ("remote_comm:register:Error sending request")
        try:
            file=open("request_register.log","a")
            file.write("\n\n" + str(time.time()) + "\n")
            file.write(str(req.status_code) + "\n")
            file.write(req.text)
            file.close()
        except Exception as e:
            #raise
            print ("remote_comm:register:Error writing to log")
            print (e)

        print ("--- Registration return ---")
        print ("Response code: ", req.status_code)
        #print req.text
        try:
            rtndata = req.json()
            rtndata2= rtndata["data"]
            #print "rtndata: ", rtndata     # debugger
            print ("rtndata2: ", rtndata2)   # debugger
            print ("Token: ", rtndata2["token"])
            my_globals.settings["token"] = rtndata2["token"]  # set token to response token
            print ("Name: ", rtndata2["name"])
            my_globals.settings["name"] = rtndata2["name"]  # set token to response token

        except Exception as e:
            print ("remote_comm:register:Error converting json")
            print (e)

        if req.status_code == 200 or req.status_code == 201:
            print ("Registration Successful")
        else:
            print ("Registration failed: Responce code: ", req.status_code)
    except:
        print ("remote_comm:register:General Error")
    print ("--------------------------------------")
    # END of register


def pic_upload():
    print ("--- Uploading Picture ----------------")
    # first check if file exists
    image = my_globals.settings["img_dir"] + my_globals.settings["img_name"]
    print ("Image name: ", image)
    if os.path.isfile(image) == 0:           # if path to file exists
        print ("Image does not exist. Skipping upload")
        return

    ## upload picture
    # setup the data
    headers = {'Accept': 'application/json'}
    url = my_globals.settings["server_img_addr"]
    payload = {}
    payload["uuid"] = ('', str(my_globals.settings["uuid"]))
    payload["token"] = ('', str(my_globals.settings["token"]))
    files= {"image": open(my_globals.settings["img_dir"] + my_globals.settings["img_name"],'rb')}

    # Debugging Code
    #print ("Data is: ", payload)              # debugger
    #print (payload.items())                   # debugger
    #print (url)                               # debugger
    #print ("json dmp: ", json.dumps(payload)) # debugger
    #print ("headers: ", headers)              # debugger
    print_log("remote:webcam", url, show_logging)
    #print ("-------------")

    try:
        try:  # Send the request
            req = requests.post(url,headers=headers, files=files, data=payload)
        except Exception as e:
            print ("remote_comm:webcam:Error sending request")
            print ("\t", e)
        try:  # log raw response to rile
            file=open("request_webcam.log","a")
            file.write("\n\n" + str(time.time()) + "\n")
            file.write(str(req.status_code) + "\n")
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
    except:
        print ("remote_comm:webcam:General Error")
    print ("--------------------------------------")
    #END of pic_upload