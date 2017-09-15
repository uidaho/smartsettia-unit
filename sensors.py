import time

# sensor simulate
temperature = 0
sysTemp = 35

# sensor data structure
sensor_dat = {"Temp":0,"Humidity":0,"SysTemp":0}

# update all sensor values
def update():
    global sensor_dat
    sensor_dat["Temp"]    = get_Temp_Hum()
    get_light()
    sensor_dat["SysTemp"] = get_Sys_Temp()
    #print "\ttemp: %d, sysTemp: %d" %(sensor_dat["Temp"], sensor_dat["SysTemp"])
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
