from datetime import datetime

from temp_reading import read_humidity as read_humidity_sensor
from Humidity import Humidity


def read_humidity():
    humidity_value = read_humidity_sensor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return Humidity(humidity_value, timestamp)