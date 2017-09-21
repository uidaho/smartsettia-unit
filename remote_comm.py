# https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=4&cad=rja&uact=8&ved=0ahUKEwi38Ljt_6rWAhUJ1mMKHeeuC4kQFghAMAM&url=http%3A%2F%2Fwww.pythonforbeginners.com%2Fpython-on-the-web%2Fhow-to-use-urllib2-in-python
import time
import my_globals   # smartsettia globals
import json
import requests
from helper_lib import print_error, print_log

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
    #print "json dmp: ", json.dumps(payload) # debugger
    print_log("remote:register", url, show_logging)
    #print "-------------"

    try:
        try:
            print "headers: ", headers
            print_error("remote_comm:reg", "test")
            req = requests.post(url, headers=headers, data=json.dumps(payload))
            print req.request.method
            #r= req.prepare()
            #print r
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
