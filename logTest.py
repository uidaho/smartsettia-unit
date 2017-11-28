import logging
#logging.basicConfig(filename='example.log',level=logging.DEBUG)


class MyFormatter(logging.Formatter):

    err_fmt  = "%(asctime)-15s %(levelname)s: %(module)s: %(message)s"
    war_fmt  = "%(asctime)-15s %(levelname)s: %(module)s: %(message)s"
    dbg_fmt  = "\tDBG: %(module)s: %(lineno)d: %(msg)s"
    info_fmt = "%(asctime)-15s %(levelname)s: %(message)s"
    

    def __init__(self):
        super().__init__(fmt="%(levelno)d: %(msg)s", datefmt=None, style='%')  

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


#
#FORMAT = "%(asctime)-15s %(levelname)s: %(message)s"
#logging.basicConfig(format=FORMAT, level=logging.DEBUG)
#
#
#d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
#logging.warning("Protocol problem: %s", "connection reset", extra=d)

import logging

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
formatter = MyFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.WARNING)

logger.debug('often makes a very good meal of %s', 'visiting tourists')
logger.debug('This message should go to the log file')
logger.debug('This message is debugging')
logger.info('So should this')
logger.error("This is an error")
logger.warning('And this, too')
logging.warning('And this, too')

logger.setLevel(logging.DEBUG)

logging.debug('This message is debugging')