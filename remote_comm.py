# https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=4&cad=rja&uact=8&ved=0ahUKEwi38Ljt_6rWAhUJ1mMKHeeuC4kQFghAMAM&url=http%3A%2F%2Fwww.pythonforbeginners.com%2Fpython-on-the-web%2Fhow-to-use-urllib2-in-python
import time
import os.path
import json
import requests
import my_globals   # smartsettia globals
from helper_lib import print_error, print_log

settings = my_globals.settings
headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

show_logging = 0        # flag if logs are shown in terminal


# using response
def r2():
    data = my_globals.sensor_dat #{"empty":"nope"}
    print "Data is: ", data

    #url = "http://echo.jsontest.com/key/values/one/two"
    #url = "https://smartsettia.com/api/ping "
    url = "http://nkren.net"
    headers = {'content-type': 'application/json'}

    try:
        #request = requests.post(url, headers=headers, params=data)
        req = requests.post(url, headers=headers, json=data)
        print req.headers
        print "-------------"
        file=open("request.log","w")
        file.write(req.text)
        file.close()
        print req.text
        print "-------------"
        try:
            print req.json()
        except:
            print "remote_comm:remote_recv:Error converting json"
    except:
        print "remote_comm:remote_recv:Error sending request"

def register():
    global headers
    url = my_globals.settings["server_reg_addr"]
    payload = {}
    payload["uuid"] = my_globals.settings["uuid"]
    payload["challenge"] = my_globals.settings["challenge"]
    #print "Data is: ", payload              # debugger

    #print url                               # debugger
    print "json dmp: ", json.dumps(payload) # debugger
    print_log("remote:register", url, show_logging)
    #print "-------------"

    try:
        try:
            print "headers: ", headers
            req = requests.post(url, headers=headers, data=json.dumps(payload))
        except:
            print "remote_comm:register:Error sending request"
        try:
            file=open("request_register.log","a")
            file.write("\n\n" + str(time.time()) + "\n")
            file.write(str(req.status_code) + "\n")
            file.write(req.text)
            file.close()
        except Exception as e:
            #raise
            print "remote_comm:register:Error writing to log"
            print e

        print req.status_code
        #print req.text
        try:
            rtndata = req.json()
            rtndata2= rtndata["data"]
            #print "rtndata: ", rtndata     # debugger
            print "-------------"
            #print "rtndata2: ", rtndata2   # debugger
            print "Response code: ", req.status_code
            print "Token: ", rtndata2["token"]
            my_globals.settings["token"] = rtndata2["token"]  # set token to response token
            print "Name: ", rtndata2["name"]
            my_globals.settings["name"] = rtndata2["name"]  # set token to response token

        except Exception as e:
            print "remote_comm:register:Error converting json"
            print e
        print "Registration Successful (not verified)"
        print "--------------------------------------"
    except:
        print "remote_comm:register:General Error"






def pic_upload():
    # first check if file exists
    test = os.path.isfile(settings["img_dir"] + settings["img_name"])
    if test == 1:
        print "Image exists"
    else:
        print "Image does not exist. Skipping upload"
        return

    # upload picture
    headers = {'Accept': 'application/json'}
    url = my_globals.settings["server_img_addr"]
    image = settings["img_dir"] + settings["img_name"]
    payload = {}
    #payload["uuid"] = my_globals.settings["uuid"]
    #payload["token"] = my_globals.settings["token"]
    #payload["uuid"] = ('', my_globals.settings["uuid"])
    #payload["token"] = ('',my_globals.settings["token"])
    payload["uuid"] = ('', "9dbc0776-9b44-11e7-abc4-cec278b6b50a")
    payload["token"] = ('',"u0tQGeyuGdikOOFWhfDfwxbR2Z7rTN9Hc5hZN1JHsg4uUfkTi8UUu5nh0XLm")
    payload.update({'image': open(settings["img_dir"] + settings["img_name"],'rb')})
    payload['image'] = open(image,'rb')

    print "Data is: ", payload              # debugger
    print payload.items()
    #print url                               # debugger
    #print "json dmp: ", json.dumps(payload) # debugger
    print_log("remote:webcam", url, show_logging)
    #print "-------------"

    try:
        try:
            print "headers: ", headers
            req = requests.post(url,headers=headers, files=payload)
        except Exception as e:
            print "remote_comm:webcam:Error sending request"
            print "\t", e
        try:
            file=open("request_webcam.log","a")
            file.write("\n\n" + str(time.time()) + "\n")
            file.write(str(req.status_code) + "\n")
            file.write(req.text)
            file.close()
        except Exception as e:
            #raise
            print "remote_comm:webcam:Error writing to log"
            print e

        print req.status_code
        try:
            rtndata = req.json()
            rtndata2= rtndata["data"]
            #print "rtndata: ", rtndata     # debugger
            print "-------------"
            #print "rtndata2: ", rtndata2   # debugger
            print "Response code: ", req.status_code
            #print "Token: ", rtndata2["token"]
            #my_globals.settings["token"] = rtndata2["token"]  # set token to response token
            #print "Name: ", rtndata2["name"]
            #my_globals.settings["name"] = rtndata2["name"]  # set token to response token

        except Exception as e:
            print "remote_comm:webcam:Error converting json"
            print e
        print "Webcam upload Successful (not verified)"
        print "--------------------------------------"
    except:
        print "remote_comm:webcam:General Error"
