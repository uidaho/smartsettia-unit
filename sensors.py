import time

temperature = 0
sysTemp = 35

def getTemp():
    global temperature
    temperature = (temperature + 1) % 50 + 50
    #print temperature
    return temperature

def getSysTemp():
    global sysTemp
    sysTemp = (sysTemp + 1) % 50 + 50
    #print "System Temp: ", sysTemp
    return sysTemp
