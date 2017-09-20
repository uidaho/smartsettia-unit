# This file contains the global variables used in smartsettia

version= "0.0.1"

sensor_dat =    {"capture_time":"YYYY-MM-DD HH:MM:SS",
                "temperature":-1,
                "humidity":-1,
                "light_out":-1,                             # ambiant light sensor outside
                "light_in":-1,                              # ambiant light sensor inside
                "limitsw_open":-1,                          # limit switch on open side
                "limitsw_close":-1,                         # limit switch on close side
                "hygrometer_count":0,                       # The number of Hygrometers attached
                                                            # sublist of dynamic hygrometers?
                "cover_state":"Uninitialized",              # Current state of the cover
                "cpu_temp":-1                               # pi system temperature
                }

settings =      {"name":"UnNamed",                          # Name of Device
                "uuid": "aa2c0776-9b44-13e7-abc4-cec278b6b50a",   # UUID V1
                "mac_address":"00:00:00:00:00:00",           # MAC address
                "challenge": "temppass",                    # challenge
                #"server_addr": "https://smartsettia.com/api/ping",
                #"server_reg_addr": "https://smartsettia-backburn.c9users.io/api/register",
                "server_reg_addr": "https://smartsettia.com/api/register",
                "token": "aSDf7986a89s7df87asd98f7dd",      # post token key
                "job_sensors_sec":5,                        # job runs every x seconds
                "job_webcam_sec":2,                         # job runs every x seconds
                                                            # other jobs
                "cover_schedual_en":1,                      # auto schedule enabled
                "cover_time_open": "YYYY-MM-DD HH:MM:SS",   # open time
                "cover_time_close": "YYYY-MM-DD HH:MM:SS",  # close time
                "webcam_pic_dir": "/tmp/"                   # directory where picture is saved
                }


# This should move to the server file when created
server_send_packet =    {"Time":"YYYY-MM-DD HH:MM:SS",      # time of packet
                        "UUID": settings["uuid"],
                        "version": version,                 # program version
                        "packetNo":0,                       # packet number
                        "token": settings["token"],
                        "sensors": sensor_dat,              # sensor data
                        "webcam_picture":"Binary"          # webcam picture binary
                        }

# not complete
server_recv_packet =    {"commands": "commands kwarg?",
                        "new_settings": "new settings kwarg"
                        }
