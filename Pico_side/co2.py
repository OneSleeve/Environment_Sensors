import machine
import ccs811

def init(i2c_bus):
    ccs811_device = ccs811.CCS811(i2c_bus)
    ccs811_device.setup()

    return ccs811_device

def data(ccs811_device):
    if ccs811_device.data_available():
        result = ccs811_device.read_algorithm_results()
        return result

def reset(ccs811_device):
    ccs811_device.reset()