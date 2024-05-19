import machine
from time import sleep_ms

#Calibraton values
min_moisture=13650
max_moisture=25000

def init(adc):
    return machine.ADC(26)

def moisture(moisture_device):
    """
    This mothed reads out the moisture sensore 20 times and averages out the reading
    in order to get a more precise output
    """
#     readings = []
# 
#     for _ in range(10):
#         sleep_ms(10)
#         readings.append(moisture_device.read_u16())
# 
#     soil = sum(readings) / len(readings)
    
    soil = moisture_device.read_u16()
    
    moisture_in_percent = (max_moisture-soil)*100/(max_moisture-min_moisture)
    
    return moisture_in_percent