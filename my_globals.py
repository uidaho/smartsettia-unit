# This file contains the global variables used in smartsettia

version= "0.0.1"

# Note to concatonate dictionaries
# z = x.copy()
# z.update(y)

sensor_dat =    {"capture_time":"YYYY-MM-DD HH:MM:SS",
                "light_in":-1,                      # ambiant light sensor inside
                "light_out":-1,                     # ambiant light sensor outside
                "limitsw_open":-1,                  # limit switch on open side
                "limitsw_close":-1,                 # limit switch on close side
                "cover_state":"Uninitialized",      # Current state of the cover
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
                "server_addr": "https://smartsettia.com/api/ping",
                #"server_reg_addr": "https://smartsettia.com/api/register",
                "server_reg_addr": "https://smartsettia-backburn.c9users.io/api/register",
                #"server_reg_addr": "https://smartsettia-nkrenowicz.c9users.io/api/register",
                "server_img_addr": "https://smartsettia-backburn.c9users.io/api/image",
                #"server_img_addr": "http://httpbin.org/post",
                "job_cover_monitor":1,                      # cover monitor run rate
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
