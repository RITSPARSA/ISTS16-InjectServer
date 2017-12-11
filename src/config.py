"""
Manages all the configuration settings for the project.
Accessible to anyone who imports it
Author: Micah Martin (mjm5097@rit.edu)
"""

import yaml
from json import dumps
from .log import Logger

class ConfigurationObject(object):
    """Manages the global configuration objects
    accessible to anyone who imports it
    """
    def __init__(self, filename="config.yml"):
        # Default configuration
        defaults = ["name", "inject_directory", "inject_count",
        "inject_path_count", "max_teams", "template_directory",
        "log_level", "log_file"]
        
        # Try to open the filename and load the data from it
        try:
            with open(filename) as fil:
                data = yaml.safe_load(fil)
            Logger.update("Loaded settings from {}".format(filename))
        except:
            Logger.error("Config file {} does not exist".format(filename))
            raise BaseException("Configuration file does not exist")
        # Check for missing config values
        error = False
        for v in defaults:
            if v not in data:
                Logger.warn("Configuration missing setting for " + v)
                error = True
        if error:
            raise BaseException("Configuration file not complete.\
                            Check log for missing values")
        self.__dict__.update(data) # Set the data as obj. properties


    def print_config(self):
        data = dumps(self.__dict__, sort_keys=True, indent=4,
                     separators=(',', ': '))
        print(data)

Config = ConfigurationObject()
Logger.loglevel = Config.log_level
