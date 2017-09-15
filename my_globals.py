# This file contains the global variables used in smartsettia

sensor_dat =    {"Capture_Time":"YYYY-MM-DD HH:MM:SS",
                "Temperature":-1,
                "Humidity":-1,
                "Light_out":-1,                  # ambiant light sensor outside
                "Light_in":-1,                   # ambiant light sensor inside
                "Limitsw_open":-1,               # limit switch on open side
                "Limitsw_close":-1,              # limit switch on close side
                "Hygrometer_count":0,           # The number of Hygrometers attached
                                                # sublist of dynamic hygrometers?
                "Cover_State":"Uninitialized",  # Current state of the cover
                "SysTemp":-1}                    # pi system temperature

settings =      {"Name":"UnNamed",                  # Name of Device
                "SN":"NOTSET_000000000",            # Pi Serial Number
                "Server_addr": "https://smartsettia.com/api",
                "Job_sensors_sec":5,                # job runs every x seconds
                "job_webcam_sec":2                  # job runs every x seconds
                                                    # other jobs
                "Cover_schedual_en":1,              # auto schedule enabled
                "Cover_schedual_open": "somedata",  # open time
                "Cover_schedual_close": "somedata",}# close time


# This should move to the server file when created
server_send_packet =    {"Time":"YYYY-MM-DD HH:MM:SS",
                        "Sensors": sensor_dat,
                        "PacketNo":0,
                        "WebcamPicture":"Binary?"}

# not complete
server_recv_packet =    {"commands": "commands kwarg?"
                        "New Settings": "new settings kwarg"}
