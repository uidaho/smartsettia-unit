# https://dev.to/karn/building-a-simple-state-machine-in-python
# gpio https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
# interactive pinout: https://pinout.xyz/pinout/wiringpi#
import my_globals
from my_globals import sensor_dat
import time

# Import gpio
if (my_globals.NOT_PI != True):
    try:
        import RPi.GPIO as GPIO
    except RuntimeError:
        print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
        print("\tFalling over to disable GPIO. This will lead to unexpected behaviour with the cover.")
        my_globals.status['error_msg'] = "GPIO Library could not be loaded"
        time.sleep(3) # Allow the user time to catch this error
        my_globals.NOT_PI = "True"
        
pin_relay    = 5
pin_ls_open  = 6
pin_ls_close = 7
        
# GPIO initialization
if (my_globals.NOT_PI != True):
    try: 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin_relay,    GPIO.OUT)
        GPIO.setup(pin_ls_open,  GPIO.IN)
        GPIO.setup(pin_ls_close, GPIO.IN)
    except Exception as e:
        print ("Error setting GPIO.", e)
        print("\tFalling over to disable GPIO. This will lead to unexpected behaviour with the cover.")
        my_globals.status['error_msg'] = "GPIO Library could not be loaded"
        time.sleep(3) # Allow the user time to catch this error
        my_globals.NOT_PI = "True"


states = {"open", "opening", "closed", "closing", "error", "locked"}
fsm_current_state = "error"

fsm_transition_state = 0    # Linear sub state counter for opening & closing

# current status reported to the server
current_status = "error"
server = "open"

# local readings of limit switches
# later copied to my_globals sensor data
ls_open = 1
ls_close = 0


# Top most Finite State Machine function
# Determins what is the active state and calls that function
def fsm():
    print ( "fsm - Current state %s" % fsm_current_state)
    global ls_open, ls_close, server
    print ("Current sensors open/close (%d,%d)"% (sensor_dat["limitsw_open"], sensor_dat["limitsw_close"]))
    server = my_globals.status['server_command']
    print ("Current server command: ", server)
    if fsm_current_state == "error":
        fsm_error()
    elif (fsm_current_state == "open"):
        fsm_open()
    elif (fsm_current_state == "closed"):
        fsm_close()
    elif (fsm_current_state == "opening"):
        fsm_opening()
    elif (fsm_current_state == "closing"):
        fsm_closing()
    elif (fsm_current_state == "locked"):
        fsm_locked()
    else:
        print ("ERROR: Unknown state.")
    
    # update global variables with current limit switches
    sensor_dat["limitsw_open"]  = ls_open
    sensor_dat["limitsw_close"] = ls_close
    my_globals.status["cover_status"] = fsm_current_state
    print ( "fsm - Next state %s" % fsm_current_state)
    print ("--------------------------------------")
    

def fsm_open():
    print ("Entered State: open")
    global ls_close, ls_close, fsm_current_state
    # if not open. unexpected movement
    print ("fsm_open:server = ", server)
    if  not (ls_open == 1 and ls_close == 0):
        my_globals.status["error_msg"] = "Unexpected Movement"
        fsm_current_state = "error"
    # check if the we are not were we want to be
    elif (server != fsm_current_state):
        if (server == "close"):
            print ("Server change event: closing")
            fsm_current_state = "closing"
        elif (server == "lock"):
            print ("Server change event: locked")
            fsm_current_state = "locked"
        else:
            print ("Unknown server change")
            
def fsm_close():
    print ("Entered State: closed")
    global ls_close, ls_close, fsm_current_state
    # if not open. unexpected movement
    if  not (ls_open == 0 and ls_close == 1):
        my_globals.status["error_msg"] = "Unexpected Movement"
        fsm_current_state = "error"
    elif (server != fsm_current_state):
        if (server == "open"):
            print ("Server change event: opening")
            fsm_current_state = "opening"
        elif (server == "lock"):
            print ("Server change event: locked")
            fsm_current_state = "locked"
        else:
            print ("Unknown server change")
            
