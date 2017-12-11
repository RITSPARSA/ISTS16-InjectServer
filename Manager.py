from src.config import Config, ConfigurationObject
from src.log import Logger
from src import injects


Config = ConfigurationObject("config.yml")
Logger.blue("[*] Loading injects...")
x = injects.Injects("injects/")
print(x.first())
