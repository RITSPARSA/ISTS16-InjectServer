"""
Manages all the configuration settings for the project.
Accessible to anyone who imports it
Author: Micah Martin (mjm5097@rit.edu)
"""

import yaml
from json import dumps
#from .log import Logger

class ConfigurationObject(object):
    """Manages the global configuration objects
    accessible to anyone who imports it
    """
    def __init__(self, filename="config.yml"):
        # Default configuration
        defaults = {"name":"InjectManager", "injects":"injects/",
        "results":"results/", "templates":"InjectManager/templates/",
        "loglevel":2} 
        data = dict(defaults)
        # Try to open the filename and load the data from it
        if filename is not None:
            try:
                with open(filename) as fil:
                    data = yaml.safe_load(fil)
                #Logger.log("Loaded settings from {}".format(filename))
            except:
                #Logger.warn("No configuration in {}, using defaults"
                #    .format(filename))
                pass
        # Check for missing config values
        for v in defaults:
            if v not in data:
                data[v] = defaults[v] # set missing val from defaults
                #Logger.warn(
                #"Configuration value \"{}\" not set. Using \"{}\""
                #.format(v, defaults[v]))
        self.__dict__.update(data) # Set the data as obj. properties


    def print_config(self):
        data = dumps(self.__dict__, sort_keys=True, indent=4,
                     separators=(',', ': '))
        print(data)

Config = ConfigurationObject()
