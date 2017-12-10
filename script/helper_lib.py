import time
import uuid
from uuid import UUID   # for some reason UUID is not imported when importing all of uuid
import my_globals
import logging


def generate_uuid():
    # https://stackoverflow.com/questions/159137/getting-mac-address
    seed = uuid.getnode()       # returns 48bit value from MAC or rand number if not found
    uu = str(uuid.uuid5(uuid.NAMESPACE_URL, str(seed)))
    logging.info ("uuid: %s" % uu)
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
        logging.error("error: %r" % e)
        return False

    return str(uuid_obj) == uuid_to_test



# Custom formatter for logging
# source: https://stackoverflow.com/a/14859558
class MyFormatter(logging.Formatter):

    err_fmt  = "%(asctime)-15s %(levelname)s: %(module)s: %(message)s"
    war_fmt  = "%(asctime)-15s %(levelname)s: %(module)s: %(message)s"
    dbg_fmt  = "\tDBG: %(module)s: %(lineno)d: %(message)s"
    info_fmt = "%(asctime)-15s %(levelname)s: %(message)s"
    
    def __init__(self):
        super().__init__(fmt="%(levelno)d: %(message)s", datefmt=None, style='%')  

    def format(self, record):

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == logging.DEBUG:
            self._style._fmt = MyFormatter.dbg_fmt

        elif record.levelno == logging.INFO:
            self._style._fmt = MyFormatter.info_fmt

        elif record.levelno == logging.ERROR:
            self._style._fmt = MyFormatter.err_fmt
            
        elif record.levelno == logging.WARNING:
            self._style._fmt = MyFormatter.war_fmt

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._style._fmt = format_orig

        return result