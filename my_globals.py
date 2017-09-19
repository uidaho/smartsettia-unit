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

settings =      {"name":"UnNamed",                          # Name of Device
                "uuid": "NOT_SET0-0000-0000-0000-000000000000",   # UUID V1
                "token": "aSDf7986a89s7df87asd98f7dd",      # post token key
                "challenge": "temppass",                    # challenge
                "mac_address":"00:00:00:00:00:00",          # MAC address
                "server_addr": "https://smartsettia.com/api/ping",
                "server_reg_addr": "http://smartsettia-backburn.c9users.io/api/register",
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
                "webcam_pic_dir": "/tmp/"                   # directory where picture is saved
                }


server_base_packet=    {"time":"YYYY-MM-DD HH:MM:SS",      # time of packet
                        "uuid": settings["uuid"],
                        "token": settings["token"],
                        "version": version,                 # program version
                        "packetNo":0,                       # packet number
                        }

# This should move to the server file when created
server_send_packet =    {"time":"YYYY-MM-DD HH:MM:SS",      # time of packet
                        "uuid": settings["uuid"],
                        "token": settings["token"],
                        "version": version,                 # program version
                        "packetNo":0,                       # packet number
                        }

server_status_packet = {"time":"YYYY-MM-DD HH:MM:SS",      # time of packet
                        "uuid": settings["uuid"],
                        "token": settings["token"],
                        "version": version,                 # program version
                        "packetNo":0,                       # packet number
                        "cover_status": "open",
                        "error_msg": "none"
                        }

server_webcam_packet = {"time":"YYYY-MM-DD HH:MM:SS",      # time of packet
                        "uuid": settings["uuid"],
                        "version": version,                 # program version
                        "packetNo":0,                       # packet number
                        "token": settings["token"],
                        "webcam_picture": "binary"
                        }

# not complete
server_recv_packet =    {"commands": "commands kwarg?",
                        "new_settings": "new settings kwarg"
                        }
