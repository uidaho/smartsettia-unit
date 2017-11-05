import time
import uuid
from uuid import UUID   # for some reason UUID is not imported when importing all of uuid
import my_globals

t0 = time.time()                # program start time

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
        file=open(my_globals.settings["storage_dir"] + "error.log","a")
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


# taken from https://stackoverflow.com/a/33245493
def is_valid_uuid(uuid_to_test, version=5):
    """
    Check if uuid_to_test is a valid UUID.

    Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.

    Examples
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except Exception as e:
        # print ("error: ", e)
        return False

    return str(uuid_obj) == uuid_to_test
