from __future__ import print_function

"""
Handles the logging of all the other functions
Author: Micah Martin (mjm5097@rit.edu)
"""

from .config import Config
class LoggerObject(object):
    def __init__(self, loglevel=3):
        """Set the loglevel
        0 = None
        1 = Errors only
        2 = Add warnings
        3 = Everything
        """
        self.colors = {
	    "purple":'\033[95m',
	    "blue":'\033[94m',
	    "green":'\033[92m',
	    "yellow":'\033[93m',
	    "red":'\033[91m',
	    "clear":'\033[0m',
	    "bold":'\033[1m',
	    "underline":'\033[4m'
	}
        self.loglevel = loglevel

    def log(self, *args, **kwargs):
        """Log normal if the logging level is correct
        """
        if self.loglevel > 2:
            print(*args, **kwargs)
            return True
        return False
    
    def warn(self, *args,color="clear", **kwargs):
        """Log warning if the logging level is correct
        """
        color = "\033[93m"
        clear = "\033[0m"
        if self.loglevel > 1:
            print(color, end="")
            print(*args, **kwargs)
            print(clear, end="")
            return True
        return False
    
    def error(self, *args, **kwargs):
        """Log error if the logging level is correct
        """
        red = "\033[91m"
        clear = "\033[0m"
        if self.loglevel > 0:
            print(red, end="")
            print(*args, **kwargs)
            print(clear, end="")
            return True
        return False

Logger = LoggerObject(Config.loglevel)
