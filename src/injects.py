"""
All things handling the parsing of Inject files
Author: Micah Martin (mjm5097@rit.edu)
"""

from os import walk
from .log import Logger

class Inject(object):
    """An object which holds an inject and parses the file
    for the name and inject number
    """
    def __init__(self, fil):
        """Read an inject file and parse out the name, number,
        and body of the inject.
        """
        with open(fil) as f:
            lines = f.read() # Get the lines of the inject file
        try:
            i = lines.index('\n') # first the first occurence of a new line
            firstline = lines[:i].strip() # the first line
            self.text = lines[i:].strip() # the body
            firstline = firstline.split(":",1) # "1.1: Inject name"
            self.number, self.name = [n.strip() for n in firstline[:]]
            self.file = fil
            float(self.number) # Make sure this is a float or int
            if self.text == "" or self.name == "":
                raise ValueError() # make sure nothing is empty
        except:
            raise ValueError("Invalid inject in {}".format(fil))

    def __str__(self):
        return "Inject {}: {}".format(self.number, self.name)
    def __repr__(self):
        return str(self.number)
    
    def islate(self):
        """Check whether this inject can still be submitted
        """
        if int(float(self.number)) == float(self.number):
            return True # TODO actually check if the inject is late
        else:
            return False # all sub injects are never late
    
    def get(self):
        """Update all the values and return the body of inject
        """
        with open(self.file) as f:
            lines = f.read() # Get the lines of the inject file
        try:
            i = lines.index('\n') # find first new line
            firstline = lines[:i].strip() # the first line
            self.text = lines[i:].strip() # the body
            firstline = firstline.split(":",1) # "1.1: Inject name"
            self.number, self.name = [n.strip() for n in firstline[:]]
            float(self.number) # Make sure this is a float or int
            if self.text == "" or self.name == "":
                raise ValueError() # make sure nothing is empty
        except:
            raise ValueError("Invalid inject in {}".format(fil))
        return self.body

class Injects(object):
    """Manages all of the injects that are loaded
    """
    def __init__(self, directory):
        """Loads all the injects from a given path
        """
        def append_slash(dirname):
            if dirname[-1] != "/":
                dirname+="/"
            return dirname
        
        self.injects = {}
        inject_files = []
        for (path, dirs, files) in walk(directory):
            inject_files += [ append_slash(path)+f for f in files ]

        for f in inject_files:
            try:
                inj = Inject(f) # Try to create an inject number
                self.injects[inj.number] = inj # Add to the injects
            except ValueError:
                Logger.warn("Cannot load inject {}. Skipping."\
                    .format(f.strip()))
        Logger.update("Loaded {} injects from \"{}\"".format(
                    len(self.injects), directory))
    
    def __str__(self):
        loaded = [ str(i) for i in self.injects.values()]
        return "Loaded injects:\n\t{}".format("\n\t".join(loaded))

    def next_path(self, current):
        """Finds the next minor inject in the inject path
        Returns None if there is not another
        """
        if isinstance(current, Inject):
            current = str(repr(current)) # If an inj. obj. get the inj. number
        if current not in self.injects:
            # Error if the current inject doesnt exist
            raise ValueError("Inject {} not loaded".format(current)) 
        try:
            current = float(current) # Turn the number into a float
        except:
            raise ValueError("Not a valid inject number: {}".format(current))
        
        nxt = str(current + 0.1) # Inc. by .1 for the next minor inject
        if nxt in self.injects:
            return self.injects[nxt]
        else:
            return None
    
    def get(self, inject):
        """return the inject object for a string
        Returns None if the inject doesnt exist
        """
        try:
            return self.injects[str(inject)]
        except:
            return None

    def next(self, current):
        """Finds the next major inject in the inject path
        Returns None if there is not another
        """
        if isinstance(current, Inject):
            current = str(repr(current)) # If an inject obj, get the inj. number
        if current not in self.injects:
            # Error if the current inject doesnt exist
            raise ValueError("Inject {} not loaded".format(current))
                
        try:
            current = int(float(current)) # Convert to an int
        except:
            raise ValueError("Not a valid inject number: {}".format(current))
        
        nxt = str(current+1) # Get the next major number
        if nxt in self.injects:
            return self.injects[nxt]
        else:
            return None

    def first(self):
        """Return the first inject
        """
        key = sorted(self.injects.keys())
        return self.injects[key[0]]

    def isinject(self, name):
        return str(name) in self.injects.keys()
        
