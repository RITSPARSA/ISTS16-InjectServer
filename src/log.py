from __future__ import print_function

"""
Handles the logging of all the other functions
Author: Micah Martin (mjm5097@rit.edu)
"""

class LoggerObject(object):
    def __init__(self, loglevel=3):
        """Set the loglevel
        0 = None
        1 = Errors only
        2 = Add warnings
        3 = Normal Messages
        4 = Extra verbose
        """
        self.loglevel = loglevel
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

    def color(self, string, color=""):
        """Color a string
        """
        try:
            s = self.colors[color] # Try to get the color
            e = self.colors["clear"]
        except:
            s, e = "","" # Blank if error

        return "{}{}{}".format(s, string, e)

    def log(self,*args, **kwargs):
        """Show a blue message. Random tasks that are happening
        """
        if self.loglevel > 2:
            args = ["[*]"] + [str(x) for x in args] # convert to str
            print(self.color(" ".join(args), "purple"), **kwargs)
            return True
        return False
    
    def plain(self,*args, **kwargs):
        """Show a plain message. Random tasks that are happening
        """
        if self.loglevel > 2:
            print(*args, **kwargs)
            return True
        return False
    
    def green(self,*args, **kwargs):
        """Show a success message.
        """
        if self.loglevel > 2:
            args = ["[*]"] + [str(x) for x in args] # convert to str
            print(self.color(" ".join(args), "blue"), **kwargs)
            return True
        return False
    
    def update(self,*args, **kwargs):
        """Show a blue message. Random tasks that are happening
        """
        if self.loglevel > 3:
            args = ["[*]"] + [str(x) for x in args] # convert to str
            print(self.color(" ".join(args), "blue"), **kwargs)
            return True
        return False

    def warn(self,*args, **kwargs):
        """Show a yellow warning
        """
        if self.loglevel > 1:
            args = ["[!]"] + [str(x) for x in args] # convert to str
            print(self.color(" ".join(args), "yellow"), **kwargs)
            return True
        return False
    
    def error(self,*args, **kwargs):
        """Show a yellow warning
        """
        if self.loglevel > 0:
            args = ["[!]"] + [str(x) for x in args] # convert to str
            print(self.color(" ".join(args), "red"), **kwargs)
            return True
        return False

Logger = LoggerObject(2)
