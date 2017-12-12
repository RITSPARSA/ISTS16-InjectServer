from .config import Config
from .log import Logger
import os

def create_directories():
    keys = ['cache_directory', 'inject_directory', 'secrets_directory',
                'results_directory', 'template_directory']
    for k in keys:
        path = Config.get(k)
        if not os.path.exists(path):
            os.mkdir(path)

def write_file(filename, contents):
    path = filename.split("/")[0:-1]
    if path:
        path = "/".join(path)
        if not os.path.exists(path):
            os.mkdir(path)
    with open(filename, 'w') as fil:
        fil.write(contents)
