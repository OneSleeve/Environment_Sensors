from bme280_lib import *
import machine


def init(i2c_bus):
    bme280 = BME280(i2c = i2c_bus)
    
    return bme280

def get_values(bme280):
    return bme280.read_compensated_data()

def pressure(bme280):
    values = get_values(bme280)

    pressure_in_bar = int(values[1]) / 256 / 100000
    
    return pressure_in_bar

def air_temperature(bme280):
    values = get_values(bme280)
    return values[0] / 100

def humidity(bme280):
    values = get_values(bme280)
    return int(values[2]) / 1024