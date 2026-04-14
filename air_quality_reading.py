import board
import busio
import adafruit_sgp40
from datetime import datetime

from temp_reading import read_temperature
from humidity_reading import read_humidity


i2c = board.I2C()
_sgp40_sensor = adafruit_sgp40.SGP40(i2c)


class AirQuality:
    def __init__(self, iaq_index, raw_value, temperature, humidity, timestamp):
        self.iaq_index = iaq_index
        self.raw_value = raw_value
        self.temperature = temperature
        self.humidity = humidity
        self.timestamp = timestamp

    def get_iaq(self):
        return self.iaq_index

    def get_raw(self):
        return self.raw_value

    def get_temperature(self):
        return self.temperature

    def get_humidity(self):
        return self.humidity

    def get_timestamp(self):
        return self.timestamp

    def is_warming_up(self):
        return self.iaq_index == 0 and self.raw_value > 0


def read_air_quality():
    temperature_value = read_temperature().get_value()
    humidity_value = read_humidity().get_value()

    if temperature_value is None:
        temperature_value = 25.0
    if humidity_value is None:
        humidity_value = 50.0

    raw_value = _sgp40_sensor.measure_raw(
        temperature=temperature_value,
        relative_humidity=humidity_value,
    )
    iaq_index = _sgp40_sensor.measure_index(
        temperature=temperature_value,
        relative_humidity=humidity_value,
    )
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return AirQuality(iaq_index, raw_value, temperature_value, humidity_value, timestamp)
