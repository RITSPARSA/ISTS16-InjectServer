"""
Handle all of the testing
"""
from src.log import Logger
from src.config import Config, ConfigurationObject
from src.handler import Handler
from src.google import Google
from src.mail import parse_email, Mail
from src import files
from src.templates import EmailTemplate
from loremipsum import generate_paragraph
import os
import time

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
        # Inject path count (4) + BaseInject = 5 
        for k in range(0,Config.inject_path_count+1):
            name = names[count]
            count += 1
            fname = "{}/{}.{}_{}.txt".format(idd, j,k,name.replace(" ","_"))
            text = generate_paragraph()[2]
            with open(fname, 'w') as f:
                f.write("{}\n".format(
                        t.render(inject_name=name, inject_number="{}.{}"
                                .format(j,k), inject_body=text)))

    
Logger.log("Initializing the program")
Logger.toggle()
Config = ConfigurationObject("config.yml")
create_mock_injects()


# Create any directories jsut incase we need it
files.create_directories()
# Create the mail object
with Mail() as m:
    hand = Handler(m)
    while True:
        time.sleep(5)
        for e in m.gmail.check_mail():
            hand.handle(*e)
