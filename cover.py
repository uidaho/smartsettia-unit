# https://dev.to/karn/building-a-simple-state-machine-in-python
import my_globals
from my_globals import sensor_dat


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
    global ls_open, ls_close
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
    else:
        print ("ERROR: Unknown state.")
    
    # update global variables with current limit switches
    sensor_dat["limitsw_open"]  = ls_open
    sensor_dat["limitsw_close"] = ls_close
    my_globals.status["cover_state"] = fsm_current_state
    print ("Current sensors open/close (%d,%d)"% (sensor_dat["limitsw_open"], sensor_dat["limitsw_close"]))
    print ( "fsm - Next state %s" % fsm_current_state)
    print ("--------------------------------------")
    

def fsm_open():
    print ("Entered State: open")
    global ls_close, ls_close, fsm_current_state
    # if not open. unexpected movement
    if  not (ls_open == 1 and ls_close == 0):
        my_globals.status["error_msg"] = "Unexpected Movement"
        fsm_current_state = "error"
    # check if the we are not were we want to be
    elif (server != fsm_current_state):
        if (server == "closed"):
            print ("Server change event: closing")
            fsm_current_state = "closing"
        elif (server == "locked"):
            print ("Server change event: locked")
            fsm_current_state = "locked"
        else:
            print ("Unknown server change")
            
def fsm_close():
    print ("Entered State: closed")
    global ls_close, ls_close, fsm_current_state
    # if not open. unexpected movement
    if  not (ls_open == 1 and ls_close == 0):
        my_globals.status["error_msg"] = "Unexpected Movement"
        fsm_current_state = "error"
    elif (server != fsm_current_state):
        if (server == "open"):
            print ("Server change event: opening")
            fsm_current_state = "opening"
        elif (server == "locked"):
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
        # command relay
        fsm_transition_state = 1
    
    elif fsm_transition_state == 1:     # wait - relay on
        # wait
        x = 1
        fsm_transition_state = 2
    
    elif fsm_transition_state == 2:     # turn relay off
        # command relay
        fsm_transition_state = 3
        
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

    
def fsm_closing():
    print ("Entered State: closing")
    global ls_open, ls_close, fsm_current_state
    fsm_current_state = "closed"
    
    
# error and resolution
def fsm_error():
    print ("Entered State: Error")
    global ls_open, ls_close, fsm_current_state
    if  (ls_open == 1 and ls_close == 0):
        fsm_current_state = "open"
    elif (ls_open == 0 and ls_close == 1):
        fsm_current_state = "close"
    elif (ls_open == 0 and ls_close == 0):
        fsm_current_state = "error"
    else:
        print ("Unknown error")
        fsm_current_state = "error"
    

# read limit switches
def getSwitches():
    print ("Reading limit switches")
    global ls_open, ls_close
    ls_open  = 1
    ls_close = 0
    
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
    


# Testing Code
fsm()
fsm()
print ("server closed")
server = "closed"
fsm()
fsm()
fsm()
print ("server open")
server = "open"
fsm()
fsm()
fsm()