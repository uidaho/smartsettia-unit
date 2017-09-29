import time
import platform         # test if pi for cpu temp
import my_globals

FAKE_SENSORS = 1

# Aliasing my_globals.sensor_dat to just sensor_dat
# normally you'd access this by my_globals.sensor_dat
sensor_dat = my_globals.sensor_dat

# sensor simulate
sim_temperature = 0   # needs to be global to simulate Sensors
sim_cpuTemp = 35      # needs to be global to simulate Sensors

# update all sensor values
def update():
    global sensor_dat
    sensor_dat["Temperature"]    = get_Temp_Hum()
    get_light()
    sensor_dat["cpu_temp"] = get_cpu_temp()

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
    if FAKE_SENSORS == False and platform.machine() == "armv7l":
        return check_output(["/opt/vc/bin/vcgencmd measure_temp | cut -c6-9"], shell=True)[:-1]
    else:                   # either faking sensors and/or no armv7l architecture detected
        global sim_cpuTemp
        sim_cpuTemp = (sim_cpuTemp + 1) % 50 + 50
        return sim_cpuTemp
