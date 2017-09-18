# https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=4&cad=rja&uact=8&ved=0ahUKEwi38Ljt_6rWAhUJ1mMKHeeuC4kQFghAMAM&url=http%3A%2F%2Fwww.pythonforbeginners.com%2Fpython-on-the-web%2Fhow-to-use-urllib2-in-python
import my_globals   # smartsettia globals
import json
import requests    # need to install


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
    data ={"uuid": "aa2c0776-9b44-13e7-abc4-cec278b6b50a", "challenge": "temppass"}
    #print "Data is: ", data        # debugger

    url = my_globals.settings["server_reg_addr"]
    headers = {'content-type': 'application/json'}

    try:
        try:
            req = requests.post(url, headers=headers, json=data)
        except:
            print "remote_comm:register:Error sending request"
        print "-------------"
        try:
            file=open("request_register.log","w")
            #file.write(request.status_code)
            file.write(req.text)
            file.close()
        except Exception as e:
            #raise
            print "remote_comm:register:Error writing to log"
            print e
        #try:
            #print req.status_code      # debugger
            #print req.text             # debugger
            #print "-------------"
        #except:
            #print "remote_comm:register:Error printing response"
        try:
            rtndata = req.json()
            rtndata2= rtndata["data"]
            #print "rtndata: ", rtndata     # debugger
            print "-------------"
            #print "rtndata2: ", rtndata2   # debugger
            print "Response code: ", req.status_code
            print "Token: ", rtndata2["token"]
            print "Name: ", rtndata2["name"]
        except:
            print "remote_comm:register:Error converting json"
    except:
        print "remote_comm:register:Error"
