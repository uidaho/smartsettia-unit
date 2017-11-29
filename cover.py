# state machines      https://dev.to/karn/building-a-simple-state-machine-in-python
# gpio doc            https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
# interactive pinout: https://pinout.xyz/pinout/wiringpi
# gpio cheatsheet:    http://raspi.tv/download/RPi.GPIO-Cheat-Sheet.pdf
# gpio callbacks:     https://makezine.com/projects/tutorial-raspberry-pi-gpio-pins-and-python/
import my_globals
from my_globals import sensor_data
import time
import datetime
import logging

# Import gpio
if (my_globals.NOT_PI != True):
    try:
        import RPi.GPIO as GPIO
    except RuntimeError:
        logging.error("Error importing RPi.GPIO!")
        logging.error("Falling over to disable GPIO. This will lead to unexpected behaviour with the cover.")
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
        logging.error ("Error setting GPIO. %r" % e)
        logging.error("Falling over to disable GPIO. This will lead to unexpected behaviour with the cover.")
        my_globals.status['error_msg'] = "GPIO Library could not be loaded"
        time.sleep(3) # Allow the user time to catch this error
        my_globals.NOT_PI = "True"



states = {"open", "opening", "closed", "closing", "error", "locked"}
fsm_current_state = "error"

fsm_transition_state = 0    # Linear sub state counter for opening & closing
wait_time = 0               # time variable that will mark the time to stop waiting

# wait times for transition state
RELAY_WAIT = 3
COVER_WAIT = 25

# current status reported to the server
server_cmd = None

# local readings of limit switches
# later copied to my_globals sensor data
ls_open = 1
ls_close = 0


# Open close schedule
def cover_schedule():
    logging.info ("--- Schedule -------------------------")
    global fsm_current_state, fsm_transition_state
    
    # Test if a schedule has been set
    if (my_globals.settings["cover_time_open"] == None or my_globals.settings["cover_time_close"] == None):
        logging.warning ("One or both cover times are null: %r, %r" % (my_globals.settings["cover_time_open"], my_globals.settings["cover_time_close"]))
        time.sleep(2)                   # debugger allows the user to spot this event
        return
    
    # Naming convention  dt_open := datetime open;  t_open := time open 
    #t_open = datetime.datetime.strptime('04:07:00', '%H:%M:%S').time()         # debugger Manual set
    #t_close = datetime.datetime.strptime('04:44:00', '%H:%M:%S').time()        # debugger Manual set
    t_open =  datetime.datetime.strptime(my_globals.settings["cover_time_open"],  '%H:%M').time()    # time open     datetime.time
    t_close = datetime.datetime.strptime(my_globals.settings["cover_time_close"], '%H:%M').time()    # time close    datetime.time
    dt_now =  datetime.datetime.utcnow()                                                             # time now      datetime.datetime
    dt_last_checked = my_globals.settings["schedule_last_checked"]                                   # load raw last checked from settings
    
    # check if last check string is empty, if not parse it into datetime object
    if dt_last_checked == None:
        # null time. Update to curent time and return
        logging.warning ("Last checked time was blank.")
        dt_last_checked = datetime.datetime.strftime(dt_now, '%Y-%m-%d %H:%M:%S')
        my_globals.settings["schedule_last_checked"] = dt_last_checked
        return      # algoritm cannot work without a last check
    else:
        dt_last_checked = datetime.datetime.strptime(my_globals.settings["schedule_last_checked"], '%Y-%m-%d %H:%M:%S')
    
    # convert times into datetime. Add todays date and event time together to form a datetime object
    date_today = datetime.date.today()
    dt_open  = datetime.datetime.combine( date_today, t_open )
    dt_close = datetime.datetime.combine( date_today, t_close )
    
    # debugging times
    logging.debug ("time now   : %s" % dt_now)
    logging.debug ("last check : %s" % dt_last_checked)
    logging.debug ("time open  : %s" % dt_open)
    logging.debug ("time close : %s" % dt_close)
    
    close_active = False    # true if open  event is within our test
    open_active  = False    # true if close event is within our test
    
    try:
        # Test if open time is between last checked and now
        if dt_open > dt_last_checked and dt_open < dt_now:
            open_active = True
        # Test if close time is between last checked and now
        if dt_close > dt_last_checked and dt_close < dt_now:
            close_active = True
    except Exception as e:
        logging.error ("Schedule conditions error. %r" % e)
        return
    else:
        logging.debug ("Schedule condition events: open:%s, close:%s" % (open_active, close_active))
        if open_active and close_active:        # Both open and close events are within timeframe
            print ("   Both events happened since last checked. looking for latest")
            if dt_open > dt_close:              # checking which was the latest event
                logging.info ("Schedule opening activated")
                set_transition("open", "Schedule open", True)
            else:
                logging.info ("Schedule closing activated")
                set_transition("close", "Schedule close", True)
        else:                                   # only one event happened. act on whichever event that was
            if open_active:
                logging.info ("Schedule opening activated")
                set_transition("open", "Schedule open", True)
            elif close_active:
                logging.info ("Schedule closing activated")
                set_transition("close", "Schedule close", True)

    # update last checked timestamp
    dt_last_checked = datetime.datetime.strftime(dt_now, '%Y-%m-%d %H:%M:%S')   # convert datetime now to string
    my_globals.settings["schedule_last_checked"] = dt_last_checked


