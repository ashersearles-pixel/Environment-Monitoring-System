import time

from datetime import datetime

from .Humidity import Humidity

Humidity = Humidity()

def read_humidity():
    #add code to read humidity from sensor and return a Humidity object
    return Humidity