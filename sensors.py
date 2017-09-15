import time
import my_globals

# Aliasing my_globals.sensor_dat to just sensor_dat
# normally you'd access this by my_globals.sensor_dat
sensor_dat = my_globals.sensor_dat

# sensor simulate
temperature = 0   # needs to be global to simulate Sensors
sysTemp = 35      # needs to be global to simulate Sensors

# update all sensor values
def update():
    global sensor_dat
    sensor_dat["Temp"]    = get_Temp_Hum()
    get_light()
    sensor_dat["SysTemp"] = get_Sys_Temp()

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
def get_Sys_Temp():
    global sysTemp
    sysTemp = (sysTemp + 1) % 50 + 50
    #print "System Temp: ", sysTemp
    return sysTemp