# This function sets up the state machine to a transition state
# like closed > opening or open > closing
def set_transition(cmd, source="unknown", override_server= False):
    global fsm_current_state, fsm_transition_state
    logging.info("Entered set transition: %s, %s, %s" %(cmd, source, override_server))
    dt_now = datetime.datetime.strftime(datetime.datetime.utcnow() , '%Y-%m-%d %H:%M:%S')
    coverlog = "%s - By %s" % (dt_now, source)     # this variable contains all the text that will be printed to terminal and log file

    if (cmd == "close"):
        if (fsm_current_state == "open"):                   # test to see if already open
            fsm_current_state = "closing"                   # set state machine to start moving
            fsm_transition_state = "ts0:RelayOn"            # reset transition substate back to 0
            coverlog += " - cover set to close"
            if override_server == True:
                my_globals.status["server_override"] = True  # change server command
                my_globals.status["server_command"] = "close"
                coverlog += " - overriding server cmd"
        elif (fsm_current_state == "closed"):
            coverlog += " - cover already closed. aborting"
        else:
            coverlog += " - can't close cover if cover is not in open state"
    
    elif (cmd == "open"):
        if (fsm_current_state == "closed"):                  # test to see if already open
            fsm_current_state = "opening"                   # set state machine to start moving
            fsm_transition_state = "ts0:RelayOn"            # reset transition substate back to 0
            coverlog += " - cover set to open "
            if override_server == True:
                my_globals.status["server_override"] = True   # change server command
                my_globals.status["server_command"] = "open"
                coverlog += " - overriding server cmd"
        elif (fsm_current_state == "open"):
            coverlog += " - cover already open. aborting"
        else:
            coverlog += " - can't open cover if cover is not in closed state"
    else:
        coverlog += " - unknown state. only open/close are recognised"
    
    # print log output
    logging.info (coverlog)
    file = open(my_globals.settings["storage_dir"] + "cover.log", "a")
    file.write(coverlog + ".\n")
    file.close
    return
            

# Top most Finite State Machine function
# Determins what is the active state and calls that function
def fsm():
    logging.debug ( "Cover monitor - Current state %s" % fsm_current_state)
    global ls_open, ls_close, server_cmd
    getSwitches()
    logging.debug ("\tCurrent sensors open/closed (%d,%d)"% (ls_open, ls_close)) #(sensor_data["limitsw_open"], sensor_data["limitsw_close"]))

    server_cmd = my_globals.status['server_command']
    logging.debug ("\tCurrent server command: %s" % server_cmd)
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
        logging.error ("ERROR: Unknown state.")
    
    my_globals.status["cover_status"] = fsm_current_state
    logging.debug ( "fsm - Next state %s" % fsm_current_state)
    
