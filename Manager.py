from src.log import Logger
from src import config
from src.handler import Handler
from src.google import Google
from src.mail import parse_email

config.Config = config.ConfigurationObject("config.yml")
hand = Handler()
x = parse_email("tests/unknown_format.txt")
hand.handle(*x)
#g = Google("config.txt")
#g.creates({})