def fsm_opening():
    print ("Entered State: opening\tSubstate: %d" % fsm_transition_state)
    global ls_open, ls_close, fsm_current_state
    global fsm_transition_state
    
    """ Transition states
    0 powering relay
    1 wait relay on
    2 relay off & waiting
    3 movement test 
    4 moving
    """
    
    if fsm_transition_state == 0:       # turn relay on
        set_Relay("on")
        fsm_transition_state = 1
    
    elif fsm_transition_state == 1:     # wait - relay on
        # wait
        x = 1
        fsm_transition_state = 2
    
    elif fsm_transition_state == 2:     # turn relay off
        set_Relay("off")
        fsm_transition_state = 3
        sw00()         # DEBUGGER REMOVE LATER
        
   # test if cover is actually moving
    elif fsm_transition_state == 3:
        if (ls_open == 0 and ls_close == 0):
            fsm_transition_state = 4           # test pass. its moving
        else: 
            my_globals.status["error_msg"] = "Cover did not move"
            fsm_transition_state = 0            # reset
            fsm_current_state = "error"         # send to error state
    
    # its moving. lets wait for it to finish
    elif fsm_transition_state == 4:
        # did it finish and open?
        if (ls_open == 1 and ls_close == 0):
            # success
            fsm_transition_state = 0            # reset
            fsm_current_state = "open"          # send to open state
        # did it somehow revers and went back to close? dont know how
        elif (ls_open == 0 and ls_close == 1):
            my_globals.status["error_msg"] = "Cover closed itself?"
            fsm_transition_state = 0            # reset
            fsm_current_state = "error"         # send to error state
        # timed out
            # if timmed out .....
                #my_globals.status["error_msg"] = "Cover movement timed out. Waiting for it to resolve to open or close"
                #fsm_transition_state = 0            # reset
                #fsm_current_state = "error"         # send to error state
        # 0,0 and not timedout 
            # do nothing. we are waiting
        sw1()           # DEBUGGER REMOVE LATER

    
def fsm_closing():
    print ("Entered State: closing")
    global ls_open, ls_close, fsm_current_state
    fsm_current_state = "closed"
    sw0()           # DEBUGGER REMOVE LATER
    
def fsm_locked():
    print ("Entered State: locked")
    global fsm_current_state
    if (server != "lock"):
        fsm_current_state = "error" # to resolve
    
# error and resolution
def fsm_error():
    print ("Entered State: Error")
    global ls_open, ls_close, fsm_current_state
    if  (ls_open == 1 and ls_close == 0):
        fsm_current_state = "open"
        sw1()           # DEBUGGER REMOVE LATER
    elif (ls_open == 0 and ls_close == 1):
        fsm_current_state = "closed"
        sw0()           # DEBUGGER REMOVE LATER
    elif (ls_open == 0 and ls_close == 0):
        fsm_current_state = "error"
    else:
        print ("Unknown error")
        fsm_current_state = "error"

# set relay pin to value
def set_Relay(val):
    print ("Setting Relay to %d" % val)
    if (my_globals.NOT_PI == False):    # this is a pi and usng gpio
        try:
            if (val == "on"):
                GPIO.output(pin_relay, GPIO.HIGH)
                # we could just wait a second here. then turn off. 
                # it would save us some complexity and additional states at the cost of a blocking statement
            else: # val == "off" or any other value. default off
                GPIO.output(pin_relay, GPIO.LOW)
        except Exception as e:
            print ("\tError setting relay output pin", e)
    else:
        print ("\tGPIO disabled")
        

# read limit switches
def getSwitches():
    print ("Reading limit switches")
    global ls_open, ls_close
    if (my_globals.NOT_PI == True):
        ls_open  = 0 # setting these to 0 will land the state machine in error mode
        ls_close = 1
    else: 
        try:
            ls_open = GPIO.input(channel)
            ls_close = GPIO.input(channel)
        except Exception as e:
            print ("\tError reading limit switch pins", e)
        
        
    
# debugging function set to open
def sw1():
    print ("Reading limit switches")
    global ls_open, ls_close
    ls_open  = 1
    ls_close = 0
    
# debugging function set to close
def sw0():
    print ("Reading limit switches")
    global ls_open, ls_close
    ls_open  = 0
    ls_close = 1
    
# debugging function set to close
def sw00():
    print ("Reading limit switches")
    global ls_open, ls_close
    ls_open  = 0
    ls_close = 0
    

if False:
    # Testing Code
    fsm()
    fsm()
    print ("server closed")
    #server = "closed"
    fsm()
    fsm()
    fsm()
    print ("server open")
    #server = "open"
    fsm()
    fsm()
    fsm()