def fsm_open():
    logging.info ("Entered State: open")
    global ls_close, ls_close, fsm_current_state, fsm_transition_state
    # if not open. unexpected movement
    if  not (ls_open == 1 and ls_close == 0):
        my_globals.status["error_msg"] = "Unexpected Movement"
        fsm_current_state = "error"
    
    # check next state conditions
    elif (server_cmd == "open"):
        return                  # do nothing
    elif (server_cmd == "close"):
        logging.info ("Server change event: closing")
        set_transition("close", "Server cmd", False)
    elif (server_cmd == "lock"):
        logging.info ("Server change event: locked")
        fsm_current_state = "locked"
    else:
        logging.warning ("Unknown server change")
            
def fsm_close():
    logging.info ("Entered State: closed")
    global ls_close, ls_close, fsm_current_state, fsm_transition_state
    # if not closed. unexpected movement
    if  not (ls_open == 0 and ls_close == 1):
        my_globals.status["error_msg"] = "Unexpected Movement"
        fsm_current_state = "error"

    # check next state conditions
    elif (server_cmd == "close"):  # server says close. i'm currently in the 'closed' state
        return                  # do nothing
    elif (server_cmd == "open"):
        logging.info ("Server change event: opening")
        set_transition("open", "Server cmd", False)
    elif (server_cmd == "lock"):
        logging.info ("Server change event: locked")
        fsm_current_state = "locked"
    else:
        logging.warning ("Unknown server change")
    
            
def fsm_opening():
    logging.info ("Entered State: opening\tSubstate: %s" % fsm_transition_state)
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
        logging.debug ("\tRelay -time is: %0.1f,\t wait time: %0.1f" % (time.time(), wait_time))
        fsm_transition_state = "ts1:RelayWait"
    
    elif fsm_transition_state == "ts1:RelayWait":     # wait - relay off
        if (time.time() >= wait_time):                # if we exceded our wait time
            set_Relay("off")                          # turn off relay
            fsm_transition_state = "ts3:MovingTest"   # go to next transition state
        
    # test if cover is actually moving
    elif fsm_transition_state == "ts3:MovingTest":
        if (ls_open == 0 and ls_close == 0):
            wait_time = time.time() + COVER_WAIT  # waiting x seconds
            logging.debug ("\tCover -time is: %0.1f,\t timout time: %0.1f" % (time.time(), wait_time))
            fsm_transition_state = "ts4:Moving"           # test pass. its moving
        else: 
            my_globals.status["error_msg"] = "Cover did not move"
            logging.error("\tError: Cover did not move. Time now is: %0.1f" % time.time())
            fsm_current_state = "error"         # send to error state
    
    # its moving. lets wait for it to finish
    elif fsm_transition_state == "ts4:Moving":
        # did it finish and open?
        if (ls_open == 1 and ls_close == 0):
            # success
            logging.debug("\tOpening finished")
            fsm_current_state = "open"          # send to open state
            
        # did it somehow reverse and went back to close? dont know how
        elif (ls_open == 0 and ls_close == 1):
            my_globals.status["error_msg"] = "Cover closed itself?"
            logging.error("\tError: Cover closed itself")
            fsm_current_state = "error"         # send to error state
            
        # timed out
        elif (time.time() > wait_time):
            my_globals.status["error_msg"] = "Cover movement timed out. Waiting for it to resolve to open or close"
            logging.error("\tCover movement timed out at %0.1f. Waiting for it to resolve to open or close" % time.time())
            fsm_current_state = "error"         # send to error state
            
        # 0,0 and not timedout 
            # do nothing. we are waiting

    
