# state machines      https://dev.to/karn/building-a-simple-state-machine-in-python
# gpio doc            https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
# interactive pinout: https://pinout.xyz/pinout/wiringpi
# gpio cheatsheet:    http://raspi.tv/download/RPi.GPIO-Cheat-Sheet.pdf
# gpio callbacks:     https://makezine.com/projects/tutorial-raspberry-pi-gpio-pins-and-python/
import my_globals
from my_globals import sensor_data
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
        
pin_relay      = 14
pin_ls_open    = 5      # pull up
pin_ls_close   = 13     # pull up
        
# GPIO initialization
if (my_globals.NOT_PI != True):
    try: 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin_relay,    GPIO.OUT)
        GPIO.output(pin_relay,   GPIO.LOW)  # set pin output to LOW
        GPIO.setup(pin_ls_open,  GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(pin_ls_close, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    except Exception as e:
        print ("Error setting GPIO.", e)
        print("\tFalling over to disable GPIO. This will lead to unexpected behaviour with the cover.")
        my_globals.status['error_msg'] = "GPIO Library could not be loaded"
        time.sleep(3) # Allow the user time to catch this error
        my_globals.NOT_PI = "True"



states = {"open", "opening", "closed", "closing", "error", "locked"}
fsm_current_state = "error"

fsm_transition_state = 0    # Linear sub state counter for opening & closing
wait_time = 0               # time variable that will mark the time to stop waiting

RELAY_WAIT = 3
COVER_WAIT = 25

# current status reported to the server
server_cmd = None

# local readings of limit switches
# later copied to my_globals sensor data
ls_open = 1
ls_close = 0



# Top most Finite State Machine function
# Determins what is the active state and calls that function
def fsm():
    print ( "Cover monitor - Current state %s" % fsm_current_state)
    global ls_open, ls_close, server_cmd
    getSwitches()
    print ("\tCurrent sensors open/closed (%d,%d)"% (ls_open, ls_close)) #(sensor_data["limitsw_open"], sensor_data["limitsw_close"]))

    server_cmd = my_globals.status['server_command']
    print ("\tCurrent server command: ", server_cmd)
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
    # sensor_data["limitsw_open"]  = ls_open
    # sensor_data["limitsw_close"] = ls_close
    my_globals.status["cover_status"] = fsm_current_state
    print ( "fsm - Next state %s" % fsm_current_state)
    print ("--------------------------------------")
    
def fsm_open():
    print ("Entered State: open")
    global ls_close, ls_close, fsm_current_state, fsm_transition_state
    # if not open. unexpected movement
    if  not (ls_open == 1 and ls_close == 0):
        my_globals.status["error_msg"] = "Unexpected Movement"
        fsm_current_state = "error"
    
    # check next state conditions
    elif (server_cmd == "open"):
        return                  # do nothing
    elif (server_cmd == "close"):
        print ("Server change event: closing")
        fsm_transition_state = "ts0:RelayOn"       # reset
        fsm_current_state = "closing"
    elif (server_cmd == "lock"):
        print ("Server change event: locked")
        fsm_current_state = "locked"
    else:
        print ("Unknown server change")
            
def fsm_close():
    print ("Entered State: closed")
    global ls_close, ls_close, fsm_current_state, fsm_transition_state
    # if not closed. unexpected movement
    if  not (ls_open == 0 and ls_close == 1):
        my_globals.status["error_msg"] = "Unexpected Movement"
        fsm_current_state = "error"

    # check next state conditions
    elif (server_cmd == "close"):  # server says close. i'm currently in the 'closed' state
        return                  # do nothing
    elif (server_cmd == "open"):
        print ("Server change event: opening")
        fsm_transition_state = "ts0:RelayOn"       # reset
        fsm_current_state = "opening"
    elif (server_cmd == "lock"):
        print ("Server change event: locked")
        fsm_current_state = "locked"
    else:
        print ("Unknown server change")
    
            
def fsm_opening():
    print ("Entered State: opening\tSubstate: %s" % fsm_transition_state)
    global ls_open, ls_close, fsm_current_state, wait_time
    global fsm_transition_state
    
    """ Transition states
    ts0:RelayOn      relay on
    ts1:RelayWait    keep relay on for set time. then turn off
    *ts2:Null         NULL not implemented
    ts3:MovingTest   testing if it moved
    ts4:Moving       cover currently moving
    """
    
    if fsm_transition_state == "ts0:RelayOn":       # turn relay on
        set_Relay("on")
        wait_time = time.time() + RELAY_WAIT  # waiting x seconds
        print ("\tRelay -time is: %0.1f,\t wait time: %0.1f" % (time.time(), wait_time))
        fsm_transition_state = "ts1:RelayWait"
    
    elif fsm_transition_state == "ts1:RelayWait":     # wait - relay off
        if (time.time() >= wait_time):                # if we exceded our wait time
            set_Relay("off")                          # turn off relay
            fsm_transition_state = "ts3:MovingTest"   # go to next transition state
        
    # test if cover is actually moving
    elif fsm_transition_state == "ts3:MovingTest":
        if (ls_open == 0 and ls_close == 0):
            wait_time = time.time() + COVER_WAIT  # waiting x seconds
            print ("\tCover -time is: %0.1f,\t timout time: %0.1f" % (time.time(), wait_time))
            fsm_transition_state = "ts4:Moving"           # test pass. its moving
        else: 
            my_globals.status["error_msg"] = "Cover did not move"
            print("\tError: Cover did not move. Time now is: %0.1f" % time.time())
            fsm_current_state = "error"         # send to error state
    
    # its moving. lets wait for it to finish
    elif fsm_transition_state == "ts4:Moving":
        # did it finish and open?
        if (ls_open == 1 and ls_close == 0):
            # success
            print("\tOpening finished")
            fsm_current_state = "open"          # send to open state
            
        # did it somehow reverse and went back to close? dont know how
        elif (ls_open == 0 and ls_close == 1):
            my_globals.status["error_msg"] = "Cover closed itself?"
            print("\tError: Cover closed itself")
            fsm_current_state = "error"         # send to error state
            
        # timed out
        elif (time.time() > wait_time):
            my_globals.status["error_msg"] = "Cover movement timed out. Waiting for it to resolve to open or close"
            print("\tCover movement timed out at %0.1f. Waiting for it to resolve to open or close" % time.time())
            fsm_current_state = "error"         # send to error state
            
        # 0,0 and not timedout 
            # do nothing. we are waiting

    
def fsm_closing():
    print ("Entered State: closing\tSubstate: %s" % fsm_transition_state)
    global ls_open, ls_close, fsm_current_state, wait_time
    global fsm_transition_state
    
    """ Transition states
    ts0:RelayOn      relay on
    ts1:RelayWait    keep relay on for set time. then turn off
    *ts2:Null         NULL not implemented
    ts3:MovingTest   testing if it moved
    ts4:Moving       cover currently moving
    """
    
    if fsm_transition_state == "ts0:RelayOn":       # turn relay on
        set_Relay("on")
        wait_time = time.time() + RELAY_WAIT  # waiting x seconds
        print ("\tRelay -time is: %0.1f,\t wait time: %0.1f" % (time.time(), wait_time))
        fsm_transition_state = "ts1:RelayWait"
    
    elif fsm_transition_state == "ts1:RelayWait":     # wait - relay off
        if (time.time() >= wait_time):                # if we exceded our wait time
            set_Relay("off")                          # turn off relay
            fsm_transition_state = "ts3:MovingTest"   # go to next transition state
        
    # test if cover is actually moving
    elif fsm_transition_state == "ts3:MovingTest":
        if (ls_open == 0 and ls_close == 0):
            wait_time = time.time() + COVER_WAIT  # waiting x seconds
            print ("\tCover -time is: %0.1f,\t timout time: %0.1f" % (time.time(), wait_time))
            fsm_transition_state = "ts4:Moving"           # test pass. its moving
        else: 
            my_globals.status["error_msg"] = "Cover did not move"
            print("\tError: Cover did not move. Time now is: %0.1f" % time.time())
            fsm_current_state = "error"         # send to error state
    
    # its moving. lets wait for it to finish
    elif fsm_transition_state == "ts4:Moving":
        # did it finish and close?
        if (ls_open == 0 and ls_close == 1):
            # success
            print("\tClosing finished")
            fsm_current_state = "closed"          # send to open state
            
        # did it somehow reverse and went back to close? dont know how
        elif (ls_open == 1 and ls_close == 0):
            my_globals.status["error_msg"] = "Cover opened itself?"
            print("\tError: Cover opened itself")
            fsm_current_state = "error"         # send to error state
            
        # timed out
        elif (time.time() > wait_time):
            my_globals.status["error_msg"] = "Cover movement timed out. Waiting for it to resolve to open or close"
            print("\tCover movement timed out at %0.1f. Waiting for it to resolve to open or close" % time.time())
            fsm_current_state = "error"         # send to error state
            
        # 0,0 and not timedout 
            # do nothing. we are waiting
    
def fsm_locked():
    print ("Entered State: locked")
    global fsm_current_state
    if (server_cmd != "lock"):
        fsm_current_state = "error" # to resolve
        fsm_error()                 # run immediatly to resolve state if possible before the next status update
    
# error and resolution
def fsm_error():
    print ("Entered State: Error")
    global ls_open, ls_close, fsm_current_state
    if  (ls_open == 1 and ls_close == 0):
        fsm_current_state = "open"
        my_globals.status["server_command"]  = "open"
        my_globals.status["server_override"] = True  # will change server state to match
    elif (ls_open == 0 and ls_close == 1):
        fsm_current_state = "closed"
        my_globals.status["server_command"]  = "close"
        my_globals.status["server_override"] = True  # will change server state to match
    elif (ls_open == 0 and ls_close == 0):
        fsm_current_state = "error"
    else:
        print ("Unknown error")
        fsm_current_state = "error"

# set relay pin to value
def set_Relay(val):
    print ("Setting Relay to %s" % val)
    print ("not pi: ", my_globals.NOT_PI)
    if (my_globals.NOT_PI == True):    # this is NOT a pi and NOT usng gpio
        print ("\tGPIO disabled")
    else:
        try:
            if (val == "on"):
                print ("\tTurning relay on")
                GPIO.output(pin_relay, GPIO.HIGH)
            else: # val == "off" or any other value. default off
                print ("\tTurning relay off")
                GPIO.output(pin_relay, GPIO.LOW)
        except Exception as e:
            print ("\tError setting relay GPIO output pin", e)


# read limit switches
def getSwitches():
    print ("Reading limit switches")
    global ls_open, ls_close
    if (my_globals.NOT_PI == True):     # this is NOT a pi and NOT usng gpio
        # Simulate switches based on current state
        print ("\t## Simulating switches")
        """
        ts0:RelayOn      relay on
        ts1:RelayWait    keep relay on for set time. then turn off
        *ts2:Null         NULL not implemented
        ts3:MovingTest   testing if it moved
        ts4:Moving       cover currently moving
        """
        if (fsm_current_state == "open"):       # the open switch should be active
            ls_open  = 1
            ls_close = 0
        elif (fsm_current_state == "closed"):    # the close switch should be active
            ls_open  = 0
            ls_close = 1
        elif (fsm_current_state == "error"):  # resolve to open when in error state
            ls_open  = 1
            ls_close = 0
        elif (fsm_current_state == "opening" or fsm_current_state == "closing"): # in transition states
            if (fsm_transition_state == "ts1:RelayWait"):   # relay activates motor which puts the cover in between the switches
                ls_open  = 0
                ls_close = 0
            if (fsm_transition_state == "ts4:Moving"):      # Done moving and hits its termination state
                if (fsm_current_state == "opening"):        # open state
                    ls_open  = 1
                    ls_close = 0
                else:                                       # closed state
                    ls_open  = 0
                    ls_close = 1
        
    else: 
        try:
            ls_open = not GPIO.input(pin_ls_open)
            ls_close = not GPIO.input(pin_ls_close)
            print ("getSwitches: (%d, %d)" %(ls_open, ls_close))
        except Exception as e:
            print ("\tError reading limit switch pins:", e)
        

# This will reset gpios back to what they were before the script started.
# The problem is that this program exits by interruping it and so this will never get called
# Included for best habbit but cant call it outside of the --single run senario
def gpio_cleanup():
    if (my_globals.NOT_PI == False):
        GPIO.cleanup()
