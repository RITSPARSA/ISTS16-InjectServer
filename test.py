"""
Handle all of the testing
"""
from src.log import Logger
from src.config import Config, ConfigurationObject
from src.handler import Handler
from src.google import Google
from src.mail import parse_email
from src import files
from src.templates import EmailTemplate
from loremipsum import generate_paragraph
import os

def create_mock_injects():
    """Generate a bunch of mock injects
    """
    count = Config.inject_count*(Config.inject_path_count+1)
    with open("tests/names.txt") as fil:
        names = [l.strip() for l in fil.readlines()[:count]]
        count = 0
    def created(dirr):
        if not os.path.exists(dirr):
            os.makedirs(dirr)
    # Make the injects directory
    rd = Config.inject_directory
    created(rd)
    t = EmailTemplate("src/templates/inject.j2")
    for j in range(1, Config.inject_count+1):
        idd = "{}/{}".format(rd,j)
        created(idd)
        for k in range(Config.inject_path_count+1):
            name = names[count]
            count += 1
            fname = "{}/{}.{}_{}.txt".format(idd, j,k,name.replace(" ","_"))
            text = generate_paragraph()[0]
            with open(fname, 'w') as f:
                f.write("{}\n".format(
                        t.render(inject_name=name, inject_number="{}.{}"
                                .format(j,k), inject_body=text)))

    
Logger.log("Initializing the program")
Logger.toggle()
Config = ConfigurationObject("config.yml")
create_mock_injects()
