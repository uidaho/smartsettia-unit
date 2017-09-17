import my_globals   # smartsettia globals
import json
import urllib2
#import requests    # need to install


def remote_send():
    data = my_globals.sensor_dat
    print "Data is: ", data

    url = "http://smartsettia.com/api"

    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(req, json.dumps(data))


#alternative using requests
def remote_send2():
    data = my_globals.sensor_dat
    print "Data is: ", data

    url = "http://smartsettia.com/api"
    headers = {'content-type': 'application/json'}

    #response = requests.post(url, data=json.dumps(data),headers=headers)
    #print "Response: ", response

def remote_recv():
    data = {"one": "two","key":"value"}
    print "Data is: ", data

    url = "http://echo.jsontest.com/key/name"

    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(req, json.dumps(data))
    print "Response is: ", response
