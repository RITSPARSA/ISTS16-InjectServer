"""
All things handling the parsing of Inject files
Author: Micah Martin (mjm5097@rit.edu)
"""

from re import findall
from os import walk
from .log import Logger
import jinja2

class EmailTemplate(object):
    """An object which holds a jinja template
    """
    def __init__(self, fil):
        """keep track of a jinja template and make sure all the needed variables
        are in the data
        """
        self.file = fil
        self.needed = []
        self.data = ""
        self.get_data()
    
    def render(self, **kwargs):
        self.get_data()
        for v in self.needed:
            if v not in self.needed:
                raise ValueError('"{}" value needed to render template "{}"'
                    .format(v, self.file))
        temp = jinja2.Template(self.data)
        return temp.render(**kwargs) # Return the rendered template

    def get_needed(self):
        self.get_data()
        return self.needed

    def get_data(self):
        """Get all the needed variables
        """
        try:
            with open(self.file) as f:
                lines = f.read() # Get the lines of the template file
            # Find all the variables in the template
            self.data = lines
            needed_vars = findall(r'\{\{ [A-Za-z_]+ \}\}', lines)
            for v in needed_vars:
                v = v.replace("{{","").replace("}}","").strip()
                self.needed.append(v)
            return True 
        except:
            raise ValueError("No template in {}".format(self.file))

class Templates(object):
    """Manages all of the injects that are loaded
    """
    def __init__(self, directory):
        """Loads all the injects from a given path
        """
        self.templates = {}
        for (path, dirs, files) in walk(directory):
            for f in files:
                try:
                    name = f.split(".")[0]
                    tmp = EmailTemplate(path+f)
                    self.templates[name] = tmp
                except ValueError:
                    Logger.warn("Cannot load template {}. Skipping."\
                        .format(f.strip()))
        Logger.update("Loaded {} templates from \"{}\"".format(
                        len(self.templates), directory))
        self.__dict__.update(self.templates)
    
