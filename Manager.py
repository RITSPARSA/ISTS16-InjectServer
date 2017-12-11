from src.log import Logger
from src import config
from src.handler import Handler
from src.google import Google
from src.mail import parse_email
from src import files
Logger.log("Initializing the program")
Logger.toggle()
config.Config = config.ConfigurationObject("config.yml")
files.setup()
hand = Handler()
x = parse_email("tests/correct.txt")
hand.handle(*x)
x = parse_email("tests/sub23.txt")
hand.handle(*x)
#g = Google("config.txt")
#g.creates({})
