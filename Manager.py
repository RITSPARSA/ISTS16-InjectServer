from src.config import Config, ConfigurationObject
from src.log import Logger
from src.handler import Handler

Config = ConfigurationObject("config.yml")
hand = Handler()
hand.handle("team1@test.ists", "team 1: inject 1.1", "blahblha")
hand.handle("team1@test.ists", "team 1: inj1", "blahblha")
hand.handle("team1@test.ists", "team 1: inject 1.1", "blahblha")
