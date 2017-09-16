import my_globals   # smartsettia globals
import json
import urllib2


def remote_send():
    data = my_globals.sensor_dat
    print "Data is: ", data

    url = "http://smartsettia.com/api"

    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(req, json.dumps(data))
