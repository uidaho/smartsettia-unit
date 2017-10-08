# This file contains the global variables used in smartsettia
import json
version= "0.1.0"

# Note to concatonate dictionaries
# z = x.copy()
# z.update(y)

# Set domain being used
DOMAIN_INDEX = 2    # choose which domain. 0-2
DOMAIN =    ["https://smartsettia.com/",
            "https://smartsettia-backburn.c9users.io/",
            "https://smartsettia-nkrenowicz.c9users.io/"]

sensor_dat =    {"capture_time":"YYYY-MM-DD HH:MM:SS",
                "light_in":-1,                      # ambiant light sensor inside
                "light_out":-1,                     # ambiant light sensor outside
                "limitsw_open": 0,                  # limit switch on open side
                "limitsw_close":-1,                 # limit switch on close side
                "cpu_temp":-1,                      # pi system temperature
                "temperature":-1,
                "humidity":-1,
                "hygrometer_count":0,               # The number of Hygrometers attached
                                    # sublist of dynamic hygrometers?
                "cover_state":"Uninitialized",              # Current state of the cover
                }

status =        {"cover_state": -1,
                "error_msg": "none"
                }

settings =      {"name":"UnNamed",                          # Name of Device
                "uuid": "NOT_SET0-0000-0000-0000-000000000000",   # UUID V1
                "token": "none",      # post token key
                "challenge": "temppass",                    # challenge
                "mac_address":"00:00:00:00:00:00",          # MAC address
                "server_reg_addr":    DOMAIN[DOMAIN_INDEX] + "api/register",
                "server_status_addr": DOMAIN[DOMAIN_INDEX] + "api/update",
                "server_update_addr": DOMAIN[DOMAIN_INDEX] + "api/update",
                "server_img_addr":    DOMAIN[DOMAIN_INDEX] + "api/image",
                "job_cover_monitor":1,                      # cover monitor run rate
                "job_save_settings":60,                     # save settings to file
                "job_sensors_sec"  :5,                      # job runs every x seconds
                "job_webcam_sec"   :2,                      # job runs every x seconds
                "job_server_webcam_sec" :5,                 # send webcam picture job
                "job_server_status_sec" :1,                 # send device status job
                "job_server_sensors_sec":20,                # send device sensors job
                                                            # other jobs
                "cover_schedual_en":1,                      # auto schedule enabled
                "cover_time_open": "YYYY-MM-DD HH:MM:SS",   # open time
                "cover_time_close": "YYYY-MM-DD HH:MM:SS",  # close time
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
        print ("Load settings error ", e)

    else:       # if file was found and all is good
        # print temp             # debugger
        if temp["uuid"] == settings["uuid"]:
            print ("UUID matches loaded settings - keeping")
            settings = temp     # set settings to loaded values

            # override loaded url's to match DOMAIN_INDEX
            # loaded settings is screwing up server comm when switching DoMAIN_INDEX
            settings["server_reg_addr"]    = DOMAIN[DOMAIN_INDEX] + "api/register"
            settings["server_status_addr"] = DOMAIN[DOMAIN_INDEX] + "api/update"
            settings["server_update_addr"] = DOMAIN[DOMAIN_INDEX] + "api/update"
            settings["server_img_addr"]    = DOMAIN[DOMAIN_INDEX] + "api/image"

        else:
            print ("UUID does not mach loaded settings - discarding")
            print ("Using default settings")
