from .config import Config
from .log import Logger
import os

def setup():
    def created(dirr):
        if not os.path.exists(dirr):
            os.makedirs(dirr)
    # Make the results directory
    rd = Config.results_directory
    created(rd)
    # Create a directory for each team
    for i in range(1, Config.max_teams+1):
        td = "{}team{}".format(rd,i)
        created(td)
        for j in range(1, Config.inject_count+1):
            idd = "{}/{}".format(td,j)
            created(idd)

def write(team, inject, filename):
    full = "{}team{}/{}/{}".format(Config.results_directory,
        team, int(float(inject)), filename)
    with open(full, 'w') as f:
        f.write("touch\n")

def is_tagged(team, inject, tag):
    filename = ".{}.{}".format(inject, tag)
    full = "{}team{}/{}/{}".format(Config.results_directory,
        team, int(float(inject)), filename)
    return os.path.exists(full)

def mark_tag(team, inject, tag):
    filename = ".{}.{}".format(inject, tag)
    write(team, inject, filename)
