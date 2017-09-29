import time
import uuid
import my_globals

error_filename = "error.log"    # name of log file
log_filename =   "log.log"
t0 = time.time()                # program start time

# log file setup for program start
file=open(error_filename,"a")
file.write("\nProgram start" + "\n")
file.write(str(time.time()) + "\n")
file.write("-------------" + "\n")
file.close()

# usage
# print_error("name of function", "error description")
# print_error("remote_comm:register", "something happened")
# This function will print the error to terminal as well as write the error to file
def print_error(fun_name, error):
    global t0           # time of program start
    t1 = time.time()    # current time
    t = t1 - t0         # run time
    error_msg = "ERROR: %d:\t%s:\t%r" %(t,fun_name,error)
    print (error_msg)

    # also right error to file
    try:
        file=open(error_filename,"a")
        file.write(error_msg + "\n")
        file.close()
    except:
        print ("ERROR: Helper_lib: File error")

def print_log(fun_name, log_text, term=1):
    global t0           # time of program start
    t1 = time.time()    # current time
    t = t1 - t0         # run time
    error_msg = "Log: %d:\t%s:\t%s" %(t,fun_name,log_text)
    if term == 1:
        print (error_msg)

    # also right error to file
    try:
        file=open(error_filename,"a")
        file.write(log_text + "\n")
        file.close()
    except:
        print ("ERROR: Helper_lib:print_log: File error")


def generate_uuid():
    # https://stackoverflow.com/questions/159137/getting-mac-address
    seed = uuid.getnode()       # returns 48bit value from MAC or rand number if not found
    uu = str(uuid.uuid5(uuid.NAMESPACE_URL, str(seed)))
    print ("uuid: ", uu)
    my_globals.settings["uuid"] = uu
