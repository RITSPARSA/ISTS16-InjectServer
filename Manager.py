from src.log import Logger
from src import Inject

x = Inject.Injects("injects/")
print(x.first())
