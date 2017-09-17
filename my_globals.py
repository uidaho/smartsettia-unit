# This file contains the global variables used in smartsettia

sensor_dat =    {"capture_time":"YYYY-MM-DD HH:MM:SS",
                "temperature":-1,
                "humidity":-1,
                "light_out":-1,                  # ambiant light sensor outside
                "light_in":-1,                   # ambiant light sensor inside
                "limitsw_open":-1,               # limit switch on open side
                "limitsw_close":-1,              # limit switch on close side
                "hygrometer_count":0,           # The number of Hygrometers attached
                                                # sublist of dynamic hygrometers?
                "cover_state":"Uninitialized",  # Current state of the cover
                "cpu_temp":-1}                   # pi system temperature

settings =      {"name":"UnNamed",                  # Name of Device
                "SN":"NOTSET_000000000",            # Pi Serial Number
                "server_addr": "https://smartsettia.com/api",
                "token": "some token data",         # post token key
                "job_sensors_sec":5,                # job runs every x seconds
                "job_webcam_sec":2,                 # job runs every x seconds
                                                    # other jobs
                "cover_schedual_en":1,              # auto schedule enabled
                "cover_time_open": "some time data",  # open time
                "cover_time_close": "some time data",}# close time


# This should move to the server file when created
server_send_packet =    {"Time":"YYYY-MM-DD HH:MM:SS",
                        "sensors": sensor_dat,
                        "packetNo":0,
                        "token": settings["Token"],
                        "webcam_picture":"Binary"}

# not complete
server_recv_packet =    {"commands": "commands kwarg?",
                        "new_settings": "new settings kwarg"}
