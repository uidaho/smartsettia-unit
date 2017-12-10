import time
import platform         # test if pi for cpu temp
import my_globals
from subprocess import check_output
import logging

FAKE_SENSORS = my_globals.NOT_PI

# sensor simulate
sim_temperature = 0   # needs to be global to simulate Sensors
sim_cpuTemp = 35      # needs to be global to simulate Sensors

# update all sensor values
def update():
    my_globals.sensor_data["sensor_data"][0]["value"] = str(get_cpu_temp())
    my_globals.sensor_data["sensor_data"][1]["value"] = get_light()
    my_globals.sensor_data["sensor_data"][2]["value"] = str(get_light())  # TODO add light inner
    my_globals.sensor_data["sensor_data"][3]["value"] = str(get_Temp_Hum())
    logging.debug("Tempsensor [3]: %r"% my_globals.sensor_data["sensor_data"][3])
    logging.debug("Temp: %s\tCpu Temp: %s\tLight: %s" % (get_Temp_Hum(), get_cpu_temp(), get_light()))

# get temperature and humidity from sensor
def get_Temp_Hum():
    global sim_temperature
    sim_temperature = (sim_temperature + 1) % 50 + 50
    #print temperature
    return sim_temperature

# get ambiant light data
def get_light():
    light = 15
    return light

# get raspberri pi system temp
def get_cpu_temp():
    "Returns the CPU temerature based on architecture"
    if platform.machine() == "armv7l":
        return check_output(["/opt/vc/bin/vcgencmd measure_temp | cut -c6-9"], shell=True)[:-1].decode('utf-8')
    else:                   # either faking sensors and/or no armv7l architecture detected
        global sim_cpuTemp
        sim_cpuTemp = (sim_cpuTemp + 1) % 50 + 50
        return sim_cpuTemp
