# This file contains the global variables used in smartsettia
import json
version= "0.2.2"

# Note to concatonate dictionaries
# z = x.copy()
# z.update(y)

# Set domain being used
DOMAIN_INDEX = 2    # choose which domain. 0-2
DOMAIN =    ["https://smartsettia.com/",
            "https://smartsettia-backburn.c9users.io/",
            "https://smartsettia-nkrenowicz.c9users.io/"]

# set by arguments to disable GPIO
NOT_PI = False

sensor_data = {}    # declare variable. Done as dictionary so that this can be imported with dic.update()            
sensor_data["sensor_data"] = [
            { "name": "cpu",         "type": "cpu_temperature", "value": "0.00" },  # pi system temperature
            { "name": "light_in",    "type": "light",           "value": "0.00" },  # ambiant light sensor inside
            { "name": "light_out",   "type": "light",           "value": "0.00" },  # ambiant light sensor outside
            { "name": "temperature", "type": "temperature",     "value": "0.00" },
            { "name": "humidity",    "type": "humidity",        "value": "0.00" }
#           { "name": "moisture_01", "type": "moisture",        "value": "0.00" },
#           { "name": "moisture_02", "type": "moisture",        "value": "0.00" }
            ]

# possible cover_statuses
# cover_status = { open, close, opening, closing, locked, error }

# possible server commands
# server_command = { open, close, lock }
status =        {"cover_status": "closed",
                "server_command": "close",
                "error_msg": None
                }

settings =      {"name":"UnNamed",                          # Name of Device
                "uuid": "NOT_SET0-0000-0000-0000-000000000000",   # UUID V1
                "token": "none",      # post token key
                "id": -1,                                   # ID no. of the device
                "challenge": "temppass",                    # challenge
                "mac_address":"00:00:00:00:00:00",          # MAC address
                "server_reg_addr":    DOMAIN[DOMAIN_INDEX] + "api/register",
                "server_status_addr": DOMAIN[DOMAIN_INDEX] + "api/update",
                "server_sensor_addr": DOMAIN[DOMAIN_INDEX] + "api/sensor",
                "server_img_addr":    DOMAIN[DOMAIN_INDEX] + "api/image",
                "job_cover_monitor":1,                      # cover monitor run rate
                "job_save_settings":60,                     # save settings to file
                "job_sensors_sec"  :5,                      # job runs every x seconds
                "job_webcam_sec"   :2,                      # job runs every x seconds
                "job_server_status_sec" :1,                 # send device status job
                "job_server_sensors_sec":20,                # send device sensors job
                                                            # other jobs
                "cover_time_open":  "HH:MM:SS",             # open time
                "cover_time_close": "HH:MM:SS",             # close time
                "img_dir": "/mnt/ramdisk/",                 # directory where picture is saved
                "img_name": "webcam_img.jpg"
                }


def save_settings():
    print ("Saving settings")
    global settings
    # print settings         # debugger
    try:
        with open('config.json', 'w') as f:
            json.dump(settings, f)
    except Exception as e:
        print ("Save settings error ", e)


def load_settings():
    print ("Loading settings")
    global settings
    temp = {}
    try:
        with open('config.json', 'r') as f:
            temp = json.load(f)
    # except FileNotFoundError:
    #    print "config.json file not found. loading default settings"
    except Exception as e:
        print ("\tLoad settings error ", e)

    else:       # if file was found and all is good
        # print temp             # debugger
        if temp["uuid"] == settings["uuid"]:
            print ("\tUUID matches loaded settings - keeping")
            settings = temp     # set settings to loaded values

            # override loaded url's to match DOMAIN_INDEX
            update_url(DOMAIN[DOMAIN_INDEX])

        else:
            print ("\tUUID does not mach loaded settings - discarding")
            print ("\tUsing default settings")


def update_url(domain):
    global settings
    
    # ending '/' test. Add if missing
    mlen = len(domain) - 1
    if (domain[mlen] != '/'):
        domain = domain + '/'
    
    print ("Using domain %s" % domain)
    settings["server_reg_addr"]    = domain + "api/register"
    settings["server_status_addr"] = domain + "api/update"
    settings["server_sensor_addr"] = domain + "api/sensor"
    settings["server_img_addr"]    = domain + "api/image"
    print ("\tURL register: %s" % settings["server_reg_addr"])
    print ("\tURL status:   %s" % settings["server_status_addr"])
    print ("\tURL sensors:  %s" % settings["server_sensor_addr"])
    print ("\tURL image:    %s" % settings["server_img_addr"])