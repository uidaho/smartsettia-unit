import time
import my_globals

# Aliasing my_globals.sensor_dat to just sensor_dat
# normally you'd access this by my_globals.sensor_dat
sensor_dat = my_globals.sensor_dat

# sensor simulate
temperature = 0   # needs to be global to simulate Sensors
cpuTemp = 35      # needs to be global to simulate Sensors

# update all sensor values
def update():
    global sensor_dat
    sensor_dat["Temperature"]    = get_Temp_Hum()
    get_light()
    sensor_dat["cpu_temp"] = get_cpu_temp()

# get temperature and humidity from sensor
def get_Temp_Hum():
    global temperature
    temperature = (temperature + 1) % 50 + 50
    #print temperature
    return temperature

# get ambiant light data
def get_light():
    light = 15
    return light

# get raspberri pi system temp
def get_cpu_temp():
    global cpuTemp
    cpuTemp = (cpuTemp + 1) % 50 + 50
    #print "System Temp: ", sysTemp
    return cpuTemp
