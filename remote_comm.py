# https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=4&cad=rja&uact=8&ved=0ahUKEwi38Ljt_6rWAhUJ1mMKHeeuC4kQFghAMAM&url=http%3A%2F%2Fwww.pythonforbeginners.com%2Fpython-on-the-web%2Fhow-to-use-urllib2-in-python
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
    data = {"empty":"nope"}
    print "Data is: ", data

    url = "http://echo.jsontest.com/key/values/one/two"

    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(req, json.dumps(data))
    print "Response is: ", response.info()
    print "Data is: ", data
