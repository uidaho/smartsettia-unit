import time

temperature = 0
sysTemp = 35
sensor_dat = 0

# update all sensor values
def update():
    global sensor_dat
    get_Temp_Hum()
    get_light()
    get_Sys_Temp()
    return sensor_dat

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
