from __future__ import print_function

"""
Handles the logging of all the other functions
Author: Micah Martin (mjm5097@rit.edu)
"""

class LoggerObject(object):
    def __init__(self, loglevel=2):
        """Set the loglevel
        0 = None
        1 = Errors only
        2 = Everything
        """
        self.loglevel = loglevel

    def log(self, *args, **kwargs):
        """Log normal if the logging level is correct
        """
        if self.loglevel > 1:
            print(*args, **kwargs)
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

Logger = LoggerObject(2)
