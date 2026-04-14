
import time
from types import SimpleNamespace

from datetime import datetime

try:
    from .Temperature import Temperature
except ImportError:
    from Temperature import Temperature

try:
    import smbus2 as smbus
except ImportError:
    try:
        import smbus # type: ignore
    except ImportError:
        class SMBus:
            def __init__(self, bus): pass
            def read_byte_data(self, addr, reg): return 0
            def write_byte_data(self, addr, reg, value): pass

        smbus = SimpleNamespace(SMBus=SMBus)

HTS221_ADDRESS = 0x5F
CTRL_REG1 = 0x20
TEMP_OUT_L = 0x2A
TEMP_OUT_H = 0x2B
T0_DEGC_X8 = 0x32
T1_DEGC_X8 = 0x33
T0_T1_MSB = 0x35
T0_OUT_L = 0x3C
T0_OUT_H = 0x3D
T1_OUT_L = 0x3E
T1_OUT_H = 0x3F

# Initialize I2C bus
bus = smbus.SMBus(1)

def read_register(reg):
    return bus.read_byte_data(HTS221_ADDRESS, reg)

def write_register(reg, value):
    bus.write_byte_data(HTS221_ADDRESS, reg, value)

def read_signed_16(low_reg, high_reg):
    value = read_register(low_reg) | (read_register(high_reg) << 8)
    if value > 32767:
        value -= 65536
    return value


def init_sensor():
    write_register(CTRL_REG1, 0x85)


def read_temperature():
    # Enable the sensor
    init_sensor()

    # Read calibration data
    T0_degC = read_register(T0_DEGC_X8)
    T1_degC = read_register(T1_DEGC_X8)
    T0_T1_msb = read_register(T0_T1_MSB)
    
    T0_degC |= (T0_T1_msb & 0x03) << 8
    T1_degC |= (T0_T1_msb & 0x0C) << 6
    
    T0_degC /= 8.0
    T1_degC /= 8.0

    # Read temperature raw data
    T0_out = read_signed_16(T0_OUT_L, T0_OUT_H)
    T1_out = read_signed_16(T1_OUT_L, T1_OUT_H)
    temp_out = read_signed_16(TEMP_OUT_L, TEMP_OUT_H)

    # Convert raw value to temperature
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if (T1_out - T0_out) == 0:
        temperature = Temperature(0, timestamp)
        return temperature

    temperature_value = T0_degC + (temp_out - T0_out) * (T1_degC - T0_degC) / (T1_out - T0_out)
    temperature_value = round(temperature_value, 2)
    return Temperature(temperature_value, timestamp)

# Test the sensor
if __name__ == "__main__":
    while True:
        temp = read_temperature()
        # insert_temperature(temp)
        print(f"Temperature: {temp.get_value()}°C")
        time.sleep(1)