def fsm_closing():
    logging.info ("Entered State: closing\tSubstate: %s" % fsm_transition_state)
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
        logging.debug ("\tRelay -time is: %0.1f,\t wait time: %0.1f" % (time.time(), wait_time))
        fsm_transition_state = "ts1:RelayWait"
    
    elif fsm_transition_state == "ts1:RelayWait":     # wait - relay off
        if (time.time() >= wait_time):                # if we exceded our wait time
            set_Relay("off")                          # turn off relay
            fsm_transition_state = "ts3:MovingTest"   # go to next transition state
        
    # test if cover is actually moving
    elif fsm_transition_state == "ts3:MovingTest":
        if (ls_open == 0 and ls_close == 0):
            wait_time = time.time() + COVER_WAIT  # waiting x seconds
            logging.debug ("\tCover -time is: %0.1f,\t timout time: %0.1f" % (time.time(), wait_time))
            fsm_transition_state = "ts4:Moving"           # test pass. its moving
        else: 
            my_globals.status["error_msg"] = "Cover did not move"
            logging.error("\tError: Cover did not move. Time now is: %0.1f" % time.time())
            fsm_current_state = "error"         # send to error state
    
    # its moving. lets wait for it to finish
    elif fsm_transition_state == "ts4:Moving":
        # did it finish and close?
        if (ls_open == 0 and ls_close == 1):
            # success
            logging.debug("\tClosing finished")
            fsm_current_state = "closed"          # send to open state
            
        # did it somehow reverse and went back to close? dont know how
        elif (ls_open == 1 and ls_close == 0):
            my_globals.status["error_msg"] = "Cover opened itself?"
            logging.error("\tError: Cover opened itself")
            fsm_current_state = "error"         # send to error state
            
        # timed out
        elif (time.time() > wait_time):
            my_globals.status["error_msg"] = "Cover movement timed out. Waiting for it to resolve to open or close"
            logging.error("\tCover movement timed out at %0.1f. Waiting for it to resolve to open or close" % time.time())
            fsm_current_state = "error"         # send to error state
            
        # 0,0 and not timedout 
            # do nothing. we are waiting
    
def fsm_locked():
    logging.info ("Entered State: locked")
    global fsm_current_state
    if (server_cmd != "lock"):
        fsm_current_state = "error" # to resolve
        fsm_error()                 # run immediatly to resolve state if possible before the next status update
    
# error and resolution
def fsm_error():
    logging.warning ("Entered State: Error")
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
        logging.error ("Unknown error")
        fsm_current_state = "error"

# set relay pin to value
def set_Relay(val):
    if (my_globals.NOT_PI == True):    # this is NOT a pi and NOT usng gpio
        logging.warning ("GPIO disabled")
    else:
        try:
            if (val == "on"):
                logging.info ("Turning relay on")
                GPIO.output(pin_relay, GPIO.HIGH)
            else: # val == "off" or any other value. default off
                logging.info ("Turning relay off")
                GPIO.output(pin_relay, GPIO.LOW)
        except Exception as e:
            logging.error ("\tError setting relay GPIO output pin %r" % e)


# read limit switches
def getSwitches():
    global ls_open, ls_close
    if (my_globals.NOT_PI == True):     # this is NOT a pi and NOT usng gpio
        # Simulate switches based on current state
        logging.warning ("## Simulating switches")
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
            logging.debug ("getSwitches: (%d, %d)" %(ls_open, ls_close))
        except Exception as e:
            logging.error ("Error reading limit switch pins: %r" % e)
        

# This will reset gpios back to what they were before the script started.
# The problem is that this program exits by interruping it and so this will never get called
# Included for best habbit but cant call it outside of the --single run senario
def gpio_cleanup():
    if (my_globals.NOT_PI == False):
        GPIO.cleanup()